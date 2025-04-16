from fastapi import FastAPI


app = FastAPI()


# Import routes
from api.routes import income, expenses, summary, export


# Include routers
app.include_router(income.router)
app.include_router(expenses.router)
app.include_router(summary.router)
app.include_router(export.router)


# Basic API functionality
@app.get("/")
async def root():
    return {"message": "Budget Tracker API"}
