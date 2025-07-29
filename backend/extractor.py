from algorithms import FC_entails

def get_adjacent_cells(cell_id:str) -> list[str]:
    # Dynamically support up to 26 rows and 99 columns
    # Infer max row/col from cell_id and typical board sizes
    row_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Try to infer max_col from cell_id, fallback to 30
    try:
        col = int(cell_id[1:])
    except Exception:
        col = 1
    max_col = max(9, col, 16, 30)  # fallback to 30 if uncertain
    # For medium/expert, frontend should only send valid cell_ids
    # You may want to pass board size explicitly for full generality
    row = cell_id[0]
    row_idx = row_labels.index(row)
    directions =[(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]
    neighbors = []
    # Use up to 26 rows, but only valid ones for the board
    for dr, dc in directions:
        r_idx = row_idx + dr
        c_idx = col + dc
        if 0 <= r_idx < len(row_labels) and 1 <= c_idx <= max_col:
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