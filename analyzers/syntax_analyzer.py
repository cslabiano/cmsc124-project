class Node:
  def __init__(self, type, value = None, children = None):
    self.value = value
    self.type = type
    self.children = children

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
      parse_tree = self.program()  # start the program parsing
      return parse_tree
    except SyntaxError as e:
      return str(e)

  # --------------------------------------------------------------------------------------------------
  # checks if the current lexeme's classification matches the expected classification 
  # --------------------------------------------------------------------------------------------------
  def check(self, type):
      
    print("lexeme: ", self.current_lexeme[0], "expected: ", type, "current: ", self.current_lexeme[1])
    if type == self.current_lexeme[1]:
      self.lexemes.pop(0)
      if self.lexemes:
        self.current_lexeme = self.lexemes[0]
    else:
      raise SyntaxError(f'Syntax Error on line {line}: Expected {type}, but found {self.current_lexeme[1]}')
    
  # --------------------------------------------------------------------------------------------------
  # <comment> ::= <statement> <comment_inline> | <comment_long> 
  # --------------------------------------------------------------------------------------------------
  def comment(self):
    children = []

    if self.current_lexeme[1] == "Multiline Comment Start":
      self.check("Multiline Comment Start")
      children.append(Node("Multiline Comment Start"))

      while self.current_lexeme[1] != "Multiline Comment End":
        self.check("Comment")
        children.append(Node("Comment"))
      
      self.check("Multiline Comment End")
      children.append(Node("Multiline Comment End"))
    
    if self.current_lexeme[1] == "Comment Delimiter":
      self.check("Comment Delimiter")
      children.append(Node("Comment Delimiter"))

      self.check("Comment")
      children.append("Comment")
    
    return Node(None, "Comment", children = children)

  # --------------------------------------------------------------------------------------------------
  # <start_statement> ::= <data_section> <linebreak> <statement> | <statement>
  # --------------------------------------------------------------------------------------------------

  def identifier(self):
    children = []
    self.check('Identifier')
    children.append(Node('Identifier'))

    return Node(None, 'Identifier', children=children)

  def variable(self):
    children = []

    self.check('Variable Declaration')
    children.append(Node('Variable Declaration'))

    children.append(self.identifier())

    if self.current_lexeme[1] == 'Variable Assignment':
      self.check('Variable Assignment')
      children.append(Node('Variable Assignment'))

      children.append(self.op_argument())
  
    return Node(None, 'Variable', children=children)
  
  def data_section(self):
    children = []

    if self.current_lexeme[1] == 'Data section Delimiter':
      self.check('Data section Delimiter')
      children.append(Node('Data section Delimiter'))

    while self.current_lexeme[1] != "Data section Delimiter":
      if self.current_lexeme[1] in {"Multiline Comment Start", "Comment Delimiter"}:
        # checks if there are comments within the data section
        children.append(self.comment())
      children.append(self.variable())

    self.check("Data section Delimiter")
    children.append(Node("Data section Delimiter"))
    
    return Node(None, "Data Section", children=children)

  def start_statement(self):
    children = []

    if self.current_lexeme[1] == 'Data section Delimiter':
      children.append(self.data_section())

    while self.current_lexeme[1] != 'Program End':
      children.append(self.statement())

    return Node(None, 'Start Statement', children=children)

  # --------------------------------------------------------------------------------------------------
  # <statement> ::= 
  # --------------------------------------------------------------------------------------------------
  def statement(self):
    children = []

    currentLex = self.current_lexeme[1]

    # expression
    if 'Expression' in currentLex:
      children.append(self.expression())
    # loop
    elif currentLex == 'Loop Delimiter':
      children.append(self.loop())
    # comment
    elif currentLex in {"Multiline Comment Start", "Comment Delimiter"}:
      children.append(self.comment())
    # print
    elif currentLex == 'Output Keyword':
      children.append(self.print_fn())
    # input
    elif currentLex == 'Input Keyword':
      children.append(self.input())
    # typecast
    elif currentLex == 'Typecast Delimiter':
      children.append(self.typecast())
    # could be a typecast or an assignment?
    elif currentLex == 'Identifier':
      children.append(self.typecast())
    elif currentLex == "String Concatenation":
      children.append(self.concatenation())

    return Node(None, 'Statement', children=children)
  
  def expression(self):
    children = []

    # Arithmetic
    if self.current_lexeme[1] in {'Addition Expression', 'Subtraction Expression', 'Multiplication Expression', 'Division Expression', 'Modulo Expression', 'Max Expression', 'Min Expression'}:
      children.append(self.arithmetic())
    # Boolean expression
    elif self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression', 'Not Expression', 'Infinite Or Expression', 'Infinite And Expression'}:
      children.append(self.boolean())
    # Equality expression
    elif self.current_lexeme[1] in {'Equality Operator Expression', 'Inequality Operator Expression'}:
      children.append(self.comparison())
    
    return Node(None, 'Expression', children=children) 

  def arithmetic(self):
    children = []

    if self.current_lexeme[1] in {'Addition Expression', 'Subtraction Expression', 'Multiplication Expression', 'Division Expression', 'Modulo Expression', 'Max Expression', 'Min Expression'}:
      self.check(self.current_lexeme[1])
      children.append(Node(self.current_lexeme[1]))

      children.append(self.op_argument())

      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))

      children.append(self.op_argument())

    return Node(None, 'Arithmetic Expression', children=children)

  # --------------------------------------------------------------------------------------------------
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # --------------------------------------------------------------------------------------------------
  def op_argument(self):
    children = []

    # Literals
    if self.current_lexeme[1] in {'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'TYPE Literal'}:
        children.append(Node(self.current_lexeme[1]))
        self.check(self.current_lexeme[1])
    elif self.current_lexeme[1] == 'String Delimiter':
      children.append(Node('String Delimiter'))
      self.check('String Delimiter')

      self.check('YARN Literal')
      children.append(Node('Yarn Literal'))

      self.check('String Delimiter')
      children.append(Node('String Delimiter'))
    # Variables
    elif self.current_lexeme[1] == "Identifier":
      children.append(self.identifier())

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

  # --------------------------------------------------------------------------------------------------
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # --------------------------------------------------------------------------------------------------
  def infinite_op_argument(self):
    children = []

    # Literals
    if self.current_lexeme[1] in {'NUMBR Literal', 'NUMBAR Literal', 'YARN Literal', 'TROOF Literal', 'TYPE Literal'}:
        children.append(Node(self.current_lexeme[1]))
        self.check(self.current_lexeme[1])

    # Variables
    elif self.current_lexeme[1] == "Identifier":
      children.append(self.identifier())

    elif 'Expression' in self.current_lexeme[1]: 
      children.append(self.infinite_expression()) 

    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')

    return Node(None, "Infinite Op Argument", children=children)

  # --------------------------------------------------------------------------------------------------
  # <boolean> ::= <fixed_boolean> | <infinite_boolean>
  # Booleans can either be a fixed boolean or an infinite boolean 
  # --------------------------------------------------------------------------------------------------
  def boolean(self):
    children = []

    if self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression', 'Not Expression'}:
        children.append(self.fixed_boolean())
    elif self.current_lexeme[1] in {'Infinite Or Expression', 'Infinite And Expression'}:
        children.append(self.infinite_boolean())

    return Node(None, "Boolean", children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <fixed_boolean> ::= BOTH OF <op_argument> AN <op_argument> 
  #                     | EITHER OF <op_argument> AN <op_argument>  
  #                     | WON OF <op_argument> AN <op_argument> 
  #                     | NOT <op_argument>
  # 
  # All fixed booleans must follow this format (except for not which only has 1 <op_argument>):   
  # <boolean_expression> <op_argument> <operation_delimiter> <op_argument> 
  # --------------------------------------------------------------------------------------------------
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
  
  # --------------------------------------------------------------------------------------------------
  # <infinite_argument> ::= <op_argument> AN <infinite_argument> | <op_argument>
  # --------------------------------------------------------------------------------------------------
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

  # --------------------------------------------------------------------------------------------------
  # <infinite_boolean> ::= ALL OF <infinite_argument> MKAY
  #                       | ANY OF <infinite_argument> MKAY
  # 
  # All infinite booleans must follow this format
  # <boolean_expression> <infinite_argument> <function_call_delimiter>  
  # TODO: MKAY is currently a Function Call Delimiter only
  # --------------------------------------------------------------------------------------------------
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
  
  # --------------------------------------------------------------------------------------------------
  # <relational_operator ::= BIGGR OF <op_argument> AN <op_argument>
  #                          | DIFFRINT OF <op_argument> AN <op_argument> 
  # can either be a max or a min
  # --------------------------------------------------------------------------------------------------
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
  
  # --------------------------------------------------------------------------------------------------
  # <comparison> ::= BOTH SAEM <op_argument> AN <op_argument>
  # | DIFFRINT <op_argument> AN <op_argument>
  # | BOTH SAEM <op_argument> AN <relational_operator>
  # | DIFFRINT <op_argument> AN <relational_operator>
  # comparison can either end in an argument or a relational operator
  # --------------------------------------------------------------------------------------------------
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

  def inc_dec(self):
    children = []

    if self.current_lexeme[1] == 'Loop Increment':
      self.check('Loop Increment')
      children.append(Node('Loop Increment'))
    elif self.current_lexeme[1] == 'Loop Decrement':
      self.check('Loop Decrement')
      children.append(Node('Loop Decrement'))

    return Node(None, 'Increment/Decrement', children=children)

  def termination(self):
    children = []

    self.check('Loop Condition')
    children.append(Node('Loop Condition'))

    children.append(self.expression())

    return Node(None, 'Loop Condition', children=children)

  def loop(self):
    children = []
    
    self.check('Loop Delimiter')
    children.append(Node('Loop Delimiter'))

    children.append(self.identifier())

    children.append(self.inc_dec())

    self.check('Condition Delimiter')
    children.append(Node('Condition Delimiter'))

    children.append(self.identifier())

    children.append(self.termination())

    while self.current_lexeme[1] != 'Loop Delimiter':
      children.append(self.statement())

    self.check('Loop Delimiter')
    children.append(Node('Loop Delimiter'))

    children.append(self.identifier())

    return Node(None, 'Loop', children=children) 

  def print_multiple(self):
    children = []
    self.check('Print Concatenation')
    children.append(Node('Print Concatenation'))

    children.append(self.op_argument())

    if self.current_lexeme[1] == 'Print Concatenation':
      children.append(self.print_multiple())

    return Node(None, 'Print Multiple', children=children)
  
  def print_fn(self):
    children = []

    self.check('Output Keyword')
    children.append(Node('Output Keyword'))

    children.append(self.op_argument())

    if self.current_lexeme[1] == 'Print Concatenation':
      children.append(self.print_multiple())
    
    return Node(None, "Print Statement", children=children)

  def input(self):
    children = []

    self.check('Input Keyword')
    children.append(Node('Input Keyword'))

    children.append(self.identifier())

    return Node(None, 'Input Keyword', children=children)

  def typecast(self):
    children = []

    # Explicit typecast
    if self.current_lexeme[1] == 'Typecast Delimiter':
      children.append(self.explicit_typecast())
    
    # Recasting
    elif self.current_lexeme[1] == 'Identifier':
      children.append(self.recasting())

    return Node(None, 'Typecast', children=children)

  def explicit_typecast(self):
    children = []

    self.check('Typecast Delimiter')
    children.append(Node('Typecast Delimiter'))

    children.append(self.identifier())

    if self.current_lexeme[1] == 'Typecast Keyword':
      self.check('Typecast Keyword')
      children.append(Node('Typecast Keyword'))

    self.check('TYPE Literal')
    children.append(Node('TYPE Literal'))

    return Node(None, 'Explicit Typecast', children=children)

  def recasting(self):
    children = []

    children.append(self.identifier())
    if self.current_lexeme[1] == 'Typecast Keyword':
      self.check('Typecast Keyword')
      children.append('Typecast Keyword')

      self.check('TYPE Literal')
      children.append('TYPE Literal')
      
    elif self.current_lexeme[1] == 'Assignment':
      self.check('Assignment')
      children.append(Node('Assignment'))

      if self.current_lexeme[1] == 'Typecast Delimiter':
        children.append(self.explicit_typecast())
      else:
        children.append(self.op_argument())

    return Node(None, 'Recasting', children=children)

  # --------------------------------------------------------------------------------------------------
  # <concatenation> ::= SMOOSH <op_argument> <an_op_argument>
  # --------------------------------------------------------------------------------------------------
  def concatenation(self):
    children = []

    self.check("String Concatenation")
    children.append(Node("String Concatenation"))

    children.append(self.op_argument())

    while self.current_lexeme[1] == "Operation Delimiter":
      self.check("Operation Delimiter")
      children.append(Node("Operation Delimiter"))
      children.append(self.op_argument())

    return Node(None, "String Concatenation", children = children)

  # --------------------------------------------------------------------------------------------------
  # <program> ::== HAI <linebreak> <start_statement> <linebreak> KTHXBYE
  # --------------------------------------------------------------------------------------------------
  def program(self):
    children = []

    # check if there are comments before HAI
    while self.current_lexeme[1] == "Multiline Comment Start" or self.current_lexeme[1] == "Comment Delimiter":
      children.append(self.comment())

    # program must start with HAI
    self.check("Program Start")
    children.append(Node("Program Start"))

    # calls start_statement abstraction
    if self.current_lexeme[1] != "Program End":
      children.append(self.start_statement())

    # program must end with KTHXBYE
    self.check("Program End")
    children.append(Node("Program End"))

    # check if there are comments before HAI
    while self.current_lexeme[1] == "Multiline Comment Start" or self.current_lexeme[1] == "Comment Delimiter":
      children.append(self.comment())

    return Node(None, "Program", children = children)
