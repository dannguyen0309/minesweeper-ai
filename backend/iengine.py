import sys
from algorithms import * 

if __name__ == "__main__":
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    
    kb, query = parsing_file(filename)

    if method == "TT":
        TT_entails(kb, query)
    elif method == "FC":
        FC_entails(kb, query)
    elif method == "BC":
        BC_entails(kb, query)
    else:
        print("Unkown method. Choose TT, BC or TC.")
