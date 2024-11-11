from fastapi import Depends, FastAPI, HTTPException, Request
from inspector.inspector_controllers import router as inspector_router
from report.report_controllers import router as report_router
from JWT_user.user_controller import router as user_router
from database import init_db
from typing import Annotated
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from JWT_user.auth import verify_access_token

app = FastAPI()

# Определение схемы авторизации через HTTPBearer
oauth2_scheme = HTTPBearer()

# Пример конечной точки с требованием токена
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# Промежуточное ПО для проверки токена в каждом запросе
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    try:
        # Получаем токен из заголовка Authorization
        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")  # Убираем префикс "Bearer" для корректной проверки
            verify_access_token(token)  # Проверяем токен с помощью функции verify_access_token
        response = await call_next(request)
        return response
    except HTTPException as exc:
        return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
    except Exception as exc:
        return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

# Инициализация базы данных
init_db()

# Подключение маршрутов
app.include_router(inspector_router, prefix="/inspectors", tags=["Inspectors"])
app.include_router(report_router, prefix="/reports", tags=["Reports"])
app.include_router(user_router, prefix="/users", tags=["Users"])