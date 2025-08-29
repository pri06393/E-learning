from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, database
# Security settings
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
bearer_scheme = HTTPBearer()

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(database.get_db)):
    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user22121" ,
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception1 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not JWT" ,
       
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception2 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not user error" ,
     
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        sub: str = payload.get("sub")

        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception1
    user = db.query(models.User).filter(models.User.name == sub).first()
    if user is None:
        raise credentials_exception2
    return user

def role_required(required_role: str):
    def role_dependency(current_user: models.User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Requires {required_role} role",
            )
        return current_user
    return role_dependency

def verify_password(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_cxt.hash(password)






