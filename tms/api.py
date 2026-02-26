from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from tms.tms import TMS

api = FastAPI()
tms = TMS()

@api.get("/")
async def get_tms():
    return tms.to_dict()

@api.get("/tester")
async def get_tester(name: str):
    try:
        return tms.get_tester(name).to_dict()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


class TesterRequest(BaseModel):
    name: str
    level: int

@api.post("/tester", status_code=status.HTTP_201_CREATED)
async def add_tester(tester: TesterRequest):
    try:
        tms.add_tester(tester.name, tester.level)
        return None
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)