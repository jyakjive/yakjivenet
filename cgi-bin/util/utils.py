

#remember a key and value pair
def remember(recall, data = '', memory = dict()):
    try:
        if (data != ''):
            memory[recall] = data
        return memory[recall]
    except:
        return None

#verify that a string is not a tab, new line, a space, or empty
def verifyNotWhitespace(data):
    check = (data.isspace() != True) & (data != '\t') & (data != '\n') & (data != '\r') & (data != '') & (data != ' ')
    return check

# classes
