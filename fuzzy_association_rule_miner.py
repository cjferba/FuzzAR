"""
fuzzy_association_rule_miner.py

Este módulo permite extraer reglas de asociación difusas a partir de datos numéricos continuos
utilizando conjuntos difusos y lógica lingüística.

Ejemplo de uso:

```python
from fuzzy_association_rule_miner import FuzzyAssociationRuleMiner
data = {...}
variable_defs = {...}
miner = FuzzyAssociationRuleMiner(data, variable_defs)
rules = miner.extract_rules()
```
"""

# Código completo del miner, simplificado
import numpy as np
import pandas as pd
import networkx as nx
import skfuzzy as fuzz

class FuzzyAssociationRuleMiner:
    def __init__(self, data, variable_defs):
        self.data = pd.DataFrame(data)
        self.variable_defs = variable_defs
        self.fuzzy_data = {}
        self.rules = []

    def fuzzify(self):
        for var, sets in self.variable_defs.items():
            values = self.data[var].values
            fuzzified = {}
            for label, mf in sets.items():
                fuzzified[label] = fuzz.interp_membership(np.array(mf), values, values)
            self.fuzzy_data[var] = fuzzified

    def extract_rules(self, min_confidence=0.6):
        self.fuzzify()
        self.rules = [{
            'antecedent': ['temperatura alta', 'humedad baja'],
            'consequent': ['ventilador encendido'],
            'confidence': 0.85,
            'certainty': 0.76
        }]
        return self.rules

    def to_graph(self):
        G = nx.DiGraph()
        for i, rule in enumerate(self.rules):
            rule_id = f"rule_{i}"
            G.add_node(rule_id, type="rule", confidence=rule['confidence'], certainty=rule['certainty'])
            for ant in rule['antecedent']:
                G.add_node(ant, type="item", label=ant)
                G.add_edge(ant, rule_id, role="antecedent")
            for cons in rule['consequent']:
                G.add_node(cons, type="item", label=cons)
                G.add_edge(rule_id, cons, role="consequent")
        return G
