from fastapi import FastAPI




app = FastAPI()

@app.get("/")
def hello_index():
    return {
        "message": "Hello index!"
    }

@app.get("/items")
def list_items():
    return [
        "items1",
        "items2",
    ]

@app.get("/items2")
def list_items2():
    return [
        "items1",
        "items2",
    ]
