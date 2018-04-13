
class Lexical(object):

    def __init__(self):
        # Initialize variables
        self.buffer = ""
        self.state = 0
        self.tokens = list()
        self.error = False

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
            '/':'/',';':';','(':'(',')':')',' ':'end'
        }
        # Table of outputs
        self.states = {
            1: ['Num','int'],    # final
            2:"Lexical error, invalid format in float number, put some numbers after dot, at ",
            3:"Lexical error, invalid format in exponential number, put some number after \"e\" or \"E\", at ",
            4:"Lexical error, invalid format in exponential number, put some number after \"+\" or \"-\", at ",
            5: ['Num','exponential'], # final
            6: ['Num','float'],       # final
            7:"Lexical error, you need to close \" at ",
            8:"Lexical error, you need to close \" at ",
            9: ['Literal'],           # final
            10:['id'],                # final
            11:"Lexical error, you need to close } at ",
            12:"Lexical error, you need to close } at ",
            13:['Comentario',''],     # final
            #14:"Lexical error",
            15:['OPR'], # final
            16:['OPR'], # final
            17:['OPR'], # final
            18:['OPR'], # final
            19:['OPR'], # final
            20:['OPR'], # final
            21:['RCB'], # final
            22:['OPM'], # final
            23:['AB_P'],# final
            24:['FC_P'],# final
            25:['PT_V'] # final
        }
        # Table of transitions
        self.table = {
            0: {'D':1, '\"':7, 'L':10,'e':10,'E':10, '{':11, '>':19, '<':15, '=':18,
        		';':25, '(':23, ')':24, '+':22, '-':22, '*':22, '/':22},
            1: {'D':1, 'E':3, 'e':3, '.':2,'end':1}, # final
            2: {'D':6 },
            3: {'+':4, '-':4, 'D':5 },
            4: {'D':5 },
            5: {'D':5,'end':5}, # final
            6: {'D':6, 'E':3, 'e':3,'end':6}, # final
            7:{'\"':9},
            8:{'\"':9},
            9:{'end':9}, # final
            10: {'L':10, 'D':10, 'e':10,'E':10 , '_':10,'end':10}, # final
            11:{'}':13},
            12:{'}':13},
            13:{'end':13}, # final
            #14:
            15: {'-':21, '=':17, '>':16,'end':15}, # final
            16:{'end':16}, # final
            17:{'end':17}, # final
            18:{'end':18}, # final
            19:{'=':20,'end':19}, # final
            20:{'end':20}, # final
            21:{'end':21}, # final
            22:{'end':22}, # final
            23:{'end':23}, # final
            24:{'end':24}, # final
            25:{'end':25} # final
        }

    # ------------------------Get the source file-------------------------------
    def get_file(self,path):
        self.f = open(path, 'r')
        self.content = self.f.read()
        self.content = self.content.replace("\n"," \n ") # Remove uselles spaces
        print(repr(self.content)) # raw file

    # --------------------Analyze the sorce file--------------------------------
    def analyze(self):
        #lines = content.splitlines()
        #words = lines.split()
        for words in self.content:
            #words = words.replace('\n',' ') # Remove end lines \n
            for letter in words:
                try:
                    self.buffer += letter                       # Make a buffer
                    self.buffer = self.buffer.replace(' ','')   # Remove uselles spaces
                    symbol = self.symbols[letter]               # Verify the symbols
                    self.state = self.table[self.state][symbol] # Verify the states
                    token = self.states[self.state][:]
                    if (symbol == 'end'):
                        token.append(self.buffer)
                        self.tokens.append(token)
                except:
                    if(token[:7] == "Lexical"):
                        print(token +str(self.buffer))

            self.buffer = ""
            self.state = 0
        print("tokens: "+str(self.tokens))
        self.f.close()

    # ---------------------Return the next token of the list--------------------
    def next_token(self):
        if(self.error == False):        # Verify if there is an error
            return self.tokens.pop(0)   # Remove and return the first element
        else: return "error"
