from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, database
# Security settings
SECRET_KEY = "yoursecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Password hashing
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.U_id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
# Role-based restriction dependency
def role_required(required_role: str):
    def role_dependency(current_user: models.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Requires {required_role} role",
            )
        return current_user
    return role_dependency
# Utility functions (optional)
def verify_password(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_cxt.hash(password)






