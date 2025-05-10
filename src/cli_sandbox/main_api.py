from fastapi import FastAPI, Query
from typing import List
from datetime import datetime

app = FastAPI()

@app.get("/greet")
def greet(
    name: str = Query(..., description="あなたの名前"),
    repeat: int = Query(1, ge=1, le=10),
    upper: bool = Query(False)
):
    if upper:
        greeting = greeting.upper()
    
    messages = [f"こんにちは, {name}さん！" for _ in range(repeat)]
    return {"messages": messages}

@app.get("/version")
def version():
    return {"version": "0.1.0"}