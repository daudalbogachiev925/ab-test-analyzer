from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Experiment, Observation
from app.schemas import (ExperimentCreate, ExperimentRead,
                         ObservationCreate, ObservationRead)

router = APIRouter()

@router.post("", response_model=ExperimentRead, status_code=201)
def create(payload: ExperimentCreate, db: Session = Depends(get_db)):
    if db.query(Experiment).filter(Experiment.name == payload.name).first():
        raise HTTPException(409, "Name exists")
    e = Experiment(**payload.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

@router.get("", response_model=List[ExperimentRead])
def list_all(db: Session = Depends(get_db)):
    return db.query(Experiment).all()

@router.get("/{exp_id}", response_model=ExperimentRead)
def get_one(exp_id: int, db: Session = Depends(get_db)):
    e = db.query(Experiment).get(exp_id)
    if not e:
        raise HTTPException(404)
    return e

@router.post("/{exp_id}/observations", response_model=ObservationRead, status_code=201)
def add_observation(exp_id: int, payload: ObservationCreate,
                     db: Session = Depends(get_db)):
    if not db.query(Experiment).get(exp_id):
        raise HTTPException(404, "Experiment not found")
    o = Observation(experiment_id=exp_id, **payload.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    return o

@router.get("/{exp_id}/observations", response_model=List[ObservationRead])
def list_observations(exp_id: int, db: Session = Depends(get_db)):
    return db.query(Observation).filter(Observation.experiment_id == exp_id).all()
