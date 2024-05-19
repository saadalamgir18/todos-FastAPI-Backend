from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from sqlmodel import Field, SQLModel, create_engine, select, Session
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

class TODOTABLE(SQLModel, table=True):
    id: int = Field(default = None, primary_key = True)
    task: str

connection_str = os.getenv("DB_URL")
connection = create_engine(str(connection_str))
SQLModel.metadata.create_all(connection)
class Todo(BaseModel):
    id: int
    task: str
print("app is running")

@app.get("/getalltodos")
def gettodo():
    with Session(connection) as session:
        statment = select(TODOTABLE)
        results = session.exec(statment)
        data = results.all()
        return data if data else {}

@app.post("/addtodo")
def addtodo(todo:Todo):
    with Session(connection) as session:
        statment = session.add(TODOTABLE(id = todo.id, task = todo.task))
        session.commit()
    return {
        "message": "task added succefully",
        "todo": todo
    }

@app.get("/gettodobyid/{id}")
def gettodobyid(id:int):
    with Session(connection) as session:
        statment = select(TODOTABLE).where(TODOTABLE.id == id)
        results = session.exec(statment)
        data = results.all()
        return data if data else {}

@app.put("/updatetodobyid")
def updatetodobyid(todo:Todo):
    with Session(connection) as session:
        statment = select(TODOTABLE).where(TODOTABLE.id == todo.id)
        results = session.exec(statment)
        set_todo = results.one()
        set_todo.task = todo.task
        session.add(set_todo)
        session.commit()
        session.refresh(set_todo)
    return set_todo


def start():
    uvicorn.run("todos.main:app",port=5000, reload = True)


