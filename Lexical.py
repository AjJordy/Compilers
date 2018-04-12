#class Lexical(object):

    #def get_file(self):
    #def __init__(self,path):

symbols = {
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

states = {
    1: ['Num','int'],    # final
    2:"Lexical error",
    3:"Lexical error",
    4:"Lexical error",
    5: ['Num',''],       # final
    6: ['Num','float'],  # final
    7:"Lexical error",
    8:"Lexical error",
    9: ['Literal',''],   # final
    10:['id',''],        # final
    11:"Lexical error",
    12:"Lexical error",
    13:['Comentario',''],# final
    14:"Lexical error",
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
    #TODO: EOF
}

table = {
    0: {'D':1, '\"':7, 'L':10,'e':10,'E':10, '{':11, '>':19, '<':15, '=':18,
		';':25, '(':23, ')':24, '+':22, '-':22, '*':22, '/':22},
    1: {'D':1, 'E':3, 'e':3, '.':2}, # final
    2: {'D':6 },
    3: {'+':4, '-':4, 'L':5 },
    4: {'D':5 },
    5: {'D':5}, # final
    6: {'D':6, 'E':3, 'e':3}, # final
    #7:
    #8:
    #9: # final
    10: {'L':10, 'D':10, 'e':10,'E':10 , '_':10}, # final
    #11:
    #12:
    #13: # final
    #14:
    15: {'-':21, '=':17, '>':16}, # final
    #16: # final
    #17: # final
    #18: # final
    19: {'=':20}, # final
    #20: # final
    #21: # final
    #22: # final
    #23: # final
    #24: # final
    #25: # final

}

f = open('source.txt', 'r')
content = f.read()

lines = content.splitlines()
#words = lines.split()

buffer = ""
symbol = ""
state = 0


for words in lines:
    #words = lines[i].split()
    for letter in words:
        try:
            print(state)
            buffer += letter
            symbol = symbols[letter]
            state = table[state][symbol]
            print("Letra: "+letter)
            print(buffer)
        except:
            buffer = ""
            state = 0
            print(states[state])
    #buffer = ""

#print(repr(content)) # raw file
f.close()

#w = '>'
#print(table[w])
