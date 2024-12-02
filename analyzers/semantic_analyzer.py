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
            # store the identifier temporarilu 
            temp = child.value  
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
              elif arg.classification == "Expression":
                self.symbol_table[temp] = self.expression(arg.children[0])
    
    # print for checking anf debugging
    print("Symbol Table:", self.symbol_table)


  '''
    Evaluates an expression

    args: 
      temp = the key to be put in the symbol table
      operation = node with format 
      "
      Class: Addition Expression, Value: None
          |- Class: Op Argument, Value: None
          |     |- Class: Identifier, Value: num
          |- Class: Operation Delimiter, Value: None
          |- Class: Op Argument, Value: None
                |- Class: NUMBR Literal, Value: 13
      "
  '''
  def expression(self, operation):
    op_type = operation.classification
    print(op_type)
    op_args = operation.children

    # Use value to access the value of the operand
    # Use classification to access if identifier or literal
    operand1 = self.evaluate_operand(op_args[0].children[0])
    operand2 = self.evaluate_operand(op_args[2].children[0])

    if op_type == "Addition Expression":
      return operand1 + operand2
    elif op_type == 'Subtraction Expression':
      return operand1 - operand2
    elif op_type == 'Multiplication Expression':
      return operand1 * operand2
    elif op_type == 'Division Expression':
      return operand1 / operand2
    elif op_type == 'Modulo Expression':
      return operand1 % operand2
    elif op_type == 'Max Expression':
      return operand1 if operand1 > operand2 else operand2
    elif op_type == 'Min Expression':
      return operand1 if operand1 < operand2 else operand2


  ''' 
    Evaluates the operand 
    operand is Identifier or Literal
    value is either the identifier name or the literal value

    args: operand = node with format "Class: Identifier, Value: num or Class: NUMBR Literal, Value: 13"
    returns the typecasted value depending on the classification

    TODO: An operand can be an expression?
  '''
  def evaluate_operand(self, operand):
    classification = operand.classification
    value = operand.value

    if classification == 'Identifier':
      if value not in self.symbol_table:
        raise NameError(f"Identifier '{value}' is not initialized.") 
      return self.symbol_table[value]
    elif classification == 'NUMBR Literal':
      return int(value)
    elif classification == 'NUMBAR Literal':
      return float(value)
    elif classification == 'YARN Literal':
      return str(value)
    elif classification == 'TROOF Literal':
      return True if value == "WIN" else False
