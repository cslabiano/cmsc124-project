class Semantic_Analyzer:
  def __init__(self, parse_tree):
    self.tree = parse_tree
    self.symbol_table = {"IT": None}

  def analyze(self):
    for node in self.tree.children:
      if node.classification == "Start Statement":
        for statement in node.children:
          if statement.classification == "Data Section":
            print("data section")
            self.data_section(statement)
          else:
            for child in statement.children:
              if child.classification == "Expression":
                self.expression(child.children)
    
    return self.symbol_table

  def data_section(self, statement):
    # temporary variable to hold the identifier name
    temp = None  
    for var in statement.children:
      if var.classification == "Variable":
        for child in var.children:
          # finds the identifier node
          if child.classification == "Identifier":  
            for identifier in child.children:
              # checks for actual identifier
              if identifier.classification == "Identifier": 
                # store the identifier temporarilu 
                temp = identifier.value  
                if temp not in self.symbol_table:
                  self.symbol_table[temp] = None
          # find the op argument node
          elif child.classification == "Op Argument":  
            for arg in child.children:
              print(f"Processing: {arg.classification}, Value: {arg.value}")  # Debug print
              # check for literal type
              if arg.classification == "NUMBR Literal":
                # assign value and add to the symbol table  
                self.symbol_table[temp] = int(arg.value)  
              elif arg.classification == "YARN Literal" :
                self.symbol_table[temp] = str(arg.value)
              elif arg.classification == "NUMBAR Literal":
                self.symbol_table[temp] = float(arg.value)
              elif arg.classification == "TROOF Literal":
                self.symbol_table[temp] = True if arg.value == "WIN" else False
    
    # print for checking anf debugging
    print("Symbol Table:", self.symbol_table)

  def expression(self, type):
    if type == "Addition Expression":
      pass
    elif type == "Subtraction Expression":
      pass