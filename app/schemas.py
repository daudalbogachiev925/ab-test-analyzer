from typing import Optional, List
from pydantic import BaseModel, Field

class ExperimentCreate(BaseModel):
    name: str
    hypothesis: Optional[str] = None
    metric: str = "conversion"
    baseline_rate: float = Field(0.10, ge=0, le=1)
    mde: float = Field(0.05, gt=0, le=1)

class ExperimentRead(ExperimentCreate):
    id: int
    status: str
    class Config:
        from_attributes = True

class ObservationCreate(BaseModel):
    variant: str = Field(pattern="^(control|treatment)$")
    users: int = Field(ge=1)
    conversions: int = Field(ge=0)
    revenue: float = 0.0
    day: int = 0

class ObservationRead(ObservationCreate):
    id: int
    class Config:
        from_attributes = True

class FreqResult(BaseModel):
    control_rate: float
    treatment_rate: float
    absolute_lift: float
    relative_lift: float
    p_value: float
    z_score: float
    ci_low: float
    ci_high: float
    significant: bool

class BayesResult(BaseModel):
    prob_treatment_better: float
    expected_lift: float
    credible_interval_low: float
    credible_interval_high: float

class MdeRequest(BaseModel):
    baseline_rate: float = Field(gt=0, le=1)
    mde_relative: float = Field(gt=0, le=1)
    alpha: float = 0.05
    power: float = 0.80
    daily_users: int = Field(1000, gt=0)

class MdeResult(BaseModel):
    users_per_variant: int
    total_users: int
    days_needed: float
