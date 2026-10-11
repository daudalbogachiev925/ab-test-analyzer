from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import experiments, analysis, mde

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AB Test Analyzer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(experiments.router, prefix="/api/experiments", tags=["experiments"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(mde.router, prefix="/api/mde", tags=["mde"])

@app.get("/health")
def health():
    return {"status": "ok"}
