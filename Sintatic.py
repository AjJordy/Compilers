from Lexical import Lexical

if __name__ == "__main__":
    main()

def main():
    lx = Lexical()
    lx.get_file('source.txt')

    stack = []

    a = lx.next_token()
    while(True):
        s = stack.top()                   # Seja s o estado no topo da pilha
        if (ACTION[s,a] = shift t):
            stack.push(t)                 # Empilha t na pilha
            a = lx.next_token()           # Seja a o proximo simbulo da entrada
        elif(ACTION[s,a] = reduce A -> B):
            stack.pop()                   # Desempilhe o simbulo B da pilha
            stack.push(t);                # Faça o estado t ser o topo da pilha
            stack.push(GOTO[t,A])        # Empilhe GOTO[t,A] na pilha
            print(produtions[production]) # Imprima a producao
        elif(ACTION[s,a] = 'accept'): break
        else recovery()

def recovery():

produtions = {
    1:'P\'-> P',
    2:'P -> inicio V A',
    3:'V -> varinicio LV',
    4:'LV -> D LV',
    5:'LV -> varfim;',
    6:'D -> id TIPO;',
    7:'TIPO -> int',
    8:'TIPO -> real',
    9:'TIPO -> lit',
    10:'A -> ES A',
    11:'ES -> leia id;',
    12:'ES -> escreva ARG;',
    13:'ARG -> literal',
    14:'ARG -> num',
    15:'ARG -> id',
    16:'A -> CMD A',
    17:'CMD -> id rcb LD;',
    18:'LD -> OPRD opm OPRD',
    19:'LD -> OPRD',
    20:'OPRD -> id',
    21:'OPRD -> num',
    22:'A -> COND A',
    23:'COND -> CABEÇALHO CORPO',
    24:'CABEÇALHO -> se [EXP_R] então',
    25:'EXP_R -> OPRD opr OPRD',
    26:'CORPO -> ES CORPO',
    27:'CORPO -> CMD CORPO',
    28:'CORPO -> COND CORPO',
    29:'CORPO -> fimse',
    30:'A -> fim'
}

GOTO = {
    0:{'P':1},
    2:{'V':3},
    3:{'A':9,'ES':10,'CMD':15,'COND':14,'CABEÇALHO':13},
    4:{'LV':5,'D':6},
    6:{'LV':24,'D':6},
    7:{'TIPO':20},
    10:{'A':25,'ES':10,'CMD':15,'COND':14,'CABEÇALHO':13},
    12:{'ARG':29},
    13:{'ES':41,'CMD':44,'COND':43,'CABEÇALHO':13,'CORPO':40},
    14:{'A':27,'ES':10,'CMD':15,'COND':14,'CABEÇALHO':13},
    15:{'A':26,'ES':10,'CMD':15,'COND':14,'CABEÇALHO':13},
    28:{'OPRD':48,'EXP_R':34},
    37:{'LD':51,'OPRD':54},
    41:{'ES':41,'CMD':44,'COND':43,'CABEÇALHO':13},
    43:{'ES':41,'CMD':44,'COND':43,'CABEÇALHO':13,'CORPO':45},
    44:{'ES':41,'CMD':44,'COND':43,'CABEÇALHO':13,'CORPO':58},
    49:{'OPRD':57},
    55:{'OPRD':56}
}
