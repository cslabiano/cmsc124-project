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
              self.process_statement(child)
    return self.symbol_table

  def process_statement(self, child):
    type = child.classification
    if type == "Expression":
      # self.expression(child.children)
      for expr in child.children:
        self.symbol_table["IT"] = self.expression(expr)
    elif type == 'Typecast': # Could be a typecast or an assignment
      typecast_type = child.children[0].classification
      if typecast_type == 'Recasting':
        self.assignment(child.children[0])
      elif typecast_type == 'Explicit Typecast':
        self.typecast(child.children[0])
    elif type == "Identifier":
      # print(child.children[0].classification)
      if child.children[0].classification == "Switch Case":
        self.switch_case(child)
    elif type == 'If-Then':
      self.if_then(child.children)
    # elif type == "Switch Case":
    #   self.switch_case(child.children)
    elif type == "Print Statement":
      result = self.visible(child.children)
      self.ui.print_in_console(result)
    elif type == "Input Keyword":
      self.gimmeh(child.children)
    elif type == "Loop":
      self.loop(child.children)
    elif type == "String Concatenation":
      value = self.smoosh(child.children)
      self.symbol_table["IT"] = value

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

    # If its a boolean expression, extract child 
    if op_type == 'Boolean':
      op_type = operation.children[0].classification # Get {} Expression class
      op_args = operation.children[0].children

      if op_type in {'Infinite And Expression', 'Infinite Or Expression'}:
        print("ITS AN INFINITE EXPRESSION")
        infinite_args = []
        # For all operands of the infinite expression, push onto list
        for arg in op_args:
          if arg.classification != 'Operation Delimiter':
            # If string delimiter encountered, pass next child
            if arg.children[0].classification == 'String Delimiter':
              infinite_args.append(self.to_troof(self.evaluate_operand(arg.children[1])))
            else:
              infinite_args.append(self.to_troof(self.evaluate_operand(arg.children[0])))
        print(infinite_args)

    # Just a checker since infinite expressions follow a different format
    if op_type not in {'Infinite And Expression', 'Infinite Or Expression'}:
      # Use value to access the value of the operand
      # Use classification to access if identifier or literal
      if op_args[0].children[0].classification == 'String Delimiter':
        operand1 = self.evaluate_operand(op_args[0].children[1])
      else: 
        operand1 = self.evaluate_operand(op_args[0].children[0])

      # A Not expression can only have one operand
      if op_type != 'Not Expression':
        if op_args[2].children[0].classification == 'String Delimiter':
          operand2 = self.evaluate_operand(op_args[2].children[1])
        else:
          operand2 = self.evaluate_operand(op_args[2].children[0])

    if op_type == "Addition Expression":
      print(operand1 + operand2)
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
      return operand1 if float(operand1) > float(operand2) else operand2
    elif op_type == 'Min Expression':
      return operand1 if float(operand1) < float(operand2) else operand2
    elif op_type == 'And Expression':
      return self.to_troof(operand1) and self.to_troof(operand2)
    elif op_type == 'Or Expression':
      return self.to_troof(operand1) or self.to_troof(operand2)
    elif op_type == 'Xor Expression':
      return self.to_troof(operand1) ^ self.to_troof(operand2)
    elif op_type == 'Not Expression':
      return not self.to_troof(operand1)
    elif op_type == 'Infinite Or Expression':
      return any(infinite_args) # Returns true if one is True, false if all are false
    elif op_type == 'Infinite And Expression':
      return all(infinite_args)
    
  '''
  typecasts an operand to a troof
  '''
  def to_troof(self, operand):
    if operand == "":
        return False
    try:
        if float(operand) == 0.0:
            return False
    except ValueError:
        pass
    if operand == False:
        return False
    return True

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

    if classification == 'YARN Literal':
        if re.fullmatch(r"\-?\d+", value):  # for integer
          return int(value)
        elif re.fullmatch(r"\-?\d+\.\d+", value):  # for float
          return float(value)
        else:
          print(value)
          return str(value)
      # return str(value)
    elif classification == 'Identifier':
      if value not in self.symbol_table:
        raise NameError(f"Identifier '{value}' is not initialized.")
      
      symbol_value = self.symbol_table[value]

      if isinstance(symbol_value, str) and str(symbol_value).isdigit():
        # typecast the value if it's a numeric string
        if re.fullmatch(r"\-?\d+", symbol_value):  # for integer
          return int(symbol_value)
        elif re.fullmatch(r"\-?\d+\.\d+", symbol_value):  # for float
          return float(symbol_value)
      return symbol_value
    
    elif classification == 'NUMBR Literal':
      return int(value)
    elif classification == 'NUMBAR Literal':
      return float(value)
    elif classification == 'TROOF Literal':
      return True if value == "WIN" else False
    elif classification == 'Expression':
      return self.expression(operand.children[0])
    else:
      raise TypeError(f"Unsupported operand classification: {classification}")

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
    assignment_type = node.classification
    
    if assignment_type == 'Recasting':
      identifier = node.children[0].value
      new_value = self.evaluate_operand(node.children[2].children[0])
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

  def if_then(self, node):

    print("are u here?")
    # takes the value of IT
    it_value = self.symbol_table["IT"]
    # check if IT is WIN or FAIL
    condition = self.is_true(it_value)
    print(condition)
    for child in node[1:]:

      # END IF FOUND OIC
      if child.classification == "Control Flow Delimiter End":
        break

      # IF CLAUSE
      elif child.classification == "If Clause" and condition:
        if_clause = child
        for statement in if_clause.children[1:]:
          for child_statement in statement.children:
            self.process_statement(child_statement)
      
      # ELSE IF CLAUSE (checks the expression if true or false)
      elif child.classification == "Else-if Clause" and self.is_true(self.expression(child.children[1].children[0])):
        else_if_clause = child
        for statement in else_if_clause.children[2:]:
          for child_statement in statement.children:
            self.process_statement(child_statement)

      # ELSE CLAUSE (if none of the clauses is true)
      elif child.classification == "Else Clause":
        else_clause = child
        for statement in else_clause.children[1:]:
          for child_statement in statement.children:
            self.process_statement(child_statement)
  
  def switch_case(self, node):

    # it_value = self.symbol_table["IT"]
    comp_value = self.symbol_table[node.value]

    sw_case = node.children

    for child in sw_case[0].children[1:]:

      if child.classification == "Control Flow Delimiter End":
        break
      
      elif child.classification == "Case Block" and self.is_it_equal(comp_value, child):
        case_block = child
        start_idx = 2
        if case_block.children[start_idx].classification == "String Delimiter":
          start_idx = 4
        else:
          start_idx = 2
        for statement in case_block.children[start_idx:]:
          for child_statement in statement.children:
            self.process_statement(child_statement)
        break
      
      elif child.classification == "Case Default Block":
        case_def_block = child
        for statement in case_def_block.children[1:]:
          for child_statement in statement.children:
            self.process_statement(child_statement)
        break

  # checks if an expression is true (used for if-clause)
  def is_true(self, it_value):

    if it_value is None or it_value == "":
      return False
    elif type(it_value) == bool:
      return it_value
    elif type(it_value) == int or type(it_value) == float:
      if it_value != 0:
        return True
      else:
        return False
    elif type(it_value) == str:
      return True
    else:
        # error checking
        raise ValueError(f"Unsupported type for truthiness check: {type(it_value)}")

  def is_it_equal(self, comp_value, literal):
    # print("literal:", type(literal))
    # print("it_value:", type(it_value))
    # print("literal_class:", literal.classification)
    # print(it_value == literal)

    if literal.children[1].classification in {'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'TYPE Literal'}:
      if str(literal.children[1].value) == str(comp_value):
        return True
    
    elif literal.children[1].classification == "String Delimiter":
      if literal.children[2].classification == "YARN Literal":
        if str(literal.children[2].value) == str(comp_value):
          return True
        
    else:
      return False

  # --------------------------------------------------------------------------------------------------
  # creats a pop up input dialog using a pyqt5 widget, QInputDialog, to ask for input
  # stores the input in the symbol table as yarn (string)
  # --------------------------------------------------------------------------------------------------
  def gimmeh(self, input):
    var_name = input[1].value
    input_value, ok = QInputDialog.getText(self.ui, 'Input', f'Enter a value for {var_name}:')

    if ok and input_value:
      self.symbol_table[var_name] = input_value

  # --------------------------------------------------------------------------------------------------
  # function for printing in the console, supports concatenation
  # --------------------------------------------------------------------------------------------------
  def visible(self, op_arg):
    result = ""
    for child in op_arg:
      if child.classification == "Op Argument":
        result += self.concatenate_ops(child)
      elif child.classification == "Print Multiple":
        for term in child.children:
          if term.classification == "Op Argument":
            result += self.concatenate_ops(term)
          elif term.classification == "Print Multiple":
            result += self.visible(term.children)
    return result

  # --------------------------------------------------------------------------------------------------
  # function for returning the values needed for concatenation
  # --------------------------------------------------------------------------------------------------
  def concatenate_ops(self, op_arg):
    op_class = op_arg.children[0]
    if op_class.classification == "Identifier":
      value = self.symbol_table[op_class.value]
      return str(value)
    elif op_class.classification == "String Delimiter":
      value = op_arg.children[1].value
      return str(value)
    elif op_class.classification == "Expression":
      value = self.expression(op_class.children[0])
      self.symbol_table["IT"] = value  
      return str(value)
    elif op_class.classification == "String Concatenation":
      value = self.smoosh(op_class.children)
      self.symbol_table["IT"] = value  
      return str(value)
    else:
      return str(op_arg.children[0].value)

  # --------------------------------------------------------------------------------------------------
  # function for smoosh
  # parameter should be the list of children of String Concatenation node
  # --------------------------------------------------------------------------------------------------
  def smoosh(self, op_arg):
    result = ""
    print(op_arg)
    for child in op_arg:
      if child.classification == "Op Argument":
        result += self.concatenate_ops(child)
    return result

  # --------------------------------------------------------------------------------------------------
  # function for checking the equality for the loop conditions
  # --------------------------------------------------------------------------------------------------
  def equality(self, args):
    op_args = args.children
    op_type = op_args[0].classification

    op1 = self.evaluate_operand(op_args[1].children[0])
    op2 = self.evaluate_operand(op_args[3].children[0])

    print(op_type, op1, op2)
    if type(op1) != type(op2):
      op1, op2 = float(op1), float(op2)

    if op_type == 'Equality Operator Expression':
      return True if op1 == op2 else False
    elif op_type == 'Inequality Operator Expression':
      return True if op1 != op2 else False

  # --------------------------------------------------------------------------------------------------
  # implements the loop function
  # --------------------------------------------------------------------------------------------------
  def loop(self, loop_children):
    loop_cond = None
    inc = loop_children[2].children[0].classification
    var = loop_children[4].value

    # check if the value needs typecasting
    if isinstance(self.symbol_table[var], str) and str(self.symbol_table[var]).isdigit():
      self.symbol_table[var] = float(val)
    val = self.symbol_table[var]
  
    # check if the loop condition is WILE or TIL
    if loop_children[5].children[0].value == "WILE":
      loop_cond = True
    elif loop_children[5].children[0].value == "TIL":
      loop_cond = False

    while True:
      expr = loop_children[5].children[1].children[0]
      expr_bool = self.equality(expr)

      if expr_bool is not loop_cond:
        break

      statement = loop_children[6].children[0]
      self.process_statement(statement)

      if inc == "Loop Increment":
        val += 1
      elif inc == "Loop Decrement":
        val -= 1
      self.symbol_table[var] = val

      print("expr_bool: ", expr_bool) # print for debugging 

  