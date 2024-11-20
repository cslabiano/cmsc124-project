lexemes = [('HAI', 'Code Delimiter', 1), ('I HAS A', 'Variable Declaration', 2), ('STRING', 'Identifier', 2), ('ITZ', 'Variable Assignment', 2), ('5', 'NUMBR Literal', 2), ('HOW IZ I', 'Function Delimiter', 3), ('POWERTWO', 'Identifier', 3), ('YR', 'Parameter Delimiter', 3), ('NUM', 'Identifier', 3), ('BTW', 'Comment Delimiter', 4), ('RETURN 1 IF 2 TO POWER OF 0', 'Comment', 4), ('BOTH SAEM', 'Equality Expression Relational', 5), ('NUM', 'Identifier', 5), ('AN', 'Operation Delimiter', 5), ('0', 'NUMBR Literal', 5), ('O RLY?', 'Control Flow Delimiter', 6), ('YA RLY', 'If Keyword', 7), ('YA RLY', 'If Keyword', 7), ('FOUND YR', 'Function Return', 8), ('1', 'NUMBR Literal', 8), ('OIC', 'Control Flow Delimiter', 9), ('OBTW', 'Multiline Comment Delimiter', 11), ('this is a comment', 'Comment', 12), ("No it's a two line comment", 'Comment', 13), ('Oops no.. it has many lines here', 'Comment', 14), ('TLDR', 'Multiline Comment Delimiter', 15), ('BTW', 'Comment Delimiter', 17), ('CALCULATE 2 TO POWER OF NUM', 'Comment', 17), ('I HAS A', 'Variable Declaration', 18), ('INDEX', 'Identifier', 18), ('ITZ', 'Variable Assignment', 18), ('0', 'NUMBR Literal', 18), ('I HAS A', 'Variable Declaration', 19), ('TOTAL', 'Identifier', 19), ('ITZ', 'Variable Assignment', 19), ('1', 'NUMBR Literal', 19), ('IM IN YR', 'Loop Delimiter', 20), ('LOOP', 'Identifier', 20), ('UPPIN', 'Loop Increment', 20), ('YR', 'Parameter Delimiter', 20), ('INDEX', 'Identifier', 20), ('TIL', 'Loop Condition', 20), ('BOTH SAEM', 'Equality Expression Relational', 20), ('INDEX', 'Identifier', 20), ('AN', 'Operation Delimiter', 20), ('NUM', 'Identifier', 20), ('TOTAL', 'Identifier', 21), ('R', 'Assignment', 21), ('PRODUKT OF', 'Multiplication Expression Arithmetic', 21), ('TOTAL', 'Identifier', 21), ('AN', 'Operation Delimiter', 21), ('2', 'NUMBR Literal', 21), ('IM OUTTA YR', 'Loop Delimiter', 22), ('LOOP', 'Identifier', 22), ('FOUND YR', 'Function Return', 24), ('TOTAL', 'Identifier', 24), 
 ('IF U SAY SO', 'Function Delimiter', 25),
('BTW', 'Comment Delimiter', 26), ('OUTPUT: 8', 'Comment', 26), ('VISIBLE', 'Output Keyword', 27), ('I IZ', 'Function Call Delimiter', 27), ('POWERTWO', 'Identifier', 27), ('YR', 'Parameter Delimiter', 27), ('MKAY', 'Function Call Delimiter', 27), ('KTHXBYE', 'Code Delimiter', 28)]

# ALGO:
# Go through each token, if a delimiter is found,
# collect tokens for that specific expression, 
# then call function to check if tokens are in order and are valid
# EXAMPLE: 
# Code Delimiter (HAI) is checked, collect all tokens until the next Code Delimiter (KTHXBYE), then pass tokens to code_statements to check validity of each statament
def syntax_analyzer(lexemes):
    try:
        while lexemes:
            if lexemes and lexemes[0][1] == 'Code Delimiter':
                print("Start of Code")
                code_tokens = []  # To store tokens between code delimiters
                lexemes.pop(0)  # Eat first Code Delimiter
                
                # Pop until next code delimiter
                while lexemes and lexemes[0][1] != 'Code Delimiter':
                    code_tokens.append(lexemes.pop(0)) #ERROR POPPING KAHIT WALA NA 
                    
                # When we encounter the next "Code Delimiter", process the collected tokens
                if lexemes[0][1] == 'Code Delimiter':
                    lexemes.pop(0)
                    if not code_statements(code_tokens):
                        print('Invalid grammar')  # Process the collected code tokens
                        return
                else:
                    print("End of code delimiter not found.")
                    return 
            else: 
                print("Start code delimiter not found")
                return
        print("Valid grammar")
    except: 
        print("Invalid grammar")

