from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.ESM2ForPTMs.main import ESM2ForPTMs

router = APIRouter()

class ProteinSequenceRequest(BaseModel):
    protein_sequence: str

@router.post("/esm2ptm/predict")
async def predict_protein_sequence(request: ProteinSequenceRequest):
    try:
        result = ESM2ForPTMs(request.protein_sequence)
        return {"predictions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
