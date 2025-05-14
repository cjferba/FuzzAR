import numpy as np
import pandas as pd
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt

class FuzzyAssociationRuleMiner:
    """
    Minería y visualización de reglas de asociación difusas.
    Paper base: https://www.sciencedirect.com/science/article/pii/S0888613X21001031
    """

    def __init__(self, fuzzy_sets, min_support=0.1, min_confidence=0.5):
        self.fuzzy_sets = fuzzy_sets
        self.min_support = min_support
        self.min_confidence = min_confidence

    def triangular_mf(self, x, a, b, c):
        x = float(x)
        if a == b == c:
            return float(x == a)
        return max(min((x - a) / (b - a) if b - a != 0 else 0, (c - x) / (c - b) if c - b != 0 else 0, 1), 0)

    def fuzzify(self, df):
        fuzzified_data = []
        for _, row in df.iterrows():
            fuzz_row = {}
            for attr, sets in self.fuzzy_sets.items():
                fuzz_row[attr] = {}
                for set_name, (a, b, c) in sets.items():
                    fuzz_row[attr][set_name] = self.triangular_mf(row[attr], a, b, c)
            fuzzified_data.append(fuzz_row)
        return fuzzified_data

    def all_fuzzy_items(self):
        return [(attr, label)
                for attr, sets in self.fuzzy_sets.items()
                for label in sets.keys()]

    def fuzzy_support(self, fuzzified_data, itemset):
        scores = []
        for row in fuzzified_data:
            grades = [row[attr][label] for attr, label in itemset]
            scores.append(min(grades))
        return np.mean(scores)

    def fuzzy_confidence(self, fuzzified_data, antecedent, consequent):
        num, denom = 0.0, 0.0
        for row in fuzzified_data:
            ant = min([row[attr][label] for attr, label in antecedent])
            cons = min([row[attr][label] for attr, label in consequent])
            num += min(ant, cons)
            denom += ant
        return num / denom if denom > 0 else 0

    def certainty_factor(self, fuzzified_data, antecedent, consequent):
        conf = self.fuzzy_confidence(fuzzified_data, antecedent, consequent)
        cons_supp = self.fuzzy_support(fuzzified_data, consequent)
        return (conf - cons_supp) / (1 - cons_supp) if cons_supp < 1 else 0

    def mine_rules(self, df, max_rule_length=None):
        fuzzified_data = self.fuzzify(df)
        fuzzy_items = self.all_fuzzy_items()
        n_atrib = len(self.fuzzy_sets)
        results = []
        max_rl = max_rule_length or n_atrib
        for total_len in range(2, max_rl + 1):
            for itemset in combinations(fuzzy_items, total_len):
                used_attribs = [attr for attr, _ in itemset]
                if len(set(used_attribs)) != len(used_attribs):
                    continue
                for split in range(1, total_len):
                    antecedent = itemset[:split]
                    consequent = itemset[split:]
                    antecedent_attrs = set([a for a, _ in antecedent])
                    consequent_attrs = set([a for a, _ in consequent])
                    if antecedent_attrs & consequent_attrs:
                        continue
                    supp = self.fuzzy_support(fuzzified_data, itemset)
                    if supp < self.min_support:
                        continue
                    conf = self.fuzzy_confidence(fuzzified_data, antecedent, consequent)
                    if conf < self.min_confidence:
                        continue
                    cf = self.certainty_factor(fuzzified_data, antecedent, consequent)
                    results.append({
                        'antecedent': antecedent,
                        'consequent': consequent,
                        'support': supp,
                        'confidence': conf,
                        'certainty_factor': cf
                    })
        return sorted(results, key=lambda x: x['certainty_factor'], reverse=True)

    def print_rules(self, rules, top_n=10):
        print(f"\nTop {top_n} reglas difusas (ordenadas por CF):\n")
        for i, rule in enumerate(rules[:top_n]):
            ant = ' y '.join([f"{a} es '{v}'" for a, v in rule['antecedent']])
            cons = ' y '.join([f"{a} es '{v}'" for a, v in rule['consequent']])
            print(f"{i + 1}. Si {ant} => {cons}, "
                  f"soporte={rule['support']:.2f}, "
                  f"conf={rule['confidence']:.2f}, "
                  f"CF={rule['certainty_factor']:.2f}")

    def rules_to_dataframe(self, rules):
        data = []
        for rule in rules:
            ant = ' & '.join([f"{a}='{v}'" for a, v in rule['antecedent']])
            cons = ' & '.join([f"{a}='{v}'" for a, v in rule['consequent']])
            data.append({
                'antecedent': ant,
                'consequent': cons,
                'support': rule['support'],
                'confidence': rule['confidence'],
                'certainty_factor': rule['certainty_factor']
            })
        return pd.DataFrame(data).sort_values('certainty_factor', ascending=False, ignore_index=True)

    def rules_summary(self, rules_df):
        print("\nResumen de reglas encontradas:")
        print('Cantidad total de reglas:', len(rules_df))
        if len(rules_df) > 0:
            print(f"Soporte - media: {rules_df['support'].mean():.3f}, min: {rules_df['support'].min():.3f}, max: {rules_df['support'].max():.3f}")
            print(f"Confianza - media: {rules_df['confidence'].mean():.3f}, min: {rules_df['confidence'].min():.3f}, max: {rules_df['confidence'].max():.3f}")
            print(f"Certainty Factor - media: {rules_df['certainty_factor'].mean():.3f}")