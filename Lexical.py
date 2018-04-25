import sys

class Lexical(object):

    def __init__(self):
        # Initialize variables
        self.buffer = ""
        self.state = 0
        self.tokens = list()
        self.error = False
        self.count_line = 1
        self.count_column = 1
        self.flag_comment = False
        self.flag_literal = False

        # Table of symbols capable to read
        self.symbols = {
            # Alphabet lower case
            'a':'L','b':'L','c':'L','d':'L','e':'e','f':'L','g':'L','h':'L','i':'L','j':'L','k':'L','l':'L',
            'm':'L','n':'L','o':'L','p':'L','q':'L','r':'L','s':'L','t':'L','u':'L','v':'L','x':'L','w':'L',
            'y':'L','z':'L',
            # Alphabet upper case
            'A':'L','B':'L','C':'L','D':'L','E':'E','F':'L','G':'L','H':'L','I':'L','J':'L','K':'L','L':'L',
            'M':'L','N':'L','O':'L','P':'L','Q':'L','R':'L','S':'L','T':'L','U':'L','V':'L','X':'L','W':'L',
            'Y':'L','Z':'L',
            # Dumbers
            '0':'D','1':'D','2':'D','3':'D','4':'D','5':'D','6':'D','7':'D','8':'D','9':'D',
            # Symbols
            '\"':'\"','.':'.',',':',','_':'_','+':'+','-':'-','{':'{','}':'}','=':'=','>':'>','<':'<','*':'*',
            '/':'/',';':';','(':'(',')':')'
        }
        # Table of outputs
        self.states = {
            1: ['Num','int'],         # final
            2: ["erro"],
            3: ["erro"],
            4: ["erro"],
            5: ['Num','exponential'], # final
            6: ['Num','float'],       # final
            7: ["erro"],
            8: ["erro"],
            9: ['Literal',''],        # final
            10:['id',''],             # final
            11:["erro"],
            12:["erro"],
            13:['Comentario',''],     # final
            14:["erro"],
            15:['OPR',''], # final
            16:['OPR',''], # final
            17:['OPR',''], # final
            18:['OPR',''], # final
            19:['OPR',''], # final
            20:['OPR',''], # final
            21:['RCB',''], # final
            22:['OPM',''], # final
            23:['AB_P',''],# final
            24:['FC_P',''],# final
            25:['PT_V',''] # final
        }

        # Table of errors
        self.errors = {
            0:"Lexical error, invalid symbol to start, at ",
            2:"Lexical error, invalid format in float number, put some numbers after dot at ",
            3:"Lexical error, invalid format in exponential number, put some number after \"e\" or \"E\", at ",
            4:"Lexical error, invalid format in exponential number, put some number after \"+\" or \"-\", at ",
            8:"Lexical error, you need to close \" at ",
            13:"Lexical error, you need to close } at "
            #14:"Lexical error",
        }

        # Table of transitions
        self.table = {
            0: {'D':1, '\"':7, 'L':10,'e':10,'E':10, '{':11, '>':19, '<':15, '=':18,
        		';':25, '(':23, ')':24, '+':22, '-':22, '*':22, '/':22},
            1: {'D':1, 'E':3, 'e':3, '.':2}, # final
            2: {'D':6},
            3: {'+':4, '-':4, 'D':5 },
            4: {'D':5},
            5: {'D':5}, # final
            6: {'D':6, 'E':3, 'e':3}, # final
            #7:{'\"':9},
            #8:{'\"':9},
            10:{'L':10, 'D':10, 'e':10,'E':10 , '_':10}, # final
            #11:{'}':13},
            #12:{'}':13},
            15: {'-':21, '=':17, '>':16}, # final
            19:{'=':20} # final
        }

    # ------------------------Get the source file-------------------------------
    def get_file(self,path):
        self.f = open(path, 'r')
        self.content = self.f.read()
        self.treat_file()


    def treat_file(self):
        #self.content = self.content.replace("\""," \" ")
        self.content = self.content.replace(";"," ; ")
        self.content = self.content.replace("="," = ")
        self.content = self.content.replace("<"," < ")
        self.content = self.content.replace(">"," > ")
        self.content = self.content.replace("="," = ")
        self.content = self.content.replace("<  >"," <> ")
        self.content = self.content.replace("{"," { ")
        self.content = self.content.replace("}"," } ")
        self.content = self.content.replace("("," ( ")
        self.content = self.content.replace(")"," ) ")
        self.content = self.content.replace("/"," / ")
        self.content = self.content.replace("*"," * ")
        self.content = self.content.replace("+"," + ")
        self.content = self.content.replace("e + ","e+")
        self.content = self.content.replace("E + ","E+")
        self.content = self.content.replace("-"," - ")
        self.content = self.content.replace("e - ","e-")
        self.content = self.content.replace("E - ","E-")
        self.content = self.content.replace("<  -"," <- ")
        #print(self.content)


    # --------------------Analyze the sorce file--------------------------------
    def analyze(self):
        self.count_line  = 1
        self.count_column= 1
        self.error = False
        source = self.content.splitlines()
        for line in source:
            line = line.split()
            for word in line:
                for letter in word:
                    self.treat(letter)
                if not(self.error):
                    token = self.states[self.state][:] # Verify token
                    if not(token[0] == "erro"): self.make_tokens_list(token)
                    else:
                        self.print_error()
                        return None
                else:
                    self.print_error()
                    return None
                self.count_column += 1
            self.count_line += 1
        if not(self.error): print("tokens: "+str(self.tokens))
        self.f.close()

    #-------------------Deal with the letter------------------------------------
    def treat(self, letter):
        if(letter == '\"'): self.flag_literal = True
        elif(letter == '{'): self.flag_comment = True
        else:
            if(self.flag_comment):
                print("entrou comentario")
                self.get_comment(letter)
            elif(self.flag_literal):
                print("entrou literal")
                self.get_literal(letter)
            else:
                self.get_state(letter)

    #---------------------Get the literals--------------------------------------
    def get_literal(self,letter):
        self.buffer += letter
        if(letter == '\"'):
            self.state = 9
            self.flag_literal = False
        else: self.state = 8

    #-------------------Get the comments----------------------------------------
    def get_comment(self,letter):
        self.buffer += letter
        if(letter == '}'):
            self.state = 13
            self.flag_comment = False
        else: self.state = 12

    # --------------------Get the state of ending of token----------------------
    def get_state(self,letter):
        self.buffer += letter # Make a buffer
        try:
            symbol = self.symbols[letter] # Verify the symbols
            try:
                self.state = self.table[self.state][symbol] # Verify the states
            except:
                self.error = True
                return None
        except:
            print("\n"+letter+" is a invalid symbol in line "+
                str(self.count_line)+" in column "+str(self.count_column)+"\n")
            self.error = True
            return None

    #---------------- Print erro's message--------------------------------------
    def print_error(self):
        print(self.state)
        print("\n"+self.errors[self.state]+self.buffer+
            " in line "+str(self.count_line)+
            " in column "+str(self.count_column)+"\n")

    #------------------Make the list of tokens----------------------------------
    def make_tokens_list(self,token):
        token.append(self.buffer)
        self.tokens.append(token)
        self.buffer = ""
        self.state = 0


    # ---------------------Return the next token of the list--------------------
    def next_token(self):
        if not(self.error):        # Verify if there is an error
            return self.tokens.pop(0)   # Remove and return the first element
        else: return None
