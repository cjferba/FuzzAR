Uso de FuzzAR
=============

Ejemplo básico de uso:

.. code-block:: python

   from fuzzy_association_rule_miner import FuzzyAssociationRuleMiner
   from fuzzy_visualization import plot_graph

   data = {...}
   variable_defs = {...}
   miner = FuzzyAssociationRuleMiner(data, variable_defs)
   rules = miner.extract_rules()
   plot_graph(miner.to_graph())
