from pydantic import BaseModel, Field

# Para crear tarea
class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Título de la tarea"
    )

# Para devolver tarea
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True