from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambia SOLO la contraseña si es distinta
DATABASE_URL = "postgresql://postgres:0147@localhost:5432/api_tareas"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()