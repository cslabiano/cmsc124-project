import re

def analyze_lexemes(content):
  lexemes = []
  pattern_dict = {}

  with open("patterns.txt", "r", encoding="utf-8") as patterns:
    lines = patterns.readlines()

  # place patterns into a dictionary
  for line in lines:
    parts = line.strip().split(", ")
    # remove "" of the regex
    pattern = parts[0]
    type = parts[1].strip('"')
    if type != "YARN Literal":
      pattern = pattern.strip('"')
    # use re.compile() to treat it as r"pattern"
    pattern_dict[re.compile(pattern)] = type

  insideMultilineComment = False
  for line_num, line in enumerate(content.splitlines(), start=1):
    line = line.lstrip()
    print(line)
    # if inside multiline comment, make each line a comment until TLDR
    if insideMultilineComment:
      # TODO: Change this logic to something not hardcoded
      if line == "TLDR":
        insideMultilineComment = False
        lexemes.append((line, 'Multiline Comment Delimiter'))
      else:
        lexemes.append((line, 'Comment'))
      continue

    # continues until the line is empty
    while line:
      matched = False
      for regex, type in pattern_dict.items():
        match = regex.search(line)
        if match:
          # takes the whole match
          lexeme = match.group(0)
          # if the type match is a Comment Delimiter
          if type == "Comment Delimiter":
            lexemes.append((lexeme, type))
            line = line.replace(lexeme, "", 1).strip()
            # add to tokens the rest of the line
            if line:
              lexemes.append((line, 'Comment'))
              line = ""
          # if the type match is a Multiline Comment Delimiter
          elif type == "Multiline Comment Delimiter":
            lexemes.append((lexeme, type))
            insideMultilineComment = not insideMultilineComment
            line = line.replace(lexeme, "", 1).strip()
          # if the type match is a YARN Literal
          elif type == "YARN Literal":
            # append quote
            lexemes.append(('"', 'String Delimiter'))
            # append YARN literal
            lexemes.append((lexeme[1:-1], type))
            # append quote
            lexemes.append(('"', 'String Delimiter'))
            line = line.replace(lexeme, "", 1).strip()
          # appent to tokens normally
          else:
            lexemes.append((lexeme, type))
            # removes the match in the current line ensuring that it won't repeat
            line = line.replace(lexeme, "", 1).strip()
          matched = True
          break
      # in case nothing matches
      if not matched:
        # return an error message with line number for the gui to display
        return None, f"Lexical error on line {line_num}: '{line}' could not be matched."

  return lexemes, None
