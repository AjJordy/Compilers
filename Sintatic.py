from Lexical import Lexical
import pandas as pd

if __name__ == "__main__":
    main()

def main():

    # Lexical
    lx = Lexical()
    lx.get_file('source.txt')

    # Import csv
    GOTO = pd.read_csv('non_terminals.csv')
    ACTION = pd.read_csv('terminals.csv')

    # Variables
    stack = []
    state = 0

    #-----------------------Sintatic algorithm----------------------------------
    a = lx.next_token()
    while(True):
        state = stack.top()               # Seja s o estado no topo da pilha
        if (ACTION.loc[state,a[0]] = shift t):
            stack.push(t)                 # Empilha t na pilha
            a = lx.next_token()           # Seja a o proximo simbulo da entrada
        elif(ACTION.loc[state,a[0]] = reduce A -> B):
            stack.pop()                   # Desempilhe o simbulo B da pilha
            stack.push(t);                # Faça o estado t ser o topo da pilha
            stack.push(GOTO.loc[t,a[0]])  # Empilhe GOTO[t,A] na pilha
            print(produtions[production]) # Imprima a producao
        elif(ACTION.loc[state,a] = 'accept'): break
        else recovery()

def recovery():
    # TODO recovery
    print("Error")

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
