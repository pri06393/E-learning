from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from learning import schemas, database
from learning.repository import Modules as module_repo
from typing import List
router = APIRouter(prefix="/courses", tags=["modules"])
@router.post("/module_create", response_model=schemas.ModulesRead)
def create_model(modules: schemas.ModulesCreate, db: Session = Depends(database.get_db)):
    return module_repo.Modules_create(modules, db)

@router.get("/{M_id}", response_model=schemas.ModulesQuizRead)
def get_model(M_id: int, db: Session = Depends(database.get_db)):
    return module_repo.Modules_read(M_id, db)