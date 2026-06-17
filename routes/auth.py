from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionLocal
from models import User
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()

# =========================
# DB DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# SCHEMAS
# =========================
class RegisterRequest(BaseModel):
    username: str
    password: str


# =========================
# REGISTER
# =========================
@router.post("/register", tags=["Auth"])
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    username = data.username
    password = data.password

    user_exists = db.query(User).filter(User.username == username).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario creado correctamente"}


# =========================
# LOGIN (OAUTH2 STANDARD)
# =========================
@router.post(
    "/login",
    tags=["Auth"],
    summary="Login de usuario",
    description="Autentica usuario y devuelve token JWT",
    response_description="JWT access token"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# PROFILE (PROTECTED ROUTE)
# =========================
@router.get("/profile", tags=["User"])
def profile(user: str = Depends(get_current_user)):
    return {
        "user": user,
        "message": "Perfil autenticado"
    }


# =========================
# TASKS (PROTECTED ROUTE)
# =========================
@router.get("/tasks", tags=["Tasks"])
def get_tasks(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    # IMPORTANTE: asegúrate de tener modelo Task
    # from models import Task

    tasks = db.query(Task).filter(Task.user_id == user).all()

    return {
        "user": user,
        "tasks": tasks
    }