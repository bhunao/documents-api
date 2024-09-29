from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def base_endpoint():
    return {"working?": "yes"}
