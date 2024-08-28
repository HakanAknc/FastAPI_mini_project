from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Takım veri modeli
class Team(BaseModel):
    id: int
    name: str
    city: str
    established_year: int
    stadium: str

teams = []

# Takımları listeleme
@app.get("/teams")
def get_teams():
    return teams

# Yeni takım ekleme
@app.post("/teams")
def create_team(team: Team):
    for existing_team in teams:
        if existing_team.id == team.id:
            raise HTTPException(status_code=400, detail="Team with this ID already exists")
    teams.append(team)
    return team

# Takım güncelleme
@app.put("/teams/{team_id}")
def update_team(team_id: int, team: Team):
    for index, existing_team in enumerate(teams):
        if existing_team.id == team_id:
            teams[index] = team
            return team
    raise HTTPException(status_code=404, detail="Team not found")

# Takım silme
@app.delete("/teams/{team_id}")
def delete_team(team_id: int):
    for index, existing_team in enumerate(teams):
        if existing_team.id == team_id:
            del teams[index]
            return {"detail": "Team deleted"}
    raise HTTPException(status_code=404, detail="Team not found")
