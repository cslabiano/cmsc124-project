import re

def analyze_lexemes(content):

    lexemes = []
    pattern_dict = {}

    with open("patterns.txt", "r", encoding="utf-8") as patterns:
        lines = patterns.readlines()

    # Place patterns in a dictionary
    for line in lines:
        parts = line.strip().split(", ")
        # Remove "" of the regex
        pattern = parts[0]
        type = parts[1].strip('"')
        if type != "YARN Literal":
            pattern = pattern.strip('"')
        # Use re.compile() to treat it as r"pattern"
        pattern_dict[re.compile(pattern)] = type

    insideMultilineComment = False
    line_number = 1  # Initialize line number

    for line in content.splitlines():
        line = line.lstrip()
        # Print the current line and its line number
        print(f"Line {line_number}: {line}")
        
        # If inside multiline comment, make each line a comment until TLDR
        if insideMultilineComment:
            # TODO: Change this logic to something not hardcoded
            if line == "TLDR":
                insideMultilineComment = False
                lexemes.append((line, 'Multiline Comment Delimiter', line_number))
            else:
                lexemes.append((line, 'Comment', line_number))
            line_number += 1
            continue

        # Process each line
        while line:
            matched = False
            for regex, type in pattern_dict.items():
                match = regex.search(line)
                if match:
                    # Takes the whole match
                    lexeme = match.group(0)
                    # If the type match is a Comment Delimiter
                    if type == "Comment Delimiter":
                        lexemes.append((lexeme, type, line_number))
                        line = line.replace(lexeme, "", 1).strip()
                        # Add to tokens the rest of the line 
                        if line:
                            lexemes.append((line, 'Comment', line_number))
                            line = ""
                    # If the type match is a Multiline Comment Delimiter
                    elif type == "Multiline Comment Delimiter":
                        lexemes.append((lexeme, type, line_number))
                        insideMultilineComment = not insideMultilineComment
                        line = line.replace(lexeme, "", 1).strip()
                    # If the type match is a YARN literal
                    elif type == "YARN Literal":
                        # Append quote
                        lexemes.append(('"', 'String Delimiter', line_number))
                        # Append YARN literal
                        lexemes.append((lexeme[1:-1], type, line_number))
                        # Append quote
                        lexemes.append(('"', 'String Delimiter', line_number))
                        line = line.replace(lexeme, "", 1).strip()
                    # Append to tokens normally
                    else: 
                        lexemes.append((lexeme, type, line_number))
                        # Removes the match in the current line ensuring that it won't repeat
                        line = line.replace(lexeme, "", 1).strip()
                        matched = True
                    break
            # In case nothing matches
            if not matched:
                break;

        line_number += 1  # Increment the line number after processing each line

    print(lexemes)
    return lexemes
