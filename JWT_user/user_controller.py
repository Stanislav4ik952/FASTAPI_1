from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from JWT_user.auth import create_access_token
from JWT_user.user_models import User
from JWT_user.user_schemas import UserCreate, UserLogin, UserResponse
from database import get_db
from JWT_user.security import hash_password, verify_password

router = APIRouter()


# Регистрация пользователя
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.login == user.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")

    hashed_password = hash_password(user.password)
    new_user = User(login=user.login, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Логин пользователя
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.login == user.login).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid login credentials")

    access_token = create_access_token(data={"sub": db_user.login,"user_id":db_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
