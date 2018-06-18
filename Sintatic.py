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


# -----------------------------  Tradução dirigida  ------------------------------------
def semantic(prod,file,ss,a,produtions):
    if prod is 5:
        file.write("\n\n\n")
    # elif prod is 6:
        # TODO id.tipo <- TIPO.tipo
        # file.write(ss[-1][2],";\n")
    # elif prod is 7:
    # elif prod is 8:
    # elif prod is 9:
    elif prod is 11:
        if a[0] is "lit":
            file.write("scanf(“%s”,",a[2],");\n")
        elif a[0] is "int":
            file.write("scanf(“%d”,", a[2], ");\n")
        elif a[0] is "real":
            file.write("scanf(“%lf”,", a[2], ");\n")
        else:
            print("\nErro: Variável não declarada\n")
    # elif prod is 12:
    #     file.write("print(",ss[-1][2],");\n")
    # elif prod is 13:
    # elif prod is 14:
    # elif prod is 15:
    # elif prod is 17:
    # elif prod is 18:
    # elif prod is 19:
    # elif prod is 20:
    # elif prod is 21:
    elif prod is 23:
        file.write("}\n")
    # elif prod is 24:
    #     file.write("if(",ss[-1][2],"){\n")
    # elif prod is 25:


# ------------------------------  Show the error message  --------------------------------------
def error(a,s):
    erros = pd.read_csv('error.csv', index_col=0)
    print("\nErro sintático na linha "+str(a[3])+" na coluna "+str(a[4]),"\n")
    if not pd.isnull(erros.loc[s,'Erro']):
        print(erros.loc[s,'Erro'],"\n")
    else:
        print("Estrutura sintática inválida.\n")


# ------------------------   Determina quantos estados desempilhar  ----------------------------
def pop(produtions,prod,pilha):
    for i in range(len(produtions.loc[prod, 'produtions'].split())):
        pilha.pop()  # Desempilha o tamanho da produção


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
    file = open("PROGRAMA.c","w")

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
                print(produtions.loc[int(prod),'non_terminal']+" -> "+produtions.loc[int(prod),'produtions'])  # Imprima a producao

                ''' ---- Semantic ----- '''
                semantic(prod,file,ss,a,produtions)

            # -------------------------- Accept -------------------------------
            elif ACTION.loc[s, a[0]] == 'accept':
                print("Código aceito!")
                file.close()
                break

        except:
            error(a,s)
            a = panic(a,lx)
            if a is 'end':
                break
            else:
                continue


if __name__ == "__main__":
    main()

