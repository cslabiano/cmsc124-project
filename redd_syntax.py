lexemes = [
    ('HAI', 'Code Delimiter', 1),
    ('I HAS A', 'Variable Declaration', 2),
    ('STRING', 'Identifier', 2),
    ('ITZ', 'Variable Assignment', 2),
    ('5', 'NUMBR Literal', 2),
    ('HOW IZ I', 'Function Delimiter', 3),
    ('POWERTWO', 'Identifier', 3),
    ('YR', 'Parameter Delimiter', 3),
    ('NUM', 'Identifier', 3),
    ('BTW', 'Comment Delimiter', 4),
    ('RETURN 1 IF 2 TO POWER OF 0', 'Comment', 4),
    ('BOTH SAEM', 'Equality Expression', 5),
    ('NUM', 'Identifier', 5),
    ('AN', 'Operation Delimiter', 5),
    ('0', 'NUMBR Literal', 5),
    ('O RLY?', 'Control Flow Delimiter', 6),
    ('YA RLY', 'If Keyword', 7),
    ('YA RLY', 'If Keyword', 7),
    ('FOUND YR', 'Function Return', 8),
    ('1', 'NUMBR Literal', 8),
    ('OIC', 'Control Flow Delimiter', 9),
    ('OBTW', 'Multiline Comment Delimiter', 11),
    ('this is a comment', 'Comment', 12),
    ("No it's a two line comment", 'Comment', 13),
    ('Oops no.. it has many lines here', 'Comment', 14),
    ('TLDR', 'Multiline Comment Delimiter', 15),
    ('BTW', 'Comment Delimiter', 17),
    ('CALCULATE 2 TO POWER OF NUM', 'Comment', 17),
    ('I HAS A', 'Variable Declaration', 18),
    ('INDEX', 'Identifier', 18),
    ('ITZ', 'Variable Assignment', 18),
    ('0', 'NUMBR Literal', 18),
    ('I HAS A', 'Variable Declaration', 19),
    ('TOTAL', 'Identifier', 19),
    ('ITZ', 'Variable Assignment', 19),
    ('1', 'NUMBR Literal', 19),
    ('IM IN YR', 'Loop Delimiter', 20),
    ('LOOP', 'Identifier', 20),
    ('UPPIN', 'Loop Increment', 20),
    ('YR', 'Parameter Delimiter', 20),
    ('INDEX', 'Identifier', 20),
    ('TIL', 'Loop Condition', 20),
    ('BOTH SAEM', 'Equality Expression', 20),
    ('INDEX', 'Identifier', 20),
    ('AN', 'Operation Delimiter', 20),
    ('NUM', 'Identifier', 20),
    ('TOTAL', 'Identifier', 21),
    ('R', 'Assignment', 21),
    ('PRODUKT OF', 'Multiplication Expression', 21),
    ('TOTAL', 'Identifier', 21),
    ('AN', 'Operation Delimiter', 21),
    ('2', 'NUMBR Literal', 21),
    ('IM OUTTA YR', 'Loop Delimiter', 22),
    ('LOOP', 'Identifier', 22),
    ('FOUND YR', 'Function Return', 24),
    ('TOTAL', 'Identifier', 24),
    ('IF U SAY SO', 'Function Delimiter', 25),
    ('BTW', 'Comment Delimiter', 26),
    ('OUTPUT: 8', 'Comment', 26),
    ('VISIBLE', 'Output Keyword', 27),
    ('I IZ', 'Function Call Delimiter', 27),
    ('POWERTWO', 'Identifier', 27),
    ('YR', 'Parameter Delimiter', 27),
    ('4', 'NUMBR Literal', 27),
    ('MKAY', 'Function Call Delimiter', 27),
    ('KTHXBYE', 'Code Delimiter', 28)
]

# ALGO:
# Go through each token, if a delimiter is found,
# collect tokens for that specific expression, 
# then call function to check if tokens are in order and are valid
# EXAMPLE: 
# Code Delimiter (HAI) is checked, collect all tokens until the next Code Delimiter (KTHXBYE), then pass tokens to code_statements to check validity of each statament
def syntax_analyzer(lexemes):
    currentToken = 0
    total_tokens = len(lexemes)
    
    while currentToken < total_tokens:
        token_type = lexemes[currentToken][1]
        
        if token_type == 'Code Delimiter':
            print("Start of Code")
            code_tokens = []  # To store tokens between code delimiters
            currentToken += 1  # Move to the token after the 'Code Delimiter'
            
            # Collect tokens until we reach the next "Code Delimiter"
            while currentToken < total_tokens and lexemes[currentToken][1] != 'Code Delimiter':
                code_tokens.append(lexemes[currentToken])
                currentToken += 1
            
            # When we encounter the next "Code Delimiter", process the collected tokens
            if currentToken < total_tokens and lexemes[currentToken][1] == 'Code Delimiter':
                currentToken += 1
                code_statements(code_tokens)  # Process the collected code tokens
            else:
                print("End of code delimiter not found.")
                
            # Check if we've reached the last Code Delimiter, then break the loop
            if currentToken >= total_tokens:
                print("End of code")
                break
                
        else: 
            currentToken += 1  # Skip tokens that are not 'Code Delimiters'

