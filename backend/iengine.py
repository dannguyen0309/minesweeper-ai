import sys
from algorithms import * 

if __name__ == "__main__":
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    
    kb, query = parsing_file(filename)

    if method == "TT":
        TT_entails(kb, query)
    elif method == "FC":
        try:
            FC_entails(kb, query)
        except NonHornClauseError as e:
            print(f"[INFO] {e} Switching to Truth Table method.")
            TT_entails(kb, query)
    elif method == "BC":
        try:
            result = BC_entails(kb, query)
        except NonHornClauseError as e:
            print(f"[INFO] {e} Switching to Truth Table method.")
            TT_entails(kb, query)
    else:
        print("Unknown method. Choose TT, BC or FC.")
