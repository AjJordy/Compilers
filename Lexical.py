import queue

class Lexical(object):

    def __init__(self):

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
            5: ['Num',''],       # final
            6: ['Num','float'],  # final
            7:"Lexical error, you need to close \" at ",
            8:"Lexical error, you need to close \" at ",
            9: ['Literal',''],   # final
            10:['id',''],        # final
            11:"Lexical error, you need to close } at ",
            12:"Lexical error, you need to close } at ",
            13:['Comentario',''],# final
            #14:"Lexical error",
            15:['OPR',''],       # final
            16:['OPR',''],       # final
            17:['OPR',''],       # final
            18:['OPR',''],       # final
            19:['OPR',''],       # final
            20:['OPR',''],       # final
            21:['RCB',''],       # final
            22:['OPM',''],       # final
            23:['AB_P',''],      # final
            24:['FC_P',''],      # final
            25:['PT_V','']       # final
        }
        # Table of transitions
        self.table = {
            0: {'D':1, '\"':7, 'L':10,'e':10,'E':10, '{':11, '>':19, '<':15, '=':18,
        		';':25, '(':23, ')':24, '+':22, '-':22, '*':22, '/':22, ' ':0,'\n':0,'\t':0},
            1: {'D':1, 'E':3, 'e':3, '.':2, ' ':0,'\n':0,'\t':0}, # final
            2: {'D':6 , ' ':0,'\n':0,'\t':0},
            3: {'+':4, '-':4, 'L':5 , ' ':0,'\n':0,'\t':0},
            4: {'D':5 , ' ':0,'\n':0,'\t':0},
            5: {'D':5, ' ':0,'\n':0,'\t':0}, # final
            6: {'D':6, 'E':3, 'e':3, ' ':0,'\n':0,'\t':0}, # final
            #7:
            #8:
            #9: # final
            10: {'L':10, 'D':10, 'e':10,'E':10 , '_':10, ' ':0,'\n':0,'\t':0}, # final
            #11:
            #12:
            #13: # final
            #14:
            15: {'-':21, '=':17, '>':16, ' ':0,'\n':0,'\t':0}, # final
            #16: # final
            #17: # final
            #18: # final
            19: {'=':20, ' ':0,'\n':0,'\t':0}, # final
            #20: # final
            #21: # final
            #22: # final
            #23: # final
            #24: # final
            #25: # final
        }

        # Initialize variables
        self.buffer = ""
        self.symbol = ""
        self.state = 0
        self.count_line = 1
        self.tokens = queue.Queue()

    # Get the source file
    def get_file(self,path):
        self.f = open(path, 'r')
        self.content = self.f.read()

    # Analyze the sorce file
    def analyze(self):
        #lines = content.splitlines()
        #words = lines.split()
        for words in self.content:
            words = words.replace('\n',' ') # Remove end lines \n
            for letter in words:
                try:
                    print(self.state)
                    self.buffer += letter                       # Make a buffer
                    self.buffer = self.buffer.replace(' ','')   # Remove uselles spaces
                    symbol = self.symbols[letter]               # Verify the symbols
                    self.state = self.table[self.state][symbol] # Verify the states
                    print(self.buffer)
                except:
                    token = self.states[self.state]
                    if(token[:7] == "Lexical"):
                        print(token +str(self.buffer))
                        break
                    else:
                        print("buffer")
                        print(self.buffer)
                        print("token1: "+str(token))
                        self.tokens.put(token.append(self.buffer))
                        print("token2: "+str(token))

                    self.buffer = ""
                    self.state = 0
        #print(repr(content)) # raw file
        self.f.close()

    def next_token(self):
        return self.tokens.get()
