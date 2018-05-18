class Lexical(object):

    def __init__(self):

        #------------------------ Initialize variables--------------------------
        self.buffer = ""
        self.state = 0
        self.tokens = list()
        self.position = 0
        self.count_line = 1
        self.count_column = 1

        #-----------------------Table of identifiers----------------------------
        self.symbols_table = {
            'inicio':['inicio','','inicio'],
            'varinicio':['varinicio','','varinicio'],
            'varfim':['varfim','','varfim'],
            'escreva':['escreva','','escreva'],
            'leia':['leia','','leia'],
            'se':['se','','se'],
            'entao':['entao','','entao'],
            'senao':['senao','','senao'],
            'fimse':['fimse','','fimse'],
            'fim':['fim','','fim'],
            'Inteiro':['Inteiro','','Inteiro'],
            'literal':['literal','','literal'],
            'real':['real','','real']
        }

        # ----------------------Table of symbols capable to read----------------
        self.symbols = {
            # Alphabet lower case
            'a':'L','b':'L','c':'L','d':'L','e':'e','f':'L','g':'L','h':'L','i':'L',
            'j':'L','k':'L','l':'L','m':'L','n':'L','o':'L','p':'L','q':'L','r':'L',
            's':'L','t':'L','u':'L','v':'L','x':'L','w':'L','y':'L','z':'L',
            # Alphabet upper case
            'A':'L','B':'L','C':'L','D':'L','E':'E','F':'L','G':'L','H':'L','I':'L',
            'J':'L','K':'L','L':'L','M':'L','N':'L','O':'L','P':'L','Q':'L','R':'L',
            'S':'L','T':'L','U':'L','V':'L','X':'L','W':'L','Y':'L','Z':'L',
            # Numbers
            '0':'D','1':'D','2':'D','3':'D','4':'D','5':'D','6':'D','7':'D','8':'D','9':'D',
            # Symbols
            '\"':'\"','.':'.',',':',','_':'_','+':'+','-':'-','{':'{','}':'}','=':'=',
            '>':'>','<':'<','*':'*','/':'/',';':';','(':'(',')':')',':':':','\\':'\\',
            'whitespace':'whitespace'
        }

        # -----------------------Table of outputs-------------------------------
        self.states = {
            1: ['Num','int'],# final
            2: ["erro"],
            3: ["erro"],
            4: ["erro"],
            5: ['Num','real'],# final
            6: ['Num','real'],# final
            7: ["erro"],
            8: ["erro"],
            9: ['Literal',''],# final
            10:['id',''],# final
            11:["erro"],
            12:["erro"],
            13:['Comentario',''],# final
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
            26:['EOF',''],
            30:'erro'
        }

        # ---------------------------Table of errors----------------------------
        self.errors = {
            0:"Lexical error, invalid symbol to start, at ",
            2:"Lexical error, invalid format in real number, put some numbers after dot at ",
            3:"Lexical error, invalid format in real number, put some number after \"e\" or \"E\", at ",
            4:"Lexical error, invalid format in real number, put some number after \"+\" or \"-\", at ",
            7:"Lexical error, you need to close \" at ",
            8:"Lexical error, you need to close \" at ",
            11:"Lexical error, you need to close } at ",
            12:"Lexical error, you need to close } at ",
            30:"Lexical error, symbol doesn't allow "
        }

        # ------------------------Table of transitions--------------------------
        self.table = {
            0:{'D':1, '\"':7, 'L':10,'e':10,'E':10, '{':11, '>':19, '<':15, '=':18,
        		';':25, '(':23, ')':24, '+':22, '-':22, '*':22, '/':22,
                'EOF':26,'whitespace':0},
            1:{'D':1,'E':3,'e':3,'.':2}, # final
            2:{'D':6},
            3:{'+':4, '-':4, 'D':5 },
            4:{'D':5},
            5:{'D':5}, # final
            6:{'D':6,'E':3,'e':3}, # final
            7:{'\"':9,'D':8, 'L':8,'e':8,'E':8, '>':8, '<':8, '=':8,':':8,
        	 	';':8, '(':8, ')':8, '+':8, '-':8, '*':8, '/':8,'whitespace':8},
            8:{'\"':9,'D':8, 'L':8,'e':8,'E':8, '>':8, '<':8, '=':8,':':8,
        	 	';':8, '(':8, ')':8, '+':8, '-':8, '*':8, '/':8,'whitespace':8},
            10:{'L':10, 'D':10, 'e':10,'E':10 , '_':10}, # final
            11:{'}':13,'D':12, '\"':12, 'L':12,'e':12,'E':12, '{':12, '>':12, '<':12, '=':12,
                ':':12,';':12, '(':12, ')':12, '+':12, '-':12, '*':12, '/':12,'whitespace':12},
            12:{'}':13,'D':12, '\"':12, 'L':12,'e':12,'E':12, '{':12, '>':12, '<':12, '=':12,
                ':':12,';':12, '(':12, ')':12, '+':12, '-':12, '*':12, '/':12,'whitespace':12},
            14:{'D':1, 'E':3, 'e':3, '.':2},
            15:{'-':21, '=':17, '>':16}, # final
            19:{'=':20}, # final
            # 26: "EOF"
        }


    # ------------------------Get the source file-------------------------------
    def get_file(self,path):
        self.f = open(path, 'r')

    #-------------------------Return the next token-----------------------------
    def next_token(self):
        self.state = 0
        self.buffer = ""
        token = []
        while(True):
            self.position = self.f.tell()
            self.content = self.f.read(1) # read one letter
            self.count_column += 1

            # -------------------- Verify the symbol---------------------------
            if(self.content in [' ','\t','\n','\\']):
                symbol = "whitespace"
            elif(self.content):
                try:
                    symbol = self.symbols[self.content]
                except:
                    token.append(self.content)
                    token.append(self.states[30])
                    token.append(self.errors[30])
                    return token
            else:
                symbol = "EOF"

            #----------------------- Make token --------------------------------
            try:
                self.state = self.table[self.state][symbol]
                if (self.state in [7,8,11,12]):
                    self.buffer += self.content
                elif not(symbol == "whitespace"):
                    self.buffer += self.content
                if(self.content in ['\n'] and not self.state in [7,8,11,12]):
                    self.count_line += 1
                    self.count_column = 1
            except:
                token = self.states[self.state][:]
                self.f.seek(self.position)
                self.count_column -= 1
                #----------------- if state isn't final-------------------------
                if(token[0] == "erro"):
                    self.print_error()
                    token.append(self.errors[self.state])
                    token.append(self.count_line)
                    token.append(self.count_column)
                #----------------- if state is final----------------------------
                else:
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
