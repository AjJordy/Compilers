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
def semantic(prod,file,ss,lx,token,lenght):
    lista = pop(ss,lenght+1)
    if prod is 5:
        file.write("\n\n\n")
    elif prod is 6:
        lx.symbols_table[lista[-lenght-1][2]][1] = lista[-lenght][1]  # id.tipo <- TIPO.tipo
        file.write(lista[-lenght][1]," ",lx.symbols_table[lista[-lenght-1][2]][2],";\n")  # Imprimir ( TIPO.tipo id.lexema ; )
    elif prod is 7:
        token[1] = lista[-lenght][1]  # TIPO.tipo <- int.tipo
        ss.append(token)
    elif prod is 8:
        token[1] = lista[-lenght][1]  # TIPO.tipo <- real.tipo
        ss.append(token)
    elif prod is 9:
        token[1] = lista[-lenght][1]  # TIPO.tipo <- lit.tipo
        ss.append(token)
    elif prod is 11:
        if ss[-1][1] is not '':
            if ss[-1][1] is "lit":
                file.write("\tscanf(“%s”,",ss[-1][2],");\n")
            elif ss[-1][1] is "int":
                file.write("\tscanf(“%d”,", ss[-1][2], ");\n")
            elif ss[-1][1] is "real":
                file.write("\tscanf(“%lf”,", ss[-1][2], ");\n")
        else:
            print("\nErro: Variável não declarada\n")
    elif prod is 12:
        file.write("\tprintf(",ss[-1][2],");\n")
    elif prod is 13:
        token[1:] = ss.pop()[1:]      # ARG.atributos <- literal.atributos
        ss.append(token)
    elif prod is 14:
        token[1:] = ss.pop()[1:]      # ARG.atributos <- num.atributos
        ss.append(token)
    elif prod is 15:
        if ss[-1][1] is not '':
            token[1:] = ss.pop()[1:]  # ARG.atributos <- id.atributos
            ss.append(token)
        else:
            print("\nErro: Variável não declarada\n")
    elif prod is 17:
        if ss[-1][1] is not '':
            lista = pop(ss,lenght)
            if lista[2][1] is lista[1][1]:
                file.write(lista[0][1]," ",lista[1][1]," ",lista[2][1])  # id.lexema rcb.tipo LD.lexema
            else:
                print("\nErro: Tipos diferentes para atribuição\n")
        else:
            print("\nErro: Variável não declarada\n")
    # elif prod is 18:

    elif prod is 19:
        LD = ss.pop()  # LD.atributos <- OPRD.atributos
        ss.append(LD)
    elif prod is 20:
        if ss[-1][1] is not '':
            token[1:] = ss.pop()[1:]  # OPRD.atributos <- id.atributos
            ss.append(token)
        else:
            print("\nErro: Variável não declarada.\n")
    elif prod is 21:
        token[1:] = ss.pop()[1:]  # OPRD.atributos <- num.atributos
        ss.append(token)
    elif prod is 23:
        file.write("}\n")
    elif prod is 24:
        lista = pop(ss, lenght)   # CABEÇALHO <- se ( EXP_R ) entao
        file.write("if(",lista[2][2],"){\n")
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
                lenght = len(produtions.loc[prod, 'produtions'].split())
                pop(stack, lenght)

                t = int(stack[-1])  # Faça o estado t ser o topo da pilha
                stack.append(int(GOTO.loc[t,produtions.loc[prod,'non_terminal']]))  # Empilhe GOTO[t,A] na pilha
                print(produtions.loc[int(prod),'non_terminal']+" -> "+produtions.loc[int(prod),'produtions'])  # Imprime a producao

                ''' ---- Semantic ----- '''
                token = [produtions.loc[int(prod),'non_terminal'],'','']  # token não terminal
                print(token)
                semantic(prod,file,ss,lx,token,lenght)

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

