class Lexical(object):

    def __init__(self):
        # Initialize variables
        self.buffer = ""
        self.state = 0
        self.tokens = list()
        self.position = 0
        self.count_line = 0
        self.count_column = 0


        self.symbols_table = {
            'inicio':['inicio','','inicio'],
            'varinicio':['varinicio','','varinicio']
            # TODO resto
        }

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
            '/':'/',';':';','(':'(',')':')', 'whitespace':'whitespace'
        }
        # Table of outputs\
        self.states = {
            1: ['Num','int'],         # final
            2: ["erro"],
            3: ["erro"],
            4: ["erro"],
            5: ['Num','real'], # final
            6: ['Num','real'],       # final
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
            25:['PT_V',''], # final
            26:['EOF','']
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
            0:{'D':1, '\"':7, 'L':10,'e':10,'E':10, '{':11, '>':19, '<':15, '=':18,
        		';':25, '(':23, ')':24, '+':22, '-':22, '*':22, '/':22,'\\n':0,' ':0,
                'EOF':26,'whitespace':0},
            1:{'D':1,'E':3,'e':3,'.':2}, # final
            2:{'D':6},
            3:{'+':4, '-':4, 'D':5 },
            4:{'D':5},
            5:{'D':5}, # final
            6:{'D':6,'E':3,'e':3}, # final
            7:{'\"':9},
            8:{'\"':9},
            10:{'L':10, 'D':10, 'e':10,'E':10 , '_':10}, # final
            11:{'D':12, '\"':12, 'L':12,'e':12,'E':12, '{':12, '>':13, '<':12, '=':13,
        	 	';':13, '(':13, ')':13, '+':13, '-':13, '*':13, '/':13,'\\n':13,' ':13},
            12:{'D':13, '\"':13, 'L':13,'e':13,'E':13, '{':13, '>':13, '<':15, '=':13,
        	 	';':13, '(':13, ')':13, '+':13, '-':13, '*':13, '/':13,'\\n':13,' ':13},
            # 13:{'D':13, '\"':13 'L':13,'e':13,'E':13, '{':13, '>':13, '<':15, '=':13,
        	# 	';':13, '(':13, ')':13, '+':13, '-':13, '*':13, '/':13,'\\n':13,' ':13},
            14:{'D':1, 'E':3, 'e':3, '.':2},
            15:{'-':21, '=':17, '>':16}, # final
            19:{'=':20}, # final


        }


    # ------------------------Get the source file-------------------------------
    def get_file(self,path):
        self.f = open(path, 'r')


    def next_token(self):
        self.state = 0
        self.buffer = ""
        while(True):
            self.position = self.f.tell()
            self.content = self.f.read(1)
            self.count_column += 1

            if(self.content in [' ','\t','\n']):
                symbol = "whitespace"
            elif(self.content): symbol = self.symbols[self.content]
            else: symbol = "EOF"

            try:
                self.state = self.table[self.state][symbol]
                if not(symbol == "whitespace"): self.buffer += self.content
                if(self.content in ['\n']):
                    self.count_line += 1
                    self.count_column = 1
            except:
                token = self.states[self.state][:]
                self.f.seek(self.position)
                self.count_column -= 1
                if(token[0] == "erro"):
                    self.print_error()
                    token.append(self.errors[self.state])
                    token.append(self.count_line)
                    token.append(self.count_column)
                else: # if state is final
                    token.append(self.buffer)
                    if(token[0] == 'id'):
                        if(self.buffer in self.symbols_table):
                            return self.symbols_table[self.buffer]
                        else:
                            self.symbols_table[self.buffer] = token
                return token



    #---------------- Print erro's message--------------------------------------
    def print_error(self):
        print("\n"+self.errors[self.state]+self.buffer+
            " in line "+str(self.count_line)+
            " in column "+str(self.count_column)+"\n\n")
