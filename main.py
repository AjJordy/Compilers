from Lexical import Lexical

def main():
    lx = Lexical()
    lx.get_file('simple_source.txt')
    #lx.get_file('source.txt')
    lx.analyze()
    #token = lx.next_token()
    #print("Next token: " +str(token))

if __name__ == "__main__":
    main()