# eto ung statement sa grammar
# TODO: Implement variables, expressions, concatenation, input, if-then, switch-case, loop
def code_statements(code_tokens):
    currentToken = 0
    total_tokens = len(code_tokens)
    
    while currentToken < total_tokens:
        token_type = code_tokens[currentToken][1]
        
        if token_type == 'Variable Declaration':
            if variable_declaration(
                code_tokens[currentToken + 1],
                code_tokens[currentToken + 2],
                code_tokens[currentToken + 3]
            ):
                currentToken += 4
            else:
                print("Invalid Variable Declaration")
                break
        
        elif token_type == 'Function Delimiter':
            function_tokens = []
            currentToken += 1
            
            while currentToken < total_tokens and code_tokens[currentToken][1] != 'Function Delimiter':
                function_tokens.append(code_tokens[currentToken])
                currentToken += 1
            
            if currentToken < total_tokens and code_tokens[currentToken][1] == 'Function Delimiter':
                function_tokens.append(code_tokens[currentToken]) 
                currentToken += 1
            else:
                print("Invalid Function Declaration")
                break
            
            if function_declaration(function_tokens):
                print("Valid function declaration")
            else:
                print("Invalid Function Declaration")
        
        elif token_type == 'Comment Delimiter':
            print("Valid comment")
            currentToken += 2
        
        elif token_type == 'Output Keyword':
            print("Valid output")
            output_tokens = []

            # Collect tokens that are on the same line number as the 'Output Keyword'
            output_line_number = code_tokens[currentToken][2]
            currentToken += 1
            while currentToken < total_tokens and code_tokens[currentToken][2] == output_line_number:
                output_tokens.append(code_tokens[currentToken])
                currentToken += 1

            # Pass collected output tokens to the output_declaration function
            output_declaration(output_tokens)
        elif token_type == 'Function Call Delimiter':
            print("Valid function call")
            function_call_tokens = []

            function_call_line_number = code_tokens[currentToken][2]
            currentToken += 1  # Skip the current Function Call Delimiter

            # Collect tokens until the next Function Call Delimiter, without including it
            while currentToken < total_tokens and code_tokens[currentToken][2] == function_call_line_number:
                if code_tokens[currentToken][1] != 'Function Call Delimiter':  # Exclude the delimiter itself
                    function_call_tokens.append(code_tokens[currentToken])
                currentToken += 1

            # Process the function call tokens
            function_call_declaration(function_call_tokens)
        else:
            print(f"Unhandled or invalid token: {code_tokens[currentToken]}")
            currentToken += 1

def variable_declaration(identifier, assignment, value):
    if identifier[1] == 'Identifier' and assignment[1] == 'Variable Assignment':
        if 'Literal' in value[1] or 'Identifier' in value[1] or 'Expression' in value[1]:
            print(f"Valid Variable Declaration: {identifier[0]} = {value[0]}")
            return True
    return False

# TODO: Implement function checker
def function_declaration(function_tokens):
    if function_tokens:
        function_name = function_tokens[0]  # First token is the function name
        arguments = [token[0] for token in function_tokens[1:] if token[1] == 'Identifier']
        
        # print(f"Valid function declaration: Name - {function_name[0]} Args - {', '.join(arguments)}")
        return True
    return False

# TODO: Only accepts literals as arguments as of the moment
def function_call_declaration(function_call_tokens):
    # print(function_call_tokens)
    if function_call_tokens[0][1] == 'Identifier' and function_call_tokens[1][1] == 'Parameter Delimiter' and function_call_tokens[2][1] == 'Parameter Delimiter' and 'Literal' in function_call_tokens[3][1]:
        return True
    else:
        return False

# TODO: Implement output checker
def output_declaration(output_arguments):
    # print(output_arguments)
    code_statements(output_arguments)
    return True

def main():
    syntax_analyzer(lexemes)

if __name__ == "__main__":
    main()
