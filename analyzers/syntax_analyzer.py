class Node:
  def __init__(self, classification, value = None, children = None):
    self.value = value
    self.classification = classification
    self.children = children

# print tree for checking and debugging
def traverse_tree(node, level=0):
  # print the current node's classification and value
  indent = "  " * level  # indentation to show tree hierarchy
  print(f"{indent}Class: {node.classification}, Value: {node.value}")

  # if the node has children, recursively traverse them
  if node.children:
    for child in node.children:
      traverse_tree(child, level + 1)

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
      traverse_tree(parse_tree)
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
      children.append(Node("Comment"))
    
    return Node("Comment", children = children)

  # --------------------------------------------------------------------------------------------------
  # For Identifiers
  # --------------------------------------------------------------------------------------------------
  def identifier(self):
    identifier_value = self.current_lexeme[0]
    self.check('Identifier')
    return Node('Identifier', value=identifier_value)

  # --------------------------------------------------------------------------------------------------
  # <variable> ::= I HAS A variable 
  # | I HAS A variable ITZ <literal> 
  # | I HAS A variable ITZ variable 
  # | I HAS A variable ITZ <expression>
  # | <var> <linebreak> <var>
  # --------------------------------------------------------------------------------------------------
  def variable(self):
    children = []

    self.check('Variable Declaration')
    children.append(Node('Variable Declaration'))

    children.append(self.identifier())

    if self.current_lexeme[1] == 'Variable Assignment':
      self.check('Variable Assignment')
      children.append(Node('Variable Assignment'))

      children.append(self.op_argument())
  
    return Node('Variable', children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <datasection> ::= WAZZUP <linebreak> <var> <linebreak> BUHBYE
  # --------------------------------------------------------------------------------------------------
  def data_section(self):
    children = []

    if self.current_lexeme[1] == 'Data section Delimiter Start':
      self.check('Data section Delimiter Start')
      children.append(Node('Data section Delimiter Start'))

    while self.current_lexeme[1] != "Data section Delimiter End":
      if self.current_lexeme[1] in {"Multiline Comment Start", "Comment Delimiter"}:
        # checks if there are comments within the data section
        children.append(self.comment())
      children.append(self.variable())

    self.check("Data section Delimiter End")
    children.append(Node("Data section Delimiter End"))
    
    return Node("Data Section", children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <start_statement> ::= <data_section> <linebreak> <statement> | <statement>
  # --------------------------------------------------------------------------------------------------
  def start_statement(self):
    children = []

    if self.current_lexeme[1] == 'Data section Delimiter Start':
      children.append(self.data_section())

    max_iter = len(self.lexemes)
    iter_count = 0

    while self.current_lexeme[1] != 'Program End':
      if iter_count >= max_iter:
        raise SyntaxError(
            f"Unexpected end of input or invalid syntax in 'HAI' clause. "
            f"Expected 'Program End', but got '{self.current_lexeme[1]}'"
          )
      children.append(self.statement())
      iter_count += 1

    return Node('Start Statement', children=children)

  # --------------------------------------------------------------------------------------------------
  # <function_return> ::= FOUND YR <expression>
  # --------------------------------------------------------------------------------------------------
  def function_return(self):
    children = []
    self.check('Function Return')
    children.append(Node('Function Return'))

    children.append(self.expression())

    return Node('Function Return', children=children)

  # --------------------------------------------------------------------------------------------------
  # <function_break> ::= GTFO
  # --------------------------------------------------------------------------------------------------
  def function_break(self):
    children = []

    self.check('Function Break')
    children.append(Node('Function Break'))

    return Node('Function Break', children=children)
 
  # --------------------------------------------------------------------------------------------------
  # <function_argument> ::= YR <expression>
  # | <function_argument> AN YR <expression>
  # --------------------------------------------------------------------------------------------------
  def function_argument_call(self):
    children = []

    # YR
    self.check('Condition Delimiter')
    children.append(Node('Condition Delimiter'))

    # expression
    children.append(self.op_argument())

    # While AN
    while self.current_lexeme[1] == 'Operation Delimiter':
      # AN
      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))

      # YR
      self.check('Condition Delimiter')
      children.append(Node('Condition Delimiter'))

      # expression
      children.append(self.op_argument())

    return Node('Function Arguments', children=children)

  # --------------------------------------------------------------------------------------------------
  # <function_call> ::= I IZ function MKAY
  # | I IZ function <fn_argument> MKAY
  # --------------------------------------------------------------------------------------------------
  def function_call(self):
    children = []

    # I IZ
    self.check('Function Call Delimiter Start')
    children.append(Node('Function Call Delimiter Start'))

    # function name
    children.append(self.identifier())

    if self.current_lexeme[1] == 'Condition Delimiter':
      children.append(self.function_argument_call())

    self.check('Function Call Delimiter End')
    children.append(Node('Function Call Delimiter End'))

    return Node('Function Call', children=children)
 
  # --------------------------------------------------------------------------------------------------
  # <statement> ::= <print> 
  # | <comment> 
  # | <var>
  # | <expression> 
  # | <concatenation> 
  # | <input> 
  # | <if_then> 
  # | <switch_case> 
  # | <loop> 
  # | <definition> 
  # | <return>
  # | <assignment>
  # | <typecast>
  # | <break> 
  # | <call> 
  # | <statement> <linebreak> <statement>
  # --------------------------------------------------------------------------------------------------
  def statement(self):
    children = []

    currentLex = self.current_lexeme[1]

    # expression
    if 'Expression' in currentLex:
      children.append(self.expression())
    # loop
    elif currentLex == 'Loop Delimiter Start':
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
    # string concatenation
    elif currentLex == "String Concatenation":
      children.append(self.concatenation())
    # function definition
    elif currentLex == 'Function Delimiter Start':
      children.append(self.function_definition())
    # function return
    elif currentLex == 'Function Return':
      children.append(self.function_return())
    # function break
    elif currentLex == 'Function Break':
      children.append(self.function_break())
    # function call
    elif currentLex == 'Function Call Delimiter Start':
      children.append(self.function_call())
    # control flow if-else
    elif currentLex == "Control Flow Delimiter If-else":
      children.append(self.if_then())
    # control flow switch
    elif currentLex == "Control Flow Delimiter Switch":
      children.append(self.switch_case())

    return Node('Statement', children=children)

  # --------------------------------------------------------------------------------------------------
  # <expression> ::= SUM OF <op_argument> AN <op_argument>
  # | DIFF OF <op_argument> AN <op_argument>
  # | PRODUKT OF <op_argument> AN <op_argument>
  # | QUOSHUNT OF <op_argument> AN <op_argument>
  # | MOD OF <op_argument> AN <op_argument>
  # | BIGGR OF <op_argument> AN <op_argument>
  # | SMALLR OF <op_argument> AN <op_argument>
  # | <boolean>
  # | <comparison>
  # --------------------------------------------------------------------------------------------------
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
    
    return Node('Expression', children=children) 

  def arithmetic(self):
    children = []

    expression_type = self.current_lexeme[1]
    self.check(expression_type)
    # children.append(Node(expression_type))

    children.append(self.op_argument())

    self.check('Operation Delimiter')
    children.append(Node('Operation Delimiter'))

    children.append(self.op_argument())

    return Node(expression_type, children=children)

  # implicit variables?
  def implicit_var(self):
    children = []

    self.check('Implicit Variable')
    children.append(Node('Implicit Variable'))

    return Node('Implicit Variable', children=children)

  # --------------------------------------------------------------------------------------------------
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # --------------------------------------------------------------------------------------------------
  def op_argument(self):
    children = []

    # Literals
    if self.current_lexeme[1] in {'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'TYPE Literal'}:
        children.append(Node(self.current_lexeme[1], value = self.current_lexeme[0]))
        self.check(self.current_lexeme[1])
    elif self.current_lexeme[1] == 'String Delimiter':
        children.append(Node('String Delimiter'))
        self.check('String Delimiter')

        if self.current_lexeme[1] == 'YARN Literal':
            children.append(Node('YARN Literal', value=self.current_lexeme[0]))
            self.check('YARN Literal')

        self.check('String Delimiter')
        children.append(Node('String Delimiter'))
    # Variables
    elif self.current_lexeme[1] == "Identifier":
      children.append(self.identifier())

    elif 'Expression' in self.current_lexeme[1]:
      children.append(self.expression())
    elif self.current_lexeme[1] == 'Implicit Variable':
      children.append(self.implicit_var())
    elif self.current_lexeme[1] == 'String Concatenation':
      children.append(self.concatenation())

    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')
    return Node("Op Argument", children=children)

  # --------------------------------------------------------------------------------------------------
  # <expression> ::= SUM OF <op_argument> AN <op_argument>
  # | DIFF OF <op_argument> AN <op_argument>
  # | PRODUKT OF <op_argument> AN <op_argument>
  # | QUOSHUNT OF <op_argument> AN <op_argument>
  # | MOD OF <op_argument> AN <op_argument>
  # | BIGGR OF <op_argument> AN <op_argument>
  # | SMALLR OF <op_argument> AN <op_argument>
  # | <fixed_boolean>
  # | <comparison>
  # --------------------------------------------------------------------------------------------------
  def infinite_expression(self):
    children = []

    if self.current_lexeme[1] in {'Addition Expression', 'Subtraction Expression', 'Multiplication Expression', 'Division Expression', 'Modulo Expression'}:
      children.append(self.arithmetic())
    # Boolean expression
    elif self.current_lexeme[1] in {'And Expression', 'Or Expression', 'Xor Expression', 'Not Expression'}:
      children.append(self.fixed_boolean())
    # Equality expression
    elif self.current_lexeme[1] in {'Equality Operator Expression', 'Inequality Operator Expression'}:
      children.append(self.comparison())

    return Node('Infinite Expression', children=children)

  # --------------------------------------------------------------------------------------------------
  # <literal> ::= numbr 
  # | numbar 
  # | yarn 
  # | troof
  # --------------------------------------------------------------------------------------------------
  def literal(self):
    children = []

    literal_value = self.current_lexeme[0]

    if self.current_lexeme[1] == 'NUMBAR Literal':
      children.append(Node('NUMBAR Literal', value=literal_value))
      self.check('NUMBAR Literal')
    elif self.current_lexeme[1] == 'NUMBR Literal':
      self.check('NUMBR Literal')
      children.append(Node('NUMBR Literal', value=literal_value))
    elif self.current_lexeme[1] == 'YARN Literal':
      self.check('YARN Literal')
      children.append(Node('YARN Literal', value=literal_value))
    elif self.current_lexeme[1] == 'TROOF Literal':
      self.check('TROOF Literal')
      children.append(Node('TROOF Literal', value=literal_value))
    elif self.current_lexeme[1] == 'TYPE Literal':
      self.check('TYPE Literal')
      children.append(Node('TYPE Literal', value=literal_value))
    
    return Node('Literal', children=children)

  # --------------------------------------------------------------------------------------------------
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # --------------------------------------------------------------------------------------------------
  def infinite_op_argument(self):
    children = []

    # Literals
    if 'Literal' in self.current_lexeme[1]:
      children.append(self.literal())

    # Variables
    elif self.current_lexeme[1] == "Identifier":
      children.append(self.identifier())

    elif 'Expression' in self.current_lexeme[1]: 
      children.append(self.infinite_expression()) 

    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')

    return Node("Infinite Op Argument", children=children)

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

    return Node("Boolean", children=children)
  
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

    return Node("Fixed Boolean", children=children)
  
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

    return Node("Infinite Argument", children=children)

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
    elif self.current_lexeme[1] == "Infinite Or Expression":
        self.check("Infinite Or Expression")
        children.append(Node("Infinite Or Expression"))

    children.append(self.infinite_argument())

    # Check 'MKAY'
    if self.current_lexeme[1] == "Function Call Delimiter End":
        self.check("Function Call Delimiter End")
        children.append(Node("Function Call Delimiter End"))

    return Node("Infinite Boolean", children=children)
  
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

    return Node('Relational Operator', children=children)
  
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
      children.append(Node('Inequality Operator Expression'))

      children.append(self.op_argument())
      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))
      
      if self.current_lexeme[1] in {'Max Expression', 'Min Expression'}:
        children.append(self.relational_operator())
      else:
        children.append(self.op_argument())
    
    return Node('Equality Comparison', children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <if_then> ::= O RLY? <linebreak> <if_clause> <linebreak> <else_clause> <linebreak> OIC
  # | O RLY? <linebreak> <if_clause> <linebreak> <else_if_clause> <linebreak> <else_clause> <linebreak> OIC
  # start with O RLY? and end with OIC
  # --------------------------------------------------------------------------------------------------
  def if_then(self):
    children = []

    if self.current_lexeme[1] == "Control Flow Delimiter If-else":
      self.check("Control Flow Delimiter If-else")
      children.append(Node("Control Flow Delimiter If-else"))

    if self.current_lexeme[1] != "Control Flow Delimiter End":
      children.append(self.if_clause())
    
    while self.current_lexeme[1] == "Else-if Keyword":
      children.append(self.else_if_clause())

    if self.current_lexeme[1] == "Else Keyword":
      children.append(self.else_clause())
    
    self.check("Control Flow Delimiter End")
    children.append(Node("Control Flow Delimiter End"))

    return Node("If-Then", children=children)

  # --------------------------------------------------------------------------------------------------
  # <if_clause> ::= YA RLY <linebreak> <statement>
  # start with YA RLY and has 1 or more statements
  # --------------------------------------------------------------------------------------------------
  def if_clause(self):
    children = []

    if self.current_lexeme[1] == "If Keyword":
      self.check("If Keyword")
      children.append(Node("If Keyword"))

      max_iter = len(self.lexemes)
      iter_count = 0

      while self.current_lexeme[1] not in {"Else-if Keyword", "Else Keyword", "Control Flow Delimiter End"}:
        if iter_count >= max_iter:
          raise SyntaxError(
            f"Unexpected end of input or invalid syntax in 'YA RLY' clause. "
            f"Expected 'Control Flow Delimiter End', but got '{self.current_lexeme[1]}'"
          )
        children.append(self.statement())
        iter_count += 1
    

    return Node("If Clause", children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <else_if_clause> ::= MEBBE <statement>
  # start with MEBBE and statement is in-line
  # --------------------------------------------------------------------------------------------------
  def else_if_clause(self):
    children = []

    if self.current_lexeme[1] == "Else-if Keyword":
      self.check("Else-if Keyword")
      children.append(Node("Else-if Keyword"))

      children.append(self.expression())

      max_iter = len(self.lexemes)
      iter_count = 0

      while self.current_lexeme[1] not in {"Else-if Keyword", "Else Keyword", "Control Flow Delimiter End"}:
        if iter_count >= max_iter:
          raise SyntaxError(
            f"Unexpected end of input or invalid syntax in 'MEBBE' clause. "
            f"Expected 'Control Flow Delimiter End', but got '{self.current_lexeme[1]}'"
          )
        children.append(self.statement())
        iter_count += 1

      # TODO: Ensure that the next statement should be an Else-if Keyword or Else Keyword or Control Flow Delimiter End

    return Node("Else-if Clause", children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <else__clause> ::= NO WAI <linebreak> <statement>
  # start with NO WAI and has 1 more statements
  # --------------------------------------------------------------------------------------------------
  def else_clause(self):
    children = []

    if self.current_lexeme[1] == "Else Keyword":
      self.check("Else Keyword")
      children.append(Node("Else Keyword"))

      max_iter = len(self.lexemes)
      iter_count = 0

      while self.current_lexeme[1] != "Control Flow Delimiter End":
        if iter_count >= max_iter:
          raise SyntaxError(
            f"Unexpected end of input or invalid syntax in 'NO WAI' clause. "
            f"Expected 'Control Flow Delimiter End', but got '{self.current_lexeme[1]}'"
          )
        children.append(self.statement())
        iter_count += 1

    return Node("Else Clause", children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <switch_case> ::= WTF? <linebreak> <case_blocks> <linebreak> OIC
  # start with WTF and end with OIC
  # --------------------------------------------------------------------------------------------------
  def switch_case(self):
    children = []

    if self.current_lexeme[1] == "Control Flow Delimiter Switch":
      self.check("Control Flow Delimiter Switch")
      children.append(Node("Control Flow Delimiter Switch"))
    
    while self.current_lexeme[1] == "Switch-case Keyword":
      children.append(self.case_block())

    if self.current_lexeme[1] == "Switch-case Default":
      children.append(self.case_default())
    
    self.check("Control Flow Delimiter End")
    children.append(Node("Control Flow Delimiter End"))

    return Node("Switch Case", children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <case_block> ::= OMG <literal> <linebreak> <statement> <linebreak> <case_blocks> 
  # | OMG <literal> <linebreak> <statement> 
  # | OMG <literal> <linebreak> <statement> <linebreak> <default_case>
  # --------------------------------------------------------------------------------------------------
  def case_block(self):
    children = []

    if self.current_lexeme[1] == "Switch-case Keyword":
      self.check("Switch-case Keyword")
      children.append(Node("Switch-case Keyword"))

      if self.current_lexeme[1] in {'NUMBR Literal', 'NUMBAR Literal', 'TROOF Literal', 'TYPE Literal'}:
        children.append(Node(self.current_lexeme[1]))
        self.check(self.current_lexeme[1])

      max_iter = len(self.lexemes)
      print(max_iter)
      iter_count = 0

      while self.current_lexeme[1] not in {"Switch-case Keyword", "Switch-case Default", "Control Flow Delimiter End"}:
        print(iter_count)
        if iter_count >= max_iter:
          raise SyntaxError(
            f"Unexpected end of input or invalid syntax in 'OMG' clause. "
            f"Expected 'Control Flow Delimiter End', but got '{self.current_lexeme[1]}'"
          )
        children.append(self.statement())
        iter_count += 1
    

    return Node("Case Block", children=children)

  # --------------------------------------------------------------------------------------------------
  # <case_default> ::= OMGWTF <linebreak> <statement>
  # --------------------------------------------------------------------------------------------------
  def case_default(self):
    children = []

    if self.current_lexeme[1] == "Switch-case Default":
      self.check("Switch-case Default")
      children.append(Node("Switch-case Default"))

      max_iter = len(self.lexemes)
      iter_count = 0

      while self.current_lexeme[1] != "Control Flow Delimiter End":
        if iter_count >= max_iter:
          raise SyntaxError(
            f"Unexpected end of input or invalid syntax in 'OMGWTF' clause. "
            f"Expected 'Control Flow Delimiter End', but got '{self.current_lexeme[1]}'"
          )
        children.append(self.statement())
        iter_count += 1
    

    return Node("Case Default Block", children=children)

  # --------------------------------------------------------------------------------------------------
  # <inc_dec> ::= UPPIN 
  # | NERFIN
  # --------------------------------------------------------------------------------------------------
  def inc_dec(self):
    children = []

    if self.current_lexeme[1] == 'Loop Increment':
      self.check('Loop Increment')
      children.append(Node('Loop Increment'))
    elif self.current_lexeme[1] == 'Loop Decrement':
      self.check('Loop Decrement')
      children.append(Node('Loop Decrement'))

    return Node('Increment/Decrement', children=children)

  # --------------------------------------------------------------------------------------------------
  # <termination> ::= TIL <expression> 
  # | WILE <expression>
  # --------------------------------------------------------------------------------------------------
  def termination(self):
    children = []

    children.append(Node('Loop Condition', value = self.current_lexeme[0]))
    self.check('Loop Condition')

    children.append(self.expression())

    return Node('Loop Condition', children=children)

  # --------------------------------------------------------------------------------------------------
  # <loop> ::= IM IN YR variable <inc_dec> YR variable <termination> <linebreak> <statement> <linebreak> IM OUTTA YR variable
  # --------------------------------------------------------------------------------------------------
  def loop(self):
    children = []
    
    self.check('Loop Delimiter Start')
    children.append(Node('Loop Delimiter Start'))

    children.append(Node('Loop Identifier', value=self.current_lexeme[0]))
    self.check('Identifier')
    # children.append(self.identifier())

    children.append(self.inc_dec())

    self.check('Condition Delimiter')
    children.append(Node('Condition Delimiter'))

    children.append(self.identifier())

    children.append(self.termination())

    while self.current_lexeme[1] != 'Loop Delimiter End':
      children.append(self.statement())

    self.check('Loop Delimiter End')
    children.append(Node('Loop Delimiter End'))

    children.append(Node('Loop Identifier', value=self.current_lexeme[0]))
    self.check('Identifier')
    # children.append(self.identifier())

    return Node('Loop', children=children) 

  # --------------------------------------------------------------------------------------------------
  # <print_multiple> ::= VISIBLE <op_argument> <plus_argument>
  # --------------------------------------------------------------------------------------------------
  def print_multiple(self):
    children = []
    self.check('Print Concatenation')
    children.append(Node('Print Concatenation'))

    children.append(self.op_argument())

    if self.current_lexeme[1] == 'Print Concatenation':
      children.append(self.print_multiple())

    return Node('Print Multiple', children=children)
  
  # --------------------------------------------------------------------------------------------------
  # <print_fn> ::= <print_one> 
  # | <print_multiple>
  # --------------------------------------------------------------------------------------------------
  def print_fn(self):
    
    children = []

    self.check('Output Keyword')
    children.append(Node('Output Keyword'))

    children.append(self.op_argument())

    if self.current_lexeme[1] == 'Print Concatenation':
      children.append(self.print_multiple())
    
    return Node("Print Statement", children=children)

  # --------------------------------------------------------------------------------------------------
  # <input> ::= GIMMEH <variable>
  # --------------------------------------------------------------------------------------------------
  def input(self):
    children = []

    self.check('Input Keyword')
    children.append(Node('Input Keyword'))

    children.append(self.identifier())

    return Node('Input Keyword', children=children)

  # --------------------------------------------------------------------------------------------------
  # <typecast> ::= <explicit_typecasting> 
  # | <recasting>
  # --------------------------------------------------------------------------------------------------
  def typecast(self):
    children = []

    # Explicit typecast
    if self.current_lexeme[1] == 'Typecast Delimiter':
      children.append(self.explicit_typecast())
    
    # Recasting
    elif self.current_lexeme[1] == 'Identifier':
      children.append(self.recasting())

    return Node('Typecast', children=children)

  # --------------------------------------------------------------------------------------------------
  # <explicit_typecasting> ::= MAEK variable A type 
  # | MAEK variable type
  # --------------------------------------------------------------------------------------------------
  def explicit_typecast(self):
    children = []

    self.check('Typecast Delimiter')
    children.append(Node('Typecast Delimiter'))

    children.append(self.identifier())

    self.check('Typecast Keyword')
    children.append(Node('Typecast Keyword'))

    children.append(self.literal())

    return Node('Explicit Typecast', children=children)

  # --------------------------------------------------------------------------------------------------
  # <recasting> ::= variable IS NOW A type
  # | variable R <explicit_typecasting>
  # --------------------------------------------------------------------------------------------------
  def recasting(self):
    children = []

    children.append(self.identifier())
    if self.current_lexeme[1] == 'Typecast Keyword':
      self.check('Typecast Keyword')
      children.append(Node('Typecast Keyword'))

      self.check('TYPE Literal')
      children.append(Node('TYPE Literal'))

    elif self.current_lexeme[1] == 'Assignment':
      self.check('Assignment')
      children.append(Node('Assignment'))

      if self.current_lexeme[1] == 'Typecast Delimiter':
        children.append(self.explicit_typecast())
      else:
        children.append(self.op_argument())

    return Node('Recasting', children=children)

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

    return Node("String Concatenation", children = children)

  # --------------------------------------------------------------------------------------------------
  # <function_argument_definition> ::= YR variable 
  # | <fn_parameter> AN YR variable
  # --------------------------------------------------------------------------------------------------
  def function_argument_definition(self):
    children = []

    # YR
    self.check('Condition Delimiter')
    children.append(Node('Condition Delimiter'))

    # x
    children.append(self.identifier())

    # While AN
    while self.current_lexeme[1] == 'Operation Delimiter':
      # AN
      self.check('Operation Delimiter')
      children.append(Node('Operation Delimiter'))

      # YR
      self.check('Condition Delimiter')
      children.append(Node('Condition Delimiter'))

      # y
      children.append(self.identifier())

    return Node('Function Arguments', children=children)

  # --------------------------------------------------------------------------------------------------
  # <function_definition> ::= HOW IZ I function <linebreak> <statement> <linebreak> IF U SAY SO  
  # | HOW IZ I function <fn_parameter> <linebreak> <statement> <linebreak> IF U SAY SO
  # --------------------------------------------------------------------------------------------------
  def function_definition(self):
    children = []
    # HOW IZ I
    self.check('Function Delimiter Start')
    children.append(Node('Function Delimiter Start'))

    # Function name
    children.append(self.identifier())

    # There is arguments
    if self.current_lexeme[1] == 'Condition Delimiter':
      children.append(self.function_argument_definition())

    while self.current_lexeme[1] != 'Function Delimiter End':
      children.append(self.statement())

    self.check('Function Delimiter End')
    children.append(Node('Function Delimiter End'))    

    return Node('Function Definition', children=children)  

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

    return Node("Program", children = children)
