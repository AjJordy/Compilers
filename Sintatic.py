from Lexical import Lexical
import pandas as pd


# ------------------------  Recuperação de erro - Panic Mode  --------------------------
def panic(a,lx):
    while a[2] is not ";":
        if a[0] is not 'EOF':
            a = lx.next_token()
        else:
            return 'end'
    return a


# ------------------------   Determina quantos estados desempilhar  ----------------------------
def pop(produtions,prod,pilha):
    for i in range(len(produtions.loc[prod, 'produtions'].split())):
        pilha.pop()  # Desempilha o tamanho da produção

def popN(n,pilha):
    for i in n:
        x = pilha.pop()
    return x

# -----------------------------  Tradução dirigida  ------------------------------------
def semantic(prod,file,ss,a,lx):  # Numero da produção, arquivo final, pilha semântica, ultimo token, objeto lexico

    if prod is 5:
        file.write("\n\n\n")
    elif prod is 6:
        lx.symbols_table[a[0]][1] = ss.pop()[1]  # id.tipo <- TIPO.tipo
        ss.append(lx.symbols_table[a])
        file.write(lx.symbols_table[a[0]][1]," ",lx.symbols_table[a[0]][2],";\n")  # Imprimir ( TIPO.tipo id.lexema ; )
    elif prod is 7:
        TIPO = ['TIPO','','TIPO']
        TIPO[1] = ss.pop()[1]       # TIPO.tipo <- int.tipo
        ss.append(TIPO)
    elif prod is 8:
        TIPO = ['TIPO', '', 'TIPO']
        TIPO[1] = ss.pop()[1]       # TIPO.tipo <- real.tipo
        ss.append(TIPO)
    elif prod is 9:
        TIPO = ['TIPO', '', 'TIPO']
        TIPO[1] = ss.pop()[1]       # TIPO.tipo <- lit.tipo
        ss.append(TIPO)
    elif prod is 11:
        if lx.symbols_table[a[0]][1] is not '':
            if lx.symbols_table[a[0]][1] is "lit":
                file.write("\tscanf(“%s”,",lx.symbols_table[a[0]][2],");\n")
            elif lx.symbols_table[a[0]][1] is "int":
                file.write("\tscanf(“%d”,", lx.symbols_table[a[0]][2], ");\n")
            elif lx.symbols_table[a[0]][1] is "real":
                file.write("\tscanf(“%lf”,", lx.symbols_table[a[0]][2], ");\n")
        else:
            print("\nErro: Variável não declarada\n")
    elif prod is 12:
        file.write("\tprintf(",ss[-1][2],");\n")
    elif prod is 13:
        ARG = ss.pop()      # ARG.atributos <- literal.atributos
        ss.append(ARG)
    elif prod is 14:
        ARG = ss.pop()      # ARG.atributos <- num.atributos
        ss.append(ARG)
    elif prod is 15:
        if lx[a][1] is not '':
            ARG = ss.pop()  # ARG.atributos <- id.atributos
            ss.append(ARG)
        else:
            print("\nErro: Variável não declarada\n")
    elif prod is 17:
        if lx[a][1] is not '':
            LD = ss.pop()
            rcb = ss.pop()
            if LD[1] is rcb[1]:
                file.write(lx[a[1][2]," ",rcb[1]," ",LD[2]])  # id.lexema rcb.tipo LD.lexema
            else:
                print("\nErro: Tipos diferentes para atribuição\n")
        else:
            print("\nErro: Variável não declarada\n")
    # elif prod is 18:

    elif prod is 19:
        LD = ss.pop()  # LD.atributos <- OPRD.atributos
        ss.append(LD)
    elif prod is 20:
        if lx[a][1] is not '':
            OPRD = ss.pop() # OPRD.atributos <- id.atributos
            ss.append(OPRD)
        else:
            print("\nErro: Variável não declarada.\n")
    elif prod is 21:
        OPRD = ss.pop()  # OPRD.atributos <- num.atributos
        ss.append(OPRD)
    elif prod is 23:
        file.write("}\n")
    elif prod is 24:
        EXP_R = ss.popN(3,ss)
        file.write("if(",EXP_R[2],"){\n")
    # elif prod is 25:






# ------------------------ Inicializa o arquivo em linguagem C ---------------------------------
def initFile():
    file = open("PROGRAMA.c","w")
    file.write("#include<stdio.h>\ntypedef char literal[256];\n\nvoid main(void){\n\t/*----Variaveis temporarias----*/\n")
    return file


def main():
    # Lexical
    lx = Lexical()
    lx.get_file('source.txt')

    # Import csv
    ACTION = pd.read_csv('terminals.csv', index_col=0)
    GOTO = pd.read_csv('non_terminals.csv', index_col=0)
    produtions = pd.read_csv('produtions.csv', index_col=0)

    # Variables
    stack = [0]  # States stack
    ss = []      # Semantic stack

    # Final source
    file = initFile()

    #------------------Sintatic algorithm - Shift Reduce------------------------
    a = lx.next_token()
    while True:
        try:
            s = stack[-1]                           # Seja s o estado no topo da pilha
            #print(a)
            # --------------------- Shift t ------------------------------------
            if ACTION.loc[s, a[0]][0] is 'S':
                t = ACTION.loc[s, a[0]][1:]         # Recebe estado da ação
                stack.append(int(t))                # Empilha t na pilha
                a = lx.next_token()                 # Seja a o proximo simbulo da entrada

                ''' --- Semantic ---- '''
                ss.append(a)

            # --------------------- Reduce A -> B -----------------------------
            elif ACTION.loc[s, a[0]][0] is 'R':
                prod = int(ACTION.loc[s, a[0]][1:])  # Recebe o numero da produção
                pop(produtions,prod,stack)

                t = int(stack[-1])  # Faça o estado t ser o topo da pilha
                stack.append(int(GOTO.loc[t,produtions.loc[prod,'non_terminal']]))  # Empilhe GOTO[t,A] na pilha
                print(produtions.loc[int(prod),'non_terminal']+" -> "+produtions.loc[int(prod),'produtions'])  # Imprime a producao

                ''' ---- Semantic ----- '''
                semantic(prod,file,ss,a,lx)

            # -------------------------- Accept -------------------------------
            elif ACTION.loc[s, a[0]] == 'accept':
                file.close()
                break

        except:
            print("\nSintatic error at line " + str(a[3]) + " at column " + str(a[4]), "\n")
            # a = panic(a,lx)
            # if a is 'end':
            #     break
            # else:
            #     continue
            break


if __name__ == "__main__":
    main()

