from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from extractor import extract_kb_from_game_state
from algorithms import FC_entails
from risk_heuristic import calculate_risk_heuristic

import random

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GameState(BaseModel):
    opened: Dict[str, int]
    unopened: List[str]
    flagged: List[str] = []
    total_mines: int

from typing import Optional

class MoveResponse(BaseModel):
    action: str
    cell: Optional[str] = None

@app.post('/play-move', response_model=MoveResponse)
def play_move(game_state: GameState):
    import time
    kb_input = {
        'opened': game_state.opened,
        'unopened': game_state.unopened,
        'flagged': game_state.flagged
    }
    kb = extract_kb_from_game_state(kb_input)
    unopened = list(set(game_state.unopened) - set(game_state.flagged))

        # If no cells are opened, pick a random cell for the first move
    if not game_state.opened:
        first_cell = random.choice(unopened)
        print({"action": "open", "cell": first_cell, "info": "first move"})
        time.sleep(1)
        return {"action": "open", "cell": first_cell}
    
    # Forward Chaining: open safe cells first
    for cell in unopened:
        if FC_entails(kb, f'safe_{cell}'):
            time.sleep(1)
            return {"action": "open", "cell": cell}
        

    # Conservative flagging: only flag if risk is extremely high and no safe moves
    risk_input = {
        'opened': game_state.opened,
        'unopened': game_state.unopened,
        'flagged': game_state.flagged
    }
    risk = calculate_risk_heuristic(risk_input)
    # Only flag if we haven't already flagged as many as total_mines
    if len(game_state.flagged) < game_state.total_mines:
        for cell in unopened:
            if FC_entails(kb, f'mine_{cell}') and risk.get(cell, 0) > 0.99:
                time.sleep(1)
                return {"action": "flag", "cell": cell}
    
    # Only open the cell with the lowest risk if it's below a threshold, otherwise stop
    RISK_GUESS_THRESHOLD = 1.0
    if risk:
        min_risk = min(risk.values())
        if min_risk > RISK_GUESS_THRESHOLD:
            print(f"All remaining moves are risky (min risk: {min_risk}). Stopping AI.")
            return {"action": "no_move", "cell": None}
        lowest_cells = [cell for cell, val in risk.items() if val == min_risk]
        chosen = lowest_cells[0]  # deterministic: first in dict order
        print({"action": "open", "cell": chosen, "risk": min_risk, "candidates": lowest_cells})
        time.sleep(1)
        return {"action": "open", "cell": chosen}
    # If no risk info, stop
    print("No risk info available")
    return {"action": "no_move", "cell": None}