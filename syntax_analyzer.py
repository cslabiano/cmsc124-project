from node import Node

# lexeme = lexemes[0][0] | current_lexeme[0]
# classification = lexemes[0][1] | current_lexeme[1]

line = 0

class Syntax_Analyzer:

  def __init__(self, lexemes):
    self.lexemes = lexemes
    self.current_lexeme = lexemes[0]

  # --------------------------------------------------------------------------------------------------
  # starts the syntax analyzer and returns the parse tree
  # --------------------------------------------------------------------------------------------------
  def analyze(self):
    global line
    line = 0
    try:
      parse_tree = self.program()  # Start the program parsing
      return parse_tree
    except SyntaxError as e:
      return str(e)

  # --------------------------------------------------------------------------------------------------
  # pops lexeme from the list 
  # --------------------------------------------------------------------------------------------------
  def check(self, type):
    global line
    line += 1
    if type == self.current_lexeme[1]:
        self.lexemes.pop(0)
        if self.lexemes:
            self.current_lexeme = self.lexemes[0]
    else:
        raise SyntaxError(f'Syntax Error on line {line}: Expected {type}, but found {self.current_lexeme[1]}')

  # ==============================================================
  # dito kayo magdagdag ng other methods (production rules)
  # ==============================================================

  # ======================================================================
  # <start_statement> ::= <data_section> <linebreak> <statement> | <statement>
  # ======================================================================
  def start_statement(self):
    children = []

    # Statement
    children.append(self.statement())

    return Node(None, 'Start Statement', children=children)

  # ======================================================================
  # <statement> ::= 
  # ======================================================================
  def statement(self):
    children = []

    # expression
    if 'Expression' in self.current_lexeme[1]:
      children.append(self.expression())

  def expression(self):
    children = []

    if self.current_lexeme[1] in {'Addition Expression', 'Subtraction Expression', 'Multiplication Expression', 'Division Expression', 'Modulo Expression'}:
      # TODO: Arithmetic
      pass
    # Boolean expression
    elif self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression', 'Not Expression', 'Infinite Or Expression', 'Infinite And Expression'}:
      children.append(self.boolean())
    # Equality expression
    elif self.current_lexeme[1] in {'Equality Operator Expression', 'Inequality Operator Expression'}:
      children.append(self.comparison())
    
    return Node(None, 'Expression', children=children) 

  # ======================================================================
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # ======================================================================
  def op_argument(self):
    children = []

    # Literals
    if self.current_lexeme[1] in {'NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal', 'TYPE Literal'}:
        children.append(Node(self.current_lexeme[1]))
        self.check(self.current_lexeme[1])

    # Variables
    elif self.current_lexeme[1] == "Identifier":
        children.append(Node("Identifier"))
        self.check("Identifier")

    elif 'Expression' in self.current_lexeme[1]:
      children.append(self.expression())

    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')
    return Node(None, "Op Argument", children=children)

  def infinite_expression(self):
    children = []

    if self.current_lexeme[1] in {'Addition Expression', 'Subtraction Expression', 'Multiplication Expression', 'Division Expression', 'Modulo Expression'}:
      # TODO: Arithmetic
      pass
    # Boolean expression
    elif self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression', 'Not Expression'}:
      children.append(self.boolean())
    # Equality expression
    elif self.current_lexeme[1] in {'Equality Operator Expression', 'Inequality Operator Expression'}:
      children.append(self.comparison())

  # ======================================================================
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # ======================================================================
  def infinite_op_argument(self):
    children = []

    # Literals
    if self.current_lexeme[1] in {'NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal', 'TYPE Literal'}:
        children.append(Node(self.current_lexeme[1]))
        self.check(self.current_lexeme[1])

    # Variables
    elif self.current_lexeme[1] == "Identifier":
        children.append(Node("Identifier"))
        self.check("Identifier")

    elif 'Expression' in self.current_lexeme[1]: 
      children.append(self.infinite_expression()) 

    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')

    return Node(None, "Infinite Op Argument", children=children)

  # ======================================================================
  # <boolean> ::= <fixed_boolean> | <infinite_boolean>
  # Booleans can either be a fixed boolean or an infinite boolean 
  # ======================================================================
  def boolean(self):
    children = []

    if self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression', 'Not Expression'}:
        children.append(self.fixed_boolean())
    elif self.current_lexeme[1] in {'Infinite Or Expression', 'Infinite And Expression'}:
        children.append(self.infinite_boolean())

    return Node(None, "Boolean", children=children)
  
  # ======================================================================
  # <fixed_boolean> ::= BOTH OF <op_argument> AN <op_argument> 
  #                     | EITHER OF <op_argument> AN <op_argument>  
  #                     | WON OF <op_argument> AN <op_argument> 
  #                     | NOT <op_argument>
  # 
  # All fixed booleans must follow this format (except for not which only has 1 <op_argument>):   
  # <boolean_expression> <op_argument> <operation_delimiter> <op_argument> 
  # ======================================================================
  def fixed_boolean(self):
    children = []

    if self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression'}:
      self.check(self.current_lexeme[1])
      children.append(Node(self.current_lexeme[1]))
      
      children.append(self.op_argument())

      self.check("Operation Delimiter")
      children.append(Node("Operation Delimiter"))

      children.append(self.op_argument())
    
    elif self.current_lexeme[1] == 'Not Expression':
      self.check("Not Expression")
      children.append(Node("Not Expression"))

      children.append(self.op_argument())

    return Node(None, "Fixed Boolean", children=children)

  
    # ======================================================================
  
  # ======================================================================
  # <infinite_argument> ::= <op_argument> AN <infinite_argument> | <op_argument>
  # ======================================================================
  def infinite_argument(self):
    children = []

    children.append(self.infinite_op_argument())

    # If there is an 'AN', it means there are more arguments
    if self.current_lexeme[1] == "Operation Delimiter":
        self.check("Operation Delimiter")
        children.append(Node("Operation Delimiter"))

        # Recursive call to check if there are more arguments
        children.append(self.infinite_argument())

    return Node(None, "Infinite Argument", children=children)

  # <infinite_boolean> ::= ALL OF <infinite_argument> MKAY
  #                       | ANY OF <infinite_argument> MKAY
  # 
  # All infinite booleans must follow this format
  # <boolean_expression> <infinite_argument> <function_call_delimiter>  
  # TODO: MKAY is currently a Function Call Delimiter only
  # ======================================================================
  def infinite_boolean(self):
    children = []

    # ALL OF or ANY OF
    if self.current_lexeme[1] == "Infinite And Expression":
        self.check("Infinite And Expression")
        children.append(Node("Infinite And Expression"))
    elif self.current_lexeme[1] == "Infinite Or":
        self.check("Infinite Or Expression")
        children.append(Node("Infinite Or Expression"))

    children.append(self.infinite_argument())

    # Check 'MKAY'
    if self.current_lexeme[1] == "Function Call Delimiter":
        self.check("Function Call Delimiter")
        children.append(Node("Function Call Delimiter"))

    return Node(None, "Infinite Boolean", children=children)
  
    # ======================================================================
  
  # <relational_operator ::= BIGGR OF <op_argument> AN <op_argument>
  #                          | DIFFRINT OF <op_argument> AN <op_argument> 
  # can either be a max or a min
  def relational_operator(self):
    children = []

    if self.current_lexeme[1] == 'Max Expression':
      self.check('Max Expression')
      children.append(Node('Max Expression'))

      children.append(self.op_argument())

      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))

      children.append(self.op_argument())
    elif self.current_lexeme[1] == 'Min Expression': 
      self.check('Min Expression')
      children.append(Node('Min Expression'))

      children.append(self.op_argument())

      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))

      children.append(self.op_argument())

    return Node(None, 'Relational Operator', children=children)
  
  # <comparison> ::= BOTH SAEM <op_argument> AN <op_argument>
  # | DIFFRINT <op_argument> AN <op_argument>
  # | BOTH SAEM <op_argument> AN <relational_operator>
  # | DIFFRINT <op_argument> AN <relational_operator>
  # comparison can either end in an argument or a relational operator
  # ======================================================================
  def comparison(self):
    children = []
    
    if self.current_lexeme[1] == 'Equality Operator Expression':
      self.check('Equality Operator Expression')
      children.append(Node('Equality Operator Expression'))
       
      children.append(self.op_argument())
      
      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))

      if self.current_lexeme[1] in {'Max Expression', 'Min Expresion'}:
        children.append(self.relational_operator())
      else:
        children.append(self.op_argument())

    elif self.current_lexeme[1] == 'Inequality Operator Expression':
      self.check('Inequality Operator Expression')
      children.append(Node('Inequality Operator'))

      children.append(self.op_argument())
      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))
      
      if self.current_lexeme[1] in {'Max Expression', 'Min Expression'}:
        children.append(self.relational_operator())
      else:
        children.append(self.op_argument())
    
    return Node(None, 'Equality Comparison', children=children)

  # --------------------------------------------------------------------------------------------------
  # <program> ::== HAI <linebreak> <start_statement> <linebreak> KTHXBYE
  # --------------------------------------------------------------------------------------------------
  def program(self):
    children = []

    # check if there are comments before HAI
    if self.current_lexeme[1] == "Multiline Comment Start":
      children.append(self.multiline_comment())
    elif self.current_lexeme[1] == "Comment Delimiter":
      children.append(self.comment())

    # program must start with HAI
    self.check("Program Start")
    children.append(Node("Program Start"))

    # linebreak?

    # calls start_statement abstraction
    if self.current_lexeme[1] != "Program End":
      children.append(self.start_statement())

    # linebreak?

    # program must end with KTHXBYE
    self.check("Program End")
    children.append(Node("Program End"))

    return Node(None, "Program", children = children)