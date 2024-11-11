import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

# Получение секретного ключа и алгоритма из переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))

# OAuth2 схема для получения токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для создания JWT-токенов
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для извлечения токена из заголовка запроса
def get_token_from_request(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not provided")

# Функция для проверки токена для использования в middleware
def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"user_id": user_id}

# Функция для получения текущего пользователя через Depends (например, для маршрутов)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)
