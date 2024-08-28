from sqlalchemy.orm import Session
from . import models, schemas

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, city=team.city, founded=team.founded)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def create_player(db: Session, player: schemas.PlayerCreate, team_id: int):
    db_player = models.Player(**player.dict(), team_id=team_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player
