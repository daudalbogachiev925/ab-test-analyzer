from fastapi import APIRouter
from app.schemas import MdeRequest, MdeResult
from app.core.mde import sample_size, days_needed

router = APIRouter()

@router.post("", response_model=MdeResult)
def calc(req: MdeRequest):
    n = sample_size(req.baseline_rate, req.mde_relative,
                    req.alpha, req.power)
    days = days_needed(n, req.daily_users)
    return MdeResult(users_per_variant=n, total_users=n*2,
                     days_needed=round(days, 1))
