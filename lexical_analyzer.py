import re

def analyze_lexemes(content):

  lexemes = []
  pattern_dict = {}

  #read the patterns.txt file
  # patterns = open("patterns.txt", "r")

  # if not patterns:
  #   print("Error in patterns.txt")

  # lines = patterns.readlines()

  with open("patterns.txt", "r", encoding="utf-8") as patterns:
    lines = patterns.readlines()

  #place patterns to a dictionary
  for line in lines:
    parts = line.strip().split(", ")
    #remove "" of the regex
    pattern = parts[0].strip('"')
    type = parts[1]
    #use re.compile() to treat it as r"pattern"
    pattern_dict[re.compile(pattern)] = type

  #find matches per line of the content
  for line in content.splitlines():
    #continues until the line is empty
    while line:
      matched = False
      for regex, type in pattern_dict.items():
          match = regex.search(line)
          if match:
            #takes the whole match
            lexeme = match.group(0)
            lexemes.append((lexeme, type))
            #removes the match in the current line ensuring that it won't repeat
            line = line.replace(lexeme, "", 1).strip()
            matched = True
            break
      #in case nothing matches
      if not matched:
          break 
  
  return lexemes