from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Experiment, Observation
from app.schemas import FreqResult, BayesResult
from app.core.frequentist import two_proportion_test
from app.core.bayesian import bayesian_ab
from app.core.sequential import sequential_test
from app.core.sanity import sanity_check

router = APIRouter()

def _aggregate(db, exp_id):
    obs = db.query(Observation).filter(Observation.experiment_id == exp_id).all()
    cu = sum(o.users for o in obs if o.variant == "control")
    cc = sum(o.conversions for o in obs if o.variant == "control")
    tu = sum(o.users for o in obs if o.variant == "treatment")
    tc = sum(o.conversions for o in obs if o.variant == "treatment")
    return cu, cc, tu, tc

@router.get("/{exp_id}/frequentist", response_model=FreqResult)
def freq(exp_id: int, db: Session = Depends(get_db)):
    e = db.query(Experiment).get(exp_id)
    if not e:
        raise HTTPException(404)
    cu, cc, tu, tc = _aggregate(db, exp_id)
    return two_proportion_test(cu, cc, tu, tc)

@router.get("/{exp_id}/bayesian", response_model=BayesResult)
def bayes(exp_id: int, db: Session = Depends(get_db)):
    if not db.query(Experiment).get(exp_id):
        raise HTTPException(404)
    cu, cc, tu, tc = _aggregate(db, exp_id)
    return bayesian_ab(cc, cu, tc, tu)

@router.get("/{exp_id}/sequential")
def seq(exp_id: int, look: int = 1, db: Session = Depends(get_db)):
    if not db.query(Experiment).get(exp_id):
        raise HTTPException(404)
    cu, cc, tu, tc = _aggregate(db, exp_id)
    if cu == 0 or tu == 0:
        raise HTTPException(400, "No data")
    return sequential_test(cc/cu, tc/tu, max(cu, tu), current_look=look)

@router.get("/{exp_id}/sanity")
def sanity(exp_id: int, db: Session = Depends(get_db)):
    if not db.query(Experiment).get(exp_id):
        raise HTTPException(404)
    cu, cc, tu, tc = _aggregate(db, exp_id)
    return sanity_check(cu, cc, tu, tc)
