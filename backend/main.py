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

    # Forward Chaining
    for cell in unopened:
        if FC_entails(kb, f'safe_{cell}'):
            return {"action": "open", "cell": cell}
        if FC_entails(kb, f'mine_{cell}'):
            return {"action": "flag", "cell": cell}
    
    # Calculate Risk
    risk = calculate_risk_heuristic(game_state.dict())
    if risk:
        safest = min(risk.items(), key=lambda x: x[1])[0]
        return {"action": "open", "cell": safest}
    
    # Random if there is no choice
    return {"action": "open", "cell": random.choice(unopened)}