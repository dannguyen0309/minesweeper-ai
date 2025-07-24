from algorithms import FC_entails

def get_adjacent_cells(cell_id:str) -> list[str]:
    row_labels = "ABCDEFGHI"
    col_labels = range(1,10+1)

    row = cell_id[0]
    col = int(cell_id[1:])

    row_idx = row_labels.index(row)

    directions =[(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]

    neighbors = []

    for dr, dc in directions:
        r_idx = row_idx + dr
        c_idx = col + dc 
        if 0 <= r_idx < 9 and 1 <= c_idx <= 9:
            neighbor = f"{row_labels[r_idx]}{c_idx}"
            neighbors.append(neighbor)
    
    return neighbors

def extract_kb_from_game_state(game_state: dict) -> list[str]:
    kb = set()
    opened = game_state["opened"]
    unopened = game_state["unopened"]
    flagged = game_state.get("flagged", [])

    unopened = [c for c in unopened if c not in flagged]

    for cell, value in opened.items():
        adj = get_adjacent_cells(cell)
        adj_unopened = [c for c in adj if c in unopened]

        if not adj_unopened:
            continue

        if value == 0:
            for c in adj_unopened:
                kb.add(f"safe_{c}")
        
        elif value == len(adj_unopened):
            for c in adj_unopened:
                kb.add(f"mine_{c}")
        else:
            premises = " & ".join([f"mine_{c}" for c in adj_unopened])
            kb.add(f"{premises} => clue_{cell}_{value}")
    
            kb.add(f"clue_{cell}_{value}")

    return list(kb)


# if __name__ == "__main__":
#     import json
#     with open("states/game_state.json") as f:
#         game_state = json.load(f)

#     kb = extract_kb_from_game_state(game_state)
    
#     # Test vài ô
#     test_cells = ["F5", "F9", "G2", "G1", "E1", "E2", "E3", "E4"]

#     for cell in test_cells:
#         print(f"\n>>> Testing {cell}")
#         FC_entails(kb, f"safe_{cell}")
#         FC_entails(kb, f"mine_{cell}")