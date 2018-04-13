from Lexical import Lexical
#from Backup import Backup

def main():
    #lx = Backup()
    lx = Lexical()
    lx.get_file('simple_source.txt')
    lx.analyze()
    #token = lx.next_token()
    #print("Next token: " +str(token))

if __name__ == "__main__":
    main()
