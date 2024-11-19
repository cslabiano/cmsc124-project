import re

def syntax_analyzer(content):

    lines = content.readlines()
    current = 0         # array counter to keep track which line is being read

    err_status, err_msg = program(lines, current)
    
    return err_status, err_msg

# program abstraction
def program(lines, current):
    
    hai = re.search(r"^HAI\b", lines[current])      # check if HAI is correct, same format for the others
    if hai == None:
        err_msg = "Program must start with HAI"
        return True, err_msg
    current += 1        # increment current to get to the next line
    
    err_status, err_msg, current = data_section(lines, current)    # call data section abstraction and return these values

    if err_status == True:      # if it got an error in the data section part
        return True, err_msg
    
    err_status, err_msg, current = statement(lines, current)

    if err_status == True:
        return True, err_msg

    kthxbye = re.search(r"^KTHXBYE\b", lines[current])
    if kthxbye == None:
        err_msg = "Program must end with KTHXBYE"
        return True, err_msg

    return False

# data section abstraction
def data_section(lines, current):

    wazzup = re.search(r"^WAZZUP\b", lines[current])
    if wazzup == None:
        err_msg = "Data section must start with WAZZUP"
        return True, err_msg, current
    current += 1

    err_status, err_msg, current = statement(lines, current)

    if err_status == True:
        return True, err_msg

    buhbye = re.search(r"^BUHBYE\b", lines[current])
    if buhbye == None:
        err_msg = "Data section must end with BUHBYE"
        return True, err_msg
    current += 1
    
    return False, "", current

# var abstraction
def var(lines, current):
    return

# statement abstraction
def statement(lines, current):

    not_end = True

    while no_err:

        # TODO: Can create if-else statements for each possible statement in our syntax


        current += 1
        #if it reaches the end of the code, end the loop
        if re.search(r"^KTHXBYE\b", lines[current]) != None:
            not_end = False

    return 