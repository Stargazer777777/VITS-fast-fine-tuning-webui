from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import role, media, train
from pydantic import BaseModel
from typing import Union, Any
from server.my_utils import get_abs_path

app = FastAPI()

app.include_router(role.router)
app.include_router(media.router)
app.include_router(train.router)

app.mount("/data", StaticFiles(directory=get_abs_path("data")), name="data")


# uvicorn server.main:app --reload --host 192.168.1.3 --port 7777
@app.get("/")
def helloWorld():
    return "Hello world"
