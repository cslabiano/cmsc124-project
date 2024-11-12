import re

def analyze_lexemes(content):

  lexemes = []
  pattern_dict = {}

  #read the patterns.txt file
  patterns = open("patterns.txt", "r")
  print(patterns)

  if not patterns:
    print("Error in patterns.txt")

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
    for regex, type in pattern_dict.items():
      matches = regex.findall(line)
      for match in matches:
        lexemes.append((match, type))
  
  return lexemes