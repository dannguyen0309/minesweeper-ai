import sys
from algorithms import *

if __name__ == "__main__":
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    
    kb, query = parsing_file(filename)

    try:
        if method == "TT":
            TT_entails(kb, query)
        elif method == "FC":
            try:
                FC_entails(kb, query)
            except Exception as e:
                print(f"[ERROR] {e}")
                print("[INFO] Attempting Truth Table method as fallback...")
                try:
                    TT_entails(kb, query)
                except Exception as e2:
                    print(f"[ERROR] {e2}")
                    print("[FAIL] Invalid KB: not a valid Horn clause or generic KB.")
        elif method == "BC":
            BC_entails(kb, query)
        else:
            print("Unknown method. Choose TT, BC or FC.")
    except Exception as e:
        print(f"[FAIL] Invalid KB: not a valid Horn clause or generic KB.\nDetails: {e}")