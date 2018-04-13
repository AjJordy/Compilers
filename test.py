from Lexical import Lexical
import queue

def main():
    lx = Lexical()
    lx.get_file('source.txt')
    lx.analyze()
    token = lx.next_token()
    print("Next token:")
    print(token)

if __name__ == "__main__":
    main()
