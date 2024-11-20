from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Initialize FastAPI app
app = FastAPI()

# Model for a player
class Player(BaseModel):
    id: int
    username: str
    email: str

# Model for a game score
class GameScore(BaseModel):
    player_id: int
    score: int

# Simulating databases
players_db = []
scores_db = []

# Route to register a player
@app.post("/api/register-player")
def register_player(player: Player):
    # Check if the player already exists
    if any(p.id == player.id for p in players_db):
        raise HTTPException(status_code=400, detail="Player already exists")
    
    # Simulate saving the player (in reality, save to a database)
    players_db.append(player)
    return {"message": f"Player {player.username} registered successfully!"}

# Route to get all players
@app.get("/api/players", response_model=List[Player])
def get_players():
    if not players_db:
        raise HTTPException(status_code=404, detail="No players found")
    return players_db

# Route to submit a game score
@app.post("/api/submit-score")
def submit_score(game_score: GameScore):
    # Check if the player exists
    player = next((p for p in players_db if p.id == game_score.player_id), None)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Simulate saving the game score
    scores_db.append(game_score)
    return {"message": f"Score of {game_score.score} for player {player.username} submitted successfully!"}

# Route to get the leaderboard (top scores)
@app.get("/api/leaderboard", response_model=List[dict])
def get_leaderboard():
    if not scores_db:
        raise HTTPException(status_code=404, detail="No scores found")
    
    # Tally the scores by player
    player_scores = {}
    for score in scores_db:
        if score.player_id in player_scores:
            player_scores[score.player_id] += score.score
        else:
            player_scores[score.player_id] = score.score
    
    # Sort players by total score in descending order
    sorted_leaderboard = sorted(
        [{"player_id": player_id, "score": score} for player_id, score in player_scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )
    
    # Return leaderboard with player details
    leaderboard = []
    for entry in sorted_leaderboard:
        player = next((p for p in players_db if p.id == entry["player_id"]), None)
        if player:
            leaderboard.append({
                "username": player.username,
                "score": entry["score"]
            })
    
    return leaderboard

# Root route with a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Game Leaderboard Microservice!"}

# Run the app using uvicorn (this can be done directly or using the command line)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
