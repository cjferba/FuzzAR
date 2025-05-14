import numpy as np
import skfuzzy as fuzz
from itertools import product
import json

class FuzzyAssociationRuleMiner:
    def __init__(self, variables_config, threshold=0.6):
        self.variables_config = variables_config
        self.threshold = threshold
        self.fuzzy_data = {}

    def _generate_membership_funcs(self, universe, label_defs):
        funcs = {}
        for label, params in label_defs.items():
            funcs[label] = fuzz.trimf(universe, params)
        return funcs

    def fuzzify(self, df):
        fuzzified_df = {}
        for var, config in self.variables_config.items():
            universe = config['universe']
            label_defs = config['labels']
            funcs = self._generate_membership_funcs(universe, label_defs)
            fuzzified = []
            for val in df[var]:
                memberships = {
                    label: fuzz.interp_membership(universe, mf, val)
                    for label, mf in funcs.items()
                }
                fuzzified.append(memberships)
            fuzzified_df[var] = fuzzified
        self.fuzzy_data = fuzzified_df

    def _calculate_support(self, var, label):
        values = self.fuzzy_data[var]
        return np.mean([row[label] for row in values])

    def generate_rules(self):
        rules = {}
        num_rows = len(next(iter(self.fuzzy_data.values())))
        var_names = list(self.fuzzy_data.keys())

        for idx in range(num_rows):
            row_vals = {var: self.fuzzy_data[var][idx] for var in var_names}
            combos = []
            for var, memberships in row_vals.items():
                combos.append([(var, lbl, val) for lbl, val in memberships.items() if val >= self.threshold])

            for antecedents in product(*combos):
                for i, ante in enumerate(antecedents):
                    for j, cons in enumerate(antecedents):
                        if i != j:
                            strength = min(ante[2], cons[2])
                            rule = ((ante[0], ante[1]), '=>', (cons[0], cons[1]))
                            rules.setdefault(rule, []).append(strength)

        final_rules = {}
        for rule, vals in rules.items():
            conf = np.mean(vals)
            cons_var, cons_lbl = rule[2]
            supp_cons = self._calculate_support(cons_var, cons_lbl)
            if conf >= self.threshold:
                cf = (conf - supp_cons) / (1 - supp_cons) if supp_cons < 1 else 0
                final_rules[rule] = {
                    'confianza': float(conf),
                    'soporte_consecuente': float(supp_cons),
                    'factor_certeza': float(cf)
                }
        return final_rules

    def build_graph(self, rules):
        graph = {'nodes': [], 'edges': []}
        item_nodes, rule_nodes = {}, {}
        rule_id_map = {}

        for idx, (rule, metrics) in enumerate(rules.items(), start=1):
            rule_id = f"R{idx}"
            rule_id_map[rule] = rule_id
            rule_nodes[rule_id] = {
                'id': rule_id,
                'type': 'rule',
                'confianza': metrics['confianza'],
                'factor_certeza': metrics['factor_certeza']
            }
            for part in [rule[0], rule[2]]:
                label = f"{part[0]} es {part[1]}"
                if label not in item_nodes:
                    item_nodes[label] = {'id': label, 'type': 'item'}

        graph['nodes'] = list(item_nodes.values()) + list(rule_nodes.values())
        for rule, rid in rule_id_map.items():
            ante = f"{rule[0][0]} es {rule[0][1]}"
            cons = f"{rule[2][0]} es {rule[2][1]}"
            graph['edges'].append({'source': ante, 'target': rid, 'role': 'antecedente'})
            graph['edges'].append({'source': rid, 'target': cons, 'role': 'consecuente'})
        return graph

    def export_graph_to_json(self, graph, filename="fuzzy_rules_graph.json"):
        with open(filename, 'w') as f:
            json.dump(graph, f, indent=2)
