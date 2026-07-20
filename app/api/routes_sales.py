from fastapi import APIRouter

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/test")
def test_sales_route():
    return {
        "message": "Sales routes are connected",
        "next_step": "CSV upload endpoint"
    }