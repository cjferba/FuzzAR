from fuzzy_miner.miner import FuzzyAssociationRuleMiner
import pandas as pd

# Cargando datos de ejemplo
df = pd.DataFrame({
    'A': [10, 20, 30, 40],
    'B': [50, 60, 55, 70]
})

# Definir conjuntos difusos
fuzzy_sets = {
    'A': {'Low': (0, 0, 20), 'Medium': (10, 30, 50), 'High': (30, 50, 60)},
    'B': {'Low': (40, 50, 60), 'High': (50, 60, 80)}
}

miner = FuzzyAssociationRuleMiner(fuzzy_sets, min_support=0.05, min_confidence=0.3)
rules = miner.mine_rules(df)
miner.print_rules(rules)

# Exportar como DataFrame
df_rules = miner.rules_to_dataframe(rules)
print(df_rules.head())

# Exportar a grafo y mostrar
miner.export_to_graph(rules, draw=True)