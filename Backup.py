
class Backup(object):

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
            '/':'/',';':';','(':'(',')':')'
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
            1: {'D':1, 'E':3, 'e':3, '.':2}, # final
            2: {'D':6 },
            3: {'+':4, '-':4, 'D':5 },
            4: {'D':5 },
            5: {'D':5}, # final
            6: {'D':6, 'E':3, 'e':3}, # final
            7:{'\"':9},
            8:{'\"':9},
            #9: # final
            10: {'L':10, 'D':10, 'e':10,'E':10 , '_':10}, # final
            11:{'}':13},
            12:{'}':13},
            #13: # final
            #14:
            15: {'-':21, '=':17, '>':16}, # final
            #16: # final
            #17: # final
            #18: # final
            19: {'=':20}, # final
            #20: # final
            #21: # final
            #22:  # final
            #23: # final
            #24: # final
            #25: # final
        }

    # ------------------------Get the source file-------------------------------
    def get_file(self,path):
        self.f = open(path, 'r')
        self.content = self.f.read()
        self.content = self.content.replace(' \n','\n') # Remove uselles spaces
        print(repr(self.content)) # raw file

    # --------------------Analyze the sorce file--------------------------------
    def analyze(self):
        #lines = content.splitlines()
        #words = lines.split()
        for words in self.content:
            words = words.replace('\n',' ') # Remove end lines \n
            for letter in words:
                try:
                    self.classify(letter)
                except:
                    self.make_list()
        print("tokens: "+str(self.tokens))
        self.f.close()

    # -----------------------Classify the token---------------------------------
    def classify(self,letter):
        #print(self.state)
        self.buffer += letter                       # Make a buffer
        self.buffer = self.buffer.replace(' ','')   # Remove uselles spaces
        if not (self.state == 7) or (self.state == 8) or (self.state == 11) or (self.state == 12):
            symbol = self.symbols[letter]               # Verify the symbols
            self.state = self.table[self.state][symbol] # Verify the states
            #print(self.buffer)
        else:
            symbol = letter
            self.state = self.table[self.state][symbol] # Verify the states

    # -------------Make the list of tokens or return erro-----------------------
    def make_list(self):
        token = self.states[self.state][:]  # Make a copy of a list
        if(token[:7] == "Lexical"):
            print(token + str(self.buffer))
            self.error = True               # Lexical error
        else:
            #print("buffer: "+str(self.buffer))
            token.append(self.buffer)
            self.tokens.append(token)
            #print("token: "+str(token))
        self.buffer = ""
        self.state = 0

    # ---------------------Return the next token of the list--------------------
    def next_token(self):
        if(self.error == False):        # Verify if there is an error
            return self.tokens.pop(0)
        else: return "error"
