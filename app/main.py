from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.dummy_data import generate_dummy_data
from app.recon_logic import reconcile_branch_gl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

data_df = generate_dummy_data()

@app.get("/")
def read_root():
    return {"message": "GL Reconciliation Backend is working!"}

@app.get("/reconcile")
def reconcile(branch: str = Query(...), start: str = Query(...), end: str = Query(...)):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    balance, makeup, summary = reconcile_branch_gl(data_df.copy(), branch, start_date, end_date)
    return {
        "balance_sheet": balance.to_dict(orient="records"),
        "makeup": makeup.to_dict(orient="records"),
        "summary": summary.to_dict(orient="records")
    }