# TODO: Implement expressions, concatenation, input, if-then, switch-case, loop, Multiline
def code_statements(code_tokens):
    while code_tokens:
        token_type = code_tokens[0][1]
# VARIABLE DECLARATION
        if token_type == 'Variable Declaration':
            code_tokens.pop(0)
            if variable_declaration(
                code_tokens.pop(0),
                code_tokens.pop(0),
                code_tokens.pop(0)
            ):
                print("Valid Variable Declaration")
            else:
                print("Invalid Variable Declaration")
                return False
# FUNCTION DECLARATION
        elif token_type == 'Function Delimiter':
            function_tokens = []
            code_tokens.pop(0) # Remove the function delimiter
            
            while code_tokens and code_tokens[0][1] != 'Function Delimiter':
                function_tokens.append(code_tokens.pop(0))
            
            if code_tokens and code_tokens[0][1] == 'Function Delimiter':
                code_tokens.pop(0)
                if function_declaration(function_tokens):
                    print("Valid function declaration")
                else:
                    print("Invalid Function Declaration")
                    return False
            else:
                print("Invalid Function Declaration")
                return False
        
# COMMENT DELIMITER
        elif token_type == 'Comment Delimiter':
            code_tokens.pop(0)
            if code_tokens[0][1] == 'Comment':
                print("Valid Comment")
                code_tokens.pop(0)

# OUTPUT KEYWORD
        elif token_type == 'Output Keyword':
            code_tokens.pop(0)
            output_tokens = []

            output_line_number = code_tokens[0][2]
            while code_tokens and code_tokens[0][2] == output_line_number:
                output_tokens.append(code_tokens.pop(0))

            output_declaration(output_tokens)
# FUNCTION CALL DELIMITER
        elif token_type == 'Function Call Delimiter':
            code_tokens.pop(0)
            function_call_declaration(code_tokens.pop(0), code_tokens.pop(0), code_tokens.pop(0))
# EXPRESSION
        elif 'Expression' in token_type:
            if 'Relational' in code_tokens[0][1]:
                code_tokens.pop(0)
                relational_expression_declaration(code_tokens.pop(0), code_tokens.pop(0), code_tokens.pop(0))
                # print(code_tokens)
            # TODO: Arithmetic
            # TODO: Boolean
            else:
                print("Expression probably arithmetic or boolean")
                return False
# INPUT KEYWORD
        elif token_type == 'Input Keyword':
            code_tokens.pop(0)
            print("Input keyword not parsed yet")
            return False
# CONTROL FLOW DELIMITER
        elif token_type == 'Control Flow Delimiter':
            code_tokens.pop(0)
            print("Control Flow not parsed yet")
            return False
# LOOP DELIMITER
        elif token_type == 'Loop Delimiter':
            code_tokens.pop(0)
            print("Loop not parsed yet")
            return False
        else:
            print(f"Unhandled or invalid token: {code_tokens[0]}")
            return False
    return True

def variable_declaration(identifier, assignment, value):
    # print(f"{identifier} {assignment} {value}")
    if identifier[1] == 'Identifier' and assignment[1] == 'Variable Assignment':
        if 'Literal' in value[1] or 'Identifier' in value[1] or 'Expression' in value[1]:
            return True
    return False

# TODO: Implement function checker
def function_declaration(function_tokens):
    if function_tokens[0][1] == 'Identifier' and function_tokens[1][1] == 'Parameter Delimiter' and function_tokens[2][1] == 'Identifier':
        function_tokens.pop(0)
        function_tokens.pop(0)
        function_tokens.pop(0)
        code_statements(function_tokens)
        return True
    return False

# TODO: Only accepts literals as arguments as of the moment
def function_call_declaration(identifier, param_delimiter, literal):
    if identifier[1] == 'Identifier' and param_delimiter[1] == 'Parameter Delimiter' and 'Literal' in literal[1]:
        return True
    else:
        return False

# TODO: Implement output checker
def output_declaration(output_arguments):
    code_statements(output_arguments)
    print("Valid Output declaration")
    return True

# TODO: Impelement Control Flow Checker
def control_flow_declaration(control_flow_tokens):
    print("Control Flow tokens")
    return True

def relational_expression_declaration(arg1, an, arg2):
    if 'Literal' in arg1[1] or 'Identifier' in arg1[1] and an[1] == 'Operation Delimiter' and 'Literal' in arg2[1] or 'Identifier' in arg2[1]:
        print("Valid Relational Expression")
        return True

def expression_declaration(expression_tokens):
    return True


def main():
    syntax_analyzer(lexemes)

if __name__ == "__main__":
    main()
