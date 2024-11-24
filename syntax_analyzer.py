from node import Node

# lexeme = lexemes[0][0] | current_lexeme[0]
# classification = lexemes[0][1] | current_lexeme[1]

class Syntax_Analyzer:

  def __init__(self, lexemes):
    self.lexemes = lexemes
    self.current_lexeme = lexemes[0]

  # --------------------------------------------------------------------------------------------------
  # starts the syntax analyzer and returns the parse tree
  # --------------------------------------------------------------------------------------------------
  def analyze(self):
    try:
      parse_tree = self.program()  # Start the program parsing
      return parse_tree
    except SyntaxError as e:
      return str(e)

  # --------------------------------------------------------------------------------------------------
  # pops lexeme from the list 
  # --------------------------------------------------------------------------------------------------
  def remove(self, type):
    if type == self.current_lexeme[1]:
        self.lexemes.pop(0)
        if self.lexemes:
            self.current_lexeme = self.lexemes[0]
    else:
        raise SyntaxError(f'Syntax Error: Expected {type}, but found {self.current_lexeme[1]}')

  # ==============================================================
  # dito kayo magdagdag ng other methods (production rules)
  # ==============================================================

  


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
    self.remove("Program Start")
    children.append(Node("Program Start"))

    # linebreak?

    # calls start_statement abstraction
    if self.current_lexeme[1] != "Program End":
      pass
      # children.append(self.start_statement([]))

    # linebreak?

    # program must end with KTHXBYE
    self.remove("Program End")
    children.append(Node("Program End"))

    return Node(None, "Program", children = children)