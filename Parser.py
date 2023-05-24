nextToken = ''

class chars:
    OPERATOR = 0
    DIGIT = 1
    LETTER = 2
    UNKNOWN = 100

    def alphanumeric(self, cclass):
        if cclass == self.DIGIT or cclass == self.LETTER:
            return True
        else:
            return False

class tokens:
    NUMERICAL_LITERAL = 3
    ADD_OP = 4
    SUB_OP = 5
    DOT = 6
    IDENTIFIER = 7
    ASSIGN_OP = 8
    DIV_OP = 9
    MULT_OP = 10
    MOD_OP = 11
    POSITIVE = 12
    NEGATIVE = 13
    UNKNOWN = 101

def lookup(char):
    global nextToken
    #global prevToken
    if char == "+":
        if prevToken in [tokens.IDENTIFIER, tokens.NUMERICAL_LITERAL]:
            addChar()
            nextToken = tokens.ADD_OP
        else:
            addChar()
            nextToken = tokens.POSITIVE
    elif char == "-":
        if prevToken in [tokens.IDENTIFIER, tokens.NUMERICAL_LITERAL]:
            addChar()
            nextToken = tokens.SUB_OP
        else:
            addChar()
            nextToken = tokens.NEGATIVE
    elif char == ".":
        addChar()
        nextToken = tokens.DOT
    elif char == "=":
        addChar()
        nextToken = tokens.ASSIGN_OP
    elif char == "/":
        addChar()
        nextToken = tokens.DIV_OP
    elif char == "*":
        addChar()
        nextToken = tokens.MULT_OP
    elif char == "%":
        addChar()
        nextToken = tokens.MOD_OP
    else:
        addChar()
        nextToken = tokens.UNKNOWN

    return nextToken

def addChar():
    global lexeme
    lexeme += nextChar

def getChar():
    global nextChar
    global charClass
    global lineNo
    nextChar = inputFile.read(1)
    if(nextChar.isalpha()):
        charClass = chars.LETTER
    elif(nextChar.isdigit()):
        charClass = chars.DIGIT
    elif(r"[+-*/%]", nextChar):
       charClass = chars.OPERATOR
    else:
        charClass = chars.UNKNOWN

def getNonBlank():
    global nextChar
    global lineNo
    while(nextChar.isspace()):
        if nextChar == '\n':
            lineNo += 1
        getChar()

#Lexical Analyzer
def lex():
    getNonBlank()
    global charClass
    global lexeme
    lexeme = ''
    global nextToken
    global prevToken

    if charClass == chars.DIGIT:
        addChar()
        getChar()

        while charClass == chars.DIGIT:
            addChar()
            getChar()
        if nextChar == ".":
            addChar()
            getChar()
            while charClass == chars.DIGIT:
                addChar()
                getChar()
        prevToken = nextToken
        nextToken = tokens.NUMERICAL_LITERAL

    elif charClass == chars.OPERATOR:
        prevToken = nextToken
        nextToken = lookup(nextChar)
        getChar()

        #Here we check if the + sign or - sign belongs to a signed number so we set it as a numerical literal
        if (nextToken == tokens.POSITIVE or nextToken == tokens.NEGATIVE) and charClass == chars.DIGIT:
            while charClass == chars.DIGIT:
                addChar()
                getChar()
            if nextChar == ".":
                addChar()
                getChar()
                while charClass == chars.DIGIT:
                    addChar()
                    getChar()
            prevToken = nextToken
            nextToken = tokens.NUMERICAL_LITERAL

    elif charClass == chars.LETTER:
        addChar()
        getChar()
        while charClass == chars.LETTER or charClass == chars.DIGIT:
            addChar()
            getChar()
        prevToken = nextToken
        nextToken = tokens.IDENTIFIER
    elif charClass == chars.UNKNOWN:
        prevToken = nextToken
        lookup(nextChar)
        getChar()
    #print(f'next token is {nextToken}, next Lexeme is {lexeme}')
    return lexeme



#Syntax Analyzer
def assign():
    global lineNo
    global prevToken
    global errors
    if nextChar not in ['', '\n']: #prevent skipping over lines
        lex()

    if nextToken == tokens.IDENTIFIER:
        if nextChar not in ['', '\n']:  # prevent skipping over lines
            lex()
        if nextToken == tokens.IDENTIFIER:
            if nextChar in ['\n'] and prevToken != tokens.IDENTIFIER:
                outputFile.write(f'Line {lineNo} is correct\n')
                lineNo += 1
                return
            if nextChar in ['']:
                outputFile.write(f'Line {lineNo} is correct\n')
                return

        while nextToken in [tokens.ADD_OP,tokens.SUB_OP,tokens.MULT_OP,tokens.DIV_OP,tokens.MOD_OP]:
            if nextChar not in ['', '\n']:
                lex()
            if nextToken == tokens.IDENTIFIER:
                if nextChar in ['\n']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    lineNo += 1
                    return
                if nextChar in ['']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    return
                lex()
            elif nextToken == tokens.NUMERICAL_LITERAL:
                if nextChar in ['\n']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    lineNo += 1
                    return
                if nextChar in ['']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    return
                lex()
            else:
                outputFile.write(f'ERROR in line {lineNo}: expected Identifier or Numerical Literal after operator instead found {lexeme}\n')
                lineNo += 1
                errors +=1
                if nextChar not in ['', '\n']:
                    line = inputFile.readline()
                return
        if lexeme != '':
            outputFile.write(f'ERROR in line {lineNo}: expected operator after identifier instead found {lexeme}\n')
            lineNo += 1
            errors +=1
            if nextChar not in ['', '\n']:
                 line = inputFile.readline()

    elif nextToken == tokens.NUMERICAL_LITERAL:
        if nextChar not in ['', '\n']:  # prevent skipping over lines
            lex()
        if nextToken == tokens.NUMERICAL_LITERAL:
            if nextChar in ['\n']:
                outputFile.write(f'Line {lineNo} is correct\n')
                lineNo += 1
                return
            if nextChar in ['']:
                outputFile.write(f'Line {lineNo} is correct\n')
                return
        while nextToken in [tokens.ADD_OP, tokens.SUB_OP, tokens.MULT_OP, tokens.DIV_OP, tokens.MOD_OP]:
            if nextChar not in ['','\n']:
                lex()
            if nextToken == tokens.IDENTIFIER:
                if nextChar in ['\n']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    lineNo += 1
                    return
                if nextChar in ['']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    return
                lex()
            elif nextToken == tokens.NUMERICAL_LITERAL:
                if nextChar in ['\n']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    lineNo += 1
                    return
                if nextChar in ['']:
                    outputFile.write(f'Line {lineNo} is correct\n')
                    return
                lex()
            else:
                outputFile.write(f'ERROR in line {lineNo}: expected Identifier or Numerical Literal after operator instead found {lexeme}\n')
                lineNo += 1
                errors+=1
                if nextChar not in ['', '\n']:
                    line = inputFile.readline()       #line consuming after err
                return
        if lexeme != '':
            outputFile.write(f'ERROR in line {lineNo}: expected operator after numerical literal instead found {lexeme}\n')
            lineNo += 1
            errors+=1
            if nextChar not in ['', '\n']:
                inputFile.readline()      #line consuming after err
    else:
        outputFile.write(f'ERROR in line {lineNo}: expected Identifier or Numerical Literal after assignment operator instead found {lexeme}\n')
        lineNo+=1
        errors+=1
        if nextChar not in ['', '\n']:
            line = inputFile.readline()      #line consuming after err

def line_parser():
    global lineNo
    global errors
    getChar()
    lex()

    if nextToken == tokens.IDENTIFIER:
        if nextChar not in ['', '\n']:
            lex()
        if nextToken == tokens.ASSIGN_OP:
            assign()
        else:
            outputFile.write(f'ERROR in line {lineNo}: expected assignment operator after identifier instead found {lexeme}\n')
            lineNo += 1
            errors +=1
            if nextChar not in ['', '\n']:
                line = inputFile.readline()

    else:
        outputFile.write(f'ERROR in line {lineNo}: expected identifier instead found {lexeme}\n')
        lineNo+=1
        errors+=1
        if nextChar not in ['', '\n']:
            line = inputFile.readline()

def eof():
    currentpos = inputFile.tell()
    if inputFile.read(1) == '':
        return True
    else:
        inputFile.seek(currentpos)
        return False



global outputFile
global inputFile
filenumber = 1
fileexists = True
outputFile = open('parser_output.txt', "w")
while fileexists:
    try:
            with open(f'{filenumber}.txt', "r") as inputFile:
                errors = 0
                lineNo = 1
                outputFile.write(f'File Number {filenumber}: \n')
                while not eof():
                    line_parser()
            outputFile.write(f'\nProgram ran with {errors} errors')
            outputFile.write(f'\n--------------------------------------------------------------------\n')
            filenumber+= 1
    except FileNotFoundError:
        fileexists = False
        break

