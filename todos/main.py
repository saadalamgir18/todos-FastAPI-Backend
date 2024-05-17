from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Todo(BaseModel):
    id: int
    task: str
print("app is running")
todosData = [
    {
        "id": 1,
        "task": "go to gym"
    },
    {
        "id": 2,
        "task": "go to gym"
    },
    {
        "id": 3,
        "task": "go to gym"
    }
]
@app.get("/getalltodos")
def gettodo():
    global todosData
    return todosData

@app.post("/addtodo")
def addtodo(todo:Todo):
    global todosData
    todosData.append(todo)
    return todosData

@app.get("/gettodobyid/{id}")
def gettodobyid(id:int):
    global todosData
    print(todosData)
    for td in todosData:
        print(td)
        if td["id"] == id:

            return td
        
@app.put("/updatetodobyid")
def updatetodobyid(todo:Todo):
    global todosData
    print("in update")
    for td in todosData:
        if td["id"] == todo.id:
            td["task"] = todo.task
            return {"message": "todo updated successfully",
                    "task":td["task"]} 




def start():
    uvicorn.run("todos.main:app",port=5000, reload = True)


