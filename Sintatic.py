from Lexical import Lexical
import pandas as pd

def main():
    # Lexical
    lx = Lexical()
    lx.get_file('source.txt')

    # Import csv
    ACTION = pd.read_csv('terminals.csv', index_col=0)
    GOTO = pd.read_csv('non_terminals.csv', index_col=0)
    produtions = pd.read_csv('produtions.csv', index_col=0)

    # Variables
    stack = [0]

    #------------------Sintatic algorithm - Shift Reduce------------------------
    a = lx.next_token()
    print(a[0])
    while True:
        s = stack[-1]                           # Seja s o estado no topo da pilha
        if ACTION.loc[s, a[0]][0] is 'S':       # shift t
            t = ACTION.loc[s, a[0]][1:]         # Recebe estado da ação
            stack.append(int(t))                # Empilha t na pilha
            a = lx.next_token()                 # Seja a o proximo simbulo da entrada
        elif ACTION.loc[s, a[0]][0] is 'R':     # reduce A -> B
            prod = int(ACTION.loc[s, a[0]][1:]) # Recebe o numero da produção
            for i in range(len(produtions.loc[prod,'produtions'].split())):
                stack.pop()                     # Desempilhe o simbulo B da pilha
            t = int(stack[-1])                  # Faça o estado t ser o topo da pilha
            stack.append(int(GOTO.loc[t,produtions.loc[prod,'non_terminal']])) # Empilhe GOTO[t,A] na pilha
            print(produtions.loc[int(prod),'non_terminal']+" -> "+produtions.loc[int(prod),'produtions']) # Imprima a producao
        elif ACTION.loc[s, a] == 'accept':
            break
        else:
            recovery()


if __name__ == "__main__":
    main()

def recovery():
    # TODO recovery
    print("Error")
