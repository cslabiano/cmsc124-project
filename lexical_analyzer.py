import re

def analyze_lexemes(content):

  lexemes = []
  pattern_dict = {}

  with open("patterns.txt", "r", encoding="utf-8") as patterns:
    lines = patterns.readlines()

  #place patterns to a dictionary
  for line in lines:
    parts = line.strip().split(", ")
    #remove "" of the regex
    pattern = parts[0]
    type = parts[1].strip('"')
    if type != "YARN Literal":
      pattern = pattern.strip('"')
    #use re.compile() to treat it as r"pattern"
    pattern_dict[re.compile(pattern)] = type

  insideMultilineComment = False
  for line in content.splitlines():
    line = line.lstrip()
    print(line)
    # If inside multiline comment, make each line a comment until TLDR
    if insideMultilineComment:
        # TODO: Change this logic to something not hardcoded
        if line == "TLDR":
          insideMultilineComment = False
          lexemes.append((line, 'Multiline Comment Delimiter'))
        else:
          lexemes.append((line, 'Comment'))
        continue

    #continues until the line is empty
    while line:
      matched = False
      for regex, type in pattern_dict.items():
          match = regex.search(line)
          if match:
            #takes the whole match
            lexeme = match.group(0)
            # If the type match is a Comment Delimiter
            if type == "Comment Delimiter":
              lexemes.append((lexeme, type))
              line = line.replace(lexeme, "", 1).strip()
              # Add to tokens the rest of the line 
              if line:
                lexemes.append((line, 'Comment'))
                line = ""
            # If the type match is a Multiline Comment Delimiter
            elif type == "Multiline Comment Delimiter":
                lexemes.append((lexeme, type))
                insideMultilineComment = not insideMultilineComment
                line = line.replace(lexeme, "", 1).strip()
            # If the type match is a YARN literal
            elif type == "YARN Literal":
                # Append quote
                lexemes.append(('"', 'String Delimiter'))
                # Append YARN literal
                lexemes.append((lexeme[1:-1], type))
                # Append quote
                lexemes.append(('"', 'String Delimiter'))
                line = line.replace(lexeme, "", 1).strip()
            # Append to tokens normally
            else: 
              lexemes.append((lexeme, type))
              #removes the match in the current line ensuring that it won't repeat
              line = line.replace(lexeme, "", 1).strip()
              matched = True
            break
      #in case nothing matches
      if not matched:
          return [("error", "error")]
  
  return lexemes