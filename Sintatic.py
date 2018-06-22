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


# ------------------------ Desempilha o tamanho da produção ----------------------------
def pop(pilha,tamanho):
    lista = []
    for i in range(tamanho):
        lista.append(pilha.pop())
    return lista


# -----------------------------  Tradução dirigida  ------------------------------------
# Numero da produção, arquivo final, pilha semântica, objeto lexico, token não terminal, lista da produção
def semantic(prod,file,ss,lx,token,lenght,T):

    resto = ss[-lenght:]
    ss = ss[:-lenght]
    ss.append(token)

    if prod is 5:
        file.write("\n\n\n")
    elif prod is 6:
        lx.symbols_table[resto[0][2]][1] = resto[1][1]  # id.tipo <- TIPO.tipo
        file.write("\t"+resto[1][1]+" "+resto[0][2]+";\n")   # Imprimir ( TIPO.tipo id.lexema ; )
    elif prod is 7:
        ss[-1][1] = resto[-1][1]  # TIPO.tipo <- int.tipo
    elif prod is 8:
        ss[-1][1] = resto[-1][1]  # TIPO.tipo <- real.tipo
    elif prod is 9:
        ss[-1][1] = resto[-1][1]  # TIPO.tipo <- lit.tipo
    elif prod is 11:
        if resto[-2][1] is not '':
            if resto[-2][1] is "lit":
                file.write("\tscanf(“%s”,&"+resto[-2][2]+");\n")
            elif resto[-2][1] is "int":
                file.write("\tscanf(“%d”,&"+ resto[-2][2]+ ");\n")
            elif resto[-2][1] is "real":
                file.write("\tscanf(“%lf”,&"+ resto[-2][2]+ ");\n")
        else:
            print("\nErro: Variável não declarada\n")
    elif prod is 12:
        file.write("\tprintf("+resto[-2][1]+");\n")
    elif prod is 13:
        token[1:] = resto[-1][2:]   # ARG.atributos <- literal.atributos
        print("new "+str(token))
    elif prod is 14:
        print(lenght)
        print("\n\nResto " + str(resto))
        token[1:] = ss[-1][1:]      # ARG.atributos <- num.atributos
    elif prod is 15:
        if ss[-1][1] is not '':
            token[1:] = ss[-1][1:]  # ARG.atributos <- id.atributos
        else:
            print("\nErro: Variável não declarada\n")
    elif prod is 17:
        if resto[-1][1] is not '':
            if resto[-1][1] is resto[-2][1]:
                file.write(resto[-1][1]+" "+resto[-2][1]+" "+resto[-3][1])  # id.lexema rcb.tipo LD.lexema
            else:
                print("\nErro: Tipos diferentes para atribuição\n")
        else:
            print("\nErro: Variável não declarada\n")
    #elif prod is 18:


    elif prod is 19:
        ss[-1][1:] = ss[-2][1:]  # LD.atributos <- OPRD.atributos
    elif prod is 20:
        if resto[-1][1] is not '':
            token[1:] = resto[-1][1:]  # OPRD.atributos <- id.atributos
        else:
            print("\nErro: Variável não declarada.\n")
    elif prod is 21:
        token[1:] = ss[-2][1:]  # OPRD.atributos <- num.atributos
    elif prod is 23:
        file.write("}\n")
    elif prod is 24:
        # CABEÇALHO <- se ( EXP_R ) entao
        file.write("\tif("+resto[-3][2]+"){\n\t")
    elif prod is 25:
        if resto[-3][1] == resto[-1][1]:
            Tx = str(resto[-3][1])+str(resto[-2][2])+str(resto[-1][1])
            T.append(Tx)
            ss[-1][2] = Tx
            file.write(Tx)
        else:
            print("\nErro: Operandos com tipos incompatíveis\n")

    return ss,T


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
    T = []  # Variáveis temporárias

    # Final source
    file = initFile()

    #------------------Sintatic algorithm - Shift Reduce------------------------
    a = lx.next_token()
    while True:
        #try:
            s = stack[-1]                           # Seja s o estado no topo da pilha
            #print(a)
            # --------------------- Shift t ------------------------------------
            if ACTION.loc[s, a[0]][0] is 'S':
                ''' --- Semantic ---- '''
                ss.append(a)

                t = ACTION.loc[s, a[0]][1:]         # Recebe estado da ação
                stack.append(int(t))                # Empilha t na pilha
                a = lx.next_token()                 # Seja a o proximo simbulo da entrada

            # --------------------- Reduce A -> B -----------------------------
            elif ACTION.loc[s, a[0]][0] is 'R':
                prod = int(ACTION.loc[s, a[0]][1:])  # Recebe o numero da produção
                lenght = len(produtions.loc[prod, 'produtions'].split())
                pop(stack, lenght)

                t = int(stack[-1])  # Faça o estado t ser o topo da pilha
                stack.append(int(GOTO.loc[t,produtions.loc[prod,'non_terminal']]))  # Empilhe GOTO[t,A] na pilha
                print(produtions.loc[int(prod),'non_terminal']+" -> "+produtions.loc[int(prod),'produtions'])  # Imprime a producao

                ''' ---- Semantic ----- '''
                token = [produtions.loc[int(prod),'non_terminal'],'','']  # token não terminal
                #print(token)
                #print(prod)
                #print(lenght)

                ss,T = semantic(prod,file,ss,lx,token,lenght,T)

            # -------------------------- Accept -------------------------------
            elif ACTION.loc[s, a[0]] == 'accept':
                file.close()
                break

        # except:
        #     print("\nSintatic error at line " + str(a[3]) + " at column " + str(a[4]), "\n")
        #     # a = panic(a,lx)
        #     # if a is 'end':
        #     #     break
        #     # else:
        #     #     continue
        #     break


if __name__ == "__main__":
    main()

