from sqlalchemy.orm import Session
from passlib.context import CryptContext
from learning import models, schemas
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
def create_user(user: schemas.UserCreate, db: Session):
    hashed_password = pwd_cxt.hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
def get_user(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.U_id == user_id).first()
def list_users(db: Session):
    return db.query(models.User).all()