from pprint import pprint
from new import Lexical

def main():
    lx = Lexical()
    lx.get_file('simple_source.txt')
    while(True):
        temp = lx.next_token()
        print(temp)
        if(temp[0] in ["EOF","erro"] ):
            break

    pprint(lx.symbols_table)


if __name__ == "__main__":
    main()
