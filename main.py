from fastapi import FastAPI
from database import engine, Base
from routes import tasks
from routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth & Tasks API",
    description="API con autenticación JWT, usuarios y tareas",
    version="1.0.0",
    contact={
        "name": "Oscar Ortega",
        "email": "oscaror98@gmail.com"
    }
)

app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "API funcionando 🚀"}