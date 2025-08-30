from sqlalchemy.orm import Session
from learning import models, schemas,  database
from fastapi import Depends
from typing import List
   #give access to instructor
def Modules_create(Modules:schemas.ModulesCreate,db:Session = Depends(database.get_db)):
    new_module = models.Modules( C_id = Modules.C_id, Module_name = Modules.Module_name )
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    db.add(new_module)    
    db.commit()   
    return new_module
def Modules_read(M_id:int,db: Session = Depends(database.get_db)):
    get_module = db.query(models.Modules).filter(models.Modules.M_id == M_id).first()
    return get_module

