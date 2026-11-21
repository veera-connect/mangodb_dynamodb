
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["college"]
students = db["students"]

# CREATE
@app.post("/students")
def create(name: str, age: int):
    students.insert_one({"name": name, "age": age})
    return {"message": "Student created"}

# READ
@app.get("/students")
def read():
    return list(students.find({}, {"_id": 0}))

# UPDATE
@app.put("/students/{name}")
def update(name: str, age: int):
    students.update_one(
        {"name": name},
        {"$set": {"age": age}}
    )
    return {"message": "Student updated"}

# DELETE
@app.delete("/students/{name}")
def delete(name: str):
    students.delete_one({"name": name})
    return {"message": "Student deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)