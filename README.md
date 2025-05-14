# FuzzAR - Fuzzy Association Rule Miner

FuzzAR es una librería en Python para la extracción y visualización de reglas de asociación difusas sobre datos continuos. Usa lógica difusa y grafos para representar y explorar el conocimiento.

## Características

- Soporte para variables lingüísticas y conjuntos difusos.
- Extracción de reglas con factor de certeza.
- Representación de reglas como grafos.
- Visualización y exportación a JSON.
- Documentación generada con ReadTheDocs.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejemplo rápido

```python
from fuzzy_association_rule_miner import FuzzyAssociationRuleMiner
from fuzzy_visualization import plot_graph

# Tus datos y definiciones aquí...
miner = FuzzyAssociationRuleMiner(data, variable_defs)
rules = miner.extract_rules()
plot_graph(miner.to_graph())
```
