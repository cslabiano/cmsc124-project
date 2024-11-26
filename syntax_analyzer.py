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
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # TODO: Expressions are not yet supported
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

    # TODO: Handle expressions here
    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')
    return Node(None, "Op Argument", children=children)

  # ======================================================================
  # <op_argument> ::= <literal> | <variable>
  # An operation argument can either be a literal, variable, or expression
  # TODO: Infinite expressions are not yet supported
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

    #TODO: Handle infinite expressions here

    else: 
      raise SyntaxError(f'Syntax Error: Expected Operation argument, but found {self.current_lexeme[1]}')

    return Node(None, "Infinite Op Argument", children=children)

  # ======================================================================
  # <boolean> ::= <fixed_boolean> | <infinite_boolean>
  # Booleans can either be a fixed boolean or an infinite boolean 
  # ======================================================================
  def boolean(self):
    children = []

    if self.current_lexeme[1] in {'And', 'Or', 'Xor', 'Not'}:
        children.append(self.fixed_boolean())
    elif self.current_lexeme[1] in {'Infinite Or', 'Infinite And'}:
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
  # TODO: Fix bug where AN that is not followed by an argument is accepted
  # ======================================================================
  def fixed_boolean(self):
    children = []

    if self.current_lexeme[1] in {'And', 'Or', 'Xor'}:
      self.check(self.current_lexeme[1])
      children.append(Node(self.current_lexeme[1]))
      
      children.append(self.op_argument())

      self.check("Operation Delimiter")
      children.append(Node("Operation Delimiter"))

      children.append(self.op_argument())
    
    elif self.current_lexeme[1] == 'Not':
      self.check("Not")
      children.append(Node("Not"))

      children.append(self.op_argument())

    return Node(None, "Fixed Boolean", children=children)

  
    # ======================================================================
  
  # ======================================================================
  # <infinite_argument> ::= <op_argument> AN <infinite_argument> | <op_argument>
  # TODO: Fix bug where AN that is not followed by an argument is valid
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
    if self.current_lexeme[1] == "Infinite And":
        self.check("Infinite And")
        children.append(Node("Infinite And"))
    elif self.current_lexeme[1] == "Infinite Or":
        self.check("Infinite Or")
        children.append(Node("Infinite Or"))

    children.append(self.infinite_argument())

    # Check 'MKAY'
    if self.current_lexeme[1] == "Function Call Delimiter":
        self.check("Function Call Delimiter")
        children.append(Node("Function Call Delimiter"))

    return Node(None, "Infinite Boolean", children=children)
  
  
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
      if self.current_lexeme[1] in {'And', 'Or', 'Xor', 'Not', 'Infinite And', 'Infinite Or'}: 
        children.append(self.boolean())
      # children.append(self.start_statement([]))

    # linebreak?

    # program must end with KTHXBYE
    self.check("Program End")
    children.append(Node("Program End"))

    return Node(None, "Program", children = children)