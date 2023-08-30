from fastapi import APIRouter, Query, HTTPException, status
import os
import shutil
from server.my_utils import get_abs_path
from pydantic import BaseModel

router = APIRouter(tags=["train"], prefix="/train")

class TrainOptions(BaseModel):
    pre_model:str = "C"
    

@router.post("/start")
def start_train():
    return
