"""Entry point for API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import income, expenses, summary, export


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://localhost:5173",
        "http://localhost:9080",
        "https://localhost:9080",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(summary.router)
app.include_router(export.router)


@app.get("/")
async def root():
    """Just to have something at the root."""
    return {"message": "Budget Tracker API"}
