from fastapi import APIRouter


router = APIRouter()


@router.get("/export/csv/")
async def export_csv():
    return {"message": "Export to CSV"}
