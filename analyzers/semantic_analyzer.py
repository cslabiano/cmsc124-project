import re
from PyQt5.QtWidgets import QInputDialog

class Semantic_Analyzer:
  def __init__(self, parse_tree, ui):
    self.tree = parse_tree
    self.symbol_table = {"IT": None}
    self.ui = ui

  def analyze(self):
    for node in self.tree.children:
      if node.classification == "Start Statement":
        for statement in node.children:
          if statement.classification == "Data Section":
            print("data section")
            self.data_section(statement)
          else:
            for child in statement.children:
              type = child.classification
              if type == "Expression":
                self.expression(child.children)
              elif type == 'Typecast': # Could be a typecast or an assignment
                typecast_type = child.children[0].classification
                print(typecast_type)
                if typecast_type == 'Recasting':
                  self.assignment(child.children[0])
                elif typecast_type == 'Explicit Typecast':
                  self.typecast(child.children[0])
              elif type == "Input Keyword":
                self.gimmeh(child.children)
              elif type == "Print Statement":
                self.visible(child.children[1])

    # print for checking anf debugging
    print("Symbol Table:", self.symbol_table)

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
              # print(f"Processing: {arg.classification}, Value: {arg.value}")
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

  '''
    Evaluates an expression

    return: the result of the expression
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

    return: the typecasted value depending on the classification
    args: operand = node with format 
    "
      Class: Identifier, Value: num
      
      or 
      
      Class: NUMBR Literal, Value: 13
      
      or 
      
      Class: Expression, Value: None
        |- Class: Addition Expression, Value: None
            |- Class: Op Argument, Value: None
            |   |- Class: NUMBR Literal, Value: 11
            |- Class: Operation Delimiter, Value: None
            |- Class: Op Argument, Value: None
                |- Class: NUMBR Literal, Value: 6
      "
  '''
  def evaluate_operand(self, operand):
    classification = operand.classification
    value = operand.value

    if classification == 'Identifier':
      if value not in self.symbol_table:
        # TODO: Show semantic error in console
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
    elif classification == 'Expression':
      return self.expression(operand.children[0])

  '''
  assigns a value to a variable
  
  return: void
  args: takes a node (list) in this format
    Class: Recasting, Value: None
      |- Class: Identifier, Value: x
      |- Class: Assignment, Value: None
      |- Class: Op Argument, Value: None
          |- Class: TROOF Literal, Value: WIN
  '''
  def assignment(self, node):
    assignment_node = node[0]
    assignment_type = assignment_node.classification
    if assignment_type == 'Recasting':
      identifier = assignment_node.children[0].value
      new_value = self.evaluate_operand(assignment_node.children[2].children[0])
      
      self.symbol_table[identifier] = new_value

  '''
  typecasts a variable and puts it in IT


  args: takes a node (list) in this format
    Class: Explicit Typecast, Value: None
      Class: Typecast Delimiter, Value: None
      Class: Identifier, Value: x
      Class: Typecast Keyword, Value: None
      Class: Literal, Value: None
        Class: TYPE Literal, Value: NUMBAR

  MAEK 3 A NUMBAR 
  '''
  def typecast(self, node):
    if node.classification == 'Explicit Typecast':
      identifier = node.children[1].value # Name of identifier in symbol table
      type_to_typecast = node.children[3].children[0].value # Type to typecast to 
      identifier_value = self.symbol_table[identifier] # Value to be typecasted 
      it = None

      print(identifier_value)

      # Takes the identifier value and converts it based on the type
      
      # NOOB
      # TODO: Check if tama ba to
      if type_to_typecast == 'NOOB': 
        if type(identifier_value) == str: 
          it = ""
        elif type(identifier_value) == int: 
          it = 0
        elif type(identifier_value) == float: 
          it = 0.0
        elif type(identifier_value) == bool: 
          it = False
        elif identifier_value == None: 
          it = None
      # TROOF
      elif type_to_typecast == 'TROOF':
        if identifier_value == "" or identifier_value == 0:
          it = False
        else:
          it = True
      elif type_to_typecast == 'NUMBAR':
        # NUMBR TO NUMBAR
        if type(identifier_value) == int:
          it = float(identifier_value)
        # TROOF TO NUMBAR
        elif type(identifier_value) == bool: 
          if identifier_value == False:
            it = 0.0
          if identifier_value == True: 
            it = 1.0
        # YARN TO NUMBAR
        elif type(identifier_value) == str:
          it = float(identifier_value)
        # NOOB TO NUMBAR
        elif identifier_value == None: 
          it = 0.0
        elif type(identifier_value) == float: 
          it = identifier_value
      elif type_to_typecast == 'NUMBR':
        # NUMBAR TO NUMBR
        if type(identifier_value) == float:
          it = int(identifier_value)
        # TROOF TO NUMBR
        elif type(identifier_value) == bool:
          if identifier_value == True: 
            it = 1
          elif identifier_value == False: 
            it = 0
        # YARN TO NUMBR
        elif type(identifier_value) == str: 
          it = int(identifier_value)
        # NOOB TO NUMBR
        elif identifier_value == None: 
          it = 0
        # NUMBR TO NUMBR
        elif type(identifier_value) == int: 
          it = identifier_value
      elif type_to_typecast == 'YARN':
        # NUMBR or NUMBAR to YARN
        if re.fullmatch(r"\-?[0-9]+\.[0-9]+\b", str(identifier_value)) or re.fullmatch(r"\-?[0-9]+\b", str(identifier_value)):
          if type(identifier_value) == int or type(identifier_value): 
              it = str(identifier_value)
          else:
              # TODO: Show this error in console
              raise ValueError(f"Invalid value for conversion to YARN: {identifier_value}")
        # NOOB TO YARN
        elif identifier_value == None: 
          it = ""
        elif type(identifier_value) == str: 
          it = identifier_value

      print(f"The value of it is {it}")
      self.symbol_table["IT"] = it

  def gimmeh(self, input):
    var_name = input[1].value

    input_value, ok = QInputDialog.getText(self.ui, 'Input', f'Enter a value for {var_name}:')

    if ok and input_value:
      self.symbol_table[var_name] = input_value

  '''
  Class: Statement, Value: None
    Class: Print Statement, Value: None
      Class: Output Keyword, Value: None
      Class: Op Argument, Value: None
        Class: Identifier, Value: sum

  Class: Statement, Value: None
    Class: Print Statement, Value: None
      Class: Output Keyword, Value: None
      Class: Op Argument, Value: None
        Class: String Delimiter, Value: None
        Class: YARN Literal, Value: declarations
        Class: String Delimiter, Value: None
  '''

  def visible(self, op_arg):
    print(op_arg.classification)
    op_class = op_arg.children[0]
    print(op_class.classification)
    if op_class.classification == "Identifier":
      value = self.symbol_table[op_class.value]
      print(value)
      self.ui.print_in_console(str(value))
    elif op_class.classification == "String Delimiter":
      value = op_arg.children[1].value
      self.ui.print_in_console(str(value))


    else:
      pass

