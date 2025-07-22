from extractor import get_adjacent_cells

def calculate_risk_heuristic(game_state: dict) -> dict[str, float]:
    risk_score = {}
    opened = game_state["opened"]
    unopened = game_state["unopened"]

    for cell, value in opened.items():
        if value == 0:
            continue
            
        neighbors = get_adjacent_cells(cell) #checking cell surround opened cell
        adj_unopened = [n for n in neighbors if n in unopened] # return array of cells that in unopened
        k =  len(adj_unopened)

        if k == 0:
            continue

        # Calculate risk
        risk = value / k

        for n in adj_unopened:
            if n not in risk_score:
                risk_score[n] = []
            risk_score[n].append(risk)
        
    #Calculate the mean 
    final_score = {cell: sum(vals)/len(vals) for cell, vals in risk_score.items()}

    return final_score




    