from fastapi import APIRouter


router = APIRouter()


@router.get("/summary/")
async def get_summary():
    return {"message": "Get summary"}
