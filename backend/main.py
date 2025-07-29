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
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState(BaseModel):
    opened: Dict[str, int]
    unopened: List[str]
    flagged: List[str] = []

class MoveResponse(BaseModel):
    action: str
    cell: str

@app.post('/play-move', response_model=MoveResponse)
def play_move(game_state: GameState):
    kb = extract_kb_from_game_state(game_state.dict())
    unopened = list(set(game_state.unopened) - set(game_state.flagged))

        # If no cells are opened, pick a random cell for the first move
    if not game_state.opened:
        first_cell = random.choice(unopened)
        print({"action": "open", "cell": first_cell, "info": "first move"})
        return {"action": "open", "cell": first_cell}
    
    # Forward Chaining: open safe cells first
    for cell in unopened:
        if FC_entails(kb, f'safe_{cell}'):
            return {"action": "open", "cell": cell}

    # Conservative flagging: only flag if risk is extremely high and no safe moves
    risk = calculate_risk_heuristic(game_state.dict())
    for cell in unopened:
        if FC_entails(kb, f'mine_{cell}') and risk.get(cell, 0) > 0.99:
            return {"action": "flag", "cell": cell}
    
    # Calculate Risk
    RISK_THRESHOLD = 1.0
    if risk:
        safe_cells = {cell: val for cell, val in risk.items() if val <= RISK_THRESHOLD}
        if safe_cells:
            min_risk = min(safe_cells.values())
            for cell, val in safe_cells.items():
                if val == min_risk:
                    print({"action": "open", "cell": cell, "risk": min_risk})
                    return {"action": "open", "cell": cell}
    
    # If all moves are risky, stop and let user decide
    print("No safe moves, all risks above threshold")
    return {"action": "no_move", "cell": None}