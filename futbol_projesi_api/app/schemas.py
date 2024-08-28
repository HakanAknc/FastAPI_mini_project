from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str
    position: str
    birth_date: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    city: str
    founded: int

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    players: list[Player] = []

    class Config:
        orm_mode = True
