class Semantic_Analyzer:
  def __init__(self, parse_tree):
    self.tree = parse_tree
    self.symbol_table = {"IT": None}

  def analyze(self):
    for node in self.tree.children:
      if node.classification == "Start Statement":
        for statement in node.children:
          print(statement.classification)