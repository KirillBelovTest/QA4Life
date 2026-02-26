from fastapi import FastAPI, status
from pydantic import BaseModel
from tms.tms import TMS

api = FastAPI()
tms = TMS()

@api.get("/")
async def get_tms():
    return tms.to_dict()

@api.get("/tester")
async def get_tester(name: str = None):
    return tms.get_tester(name).to_dict()

class TesterRequest(BaseModel):
    name: str
    level: int

@api.post("/tester", status_code=status.HTTP_201_CREATED)
async def add_tester(tester: TesterRequest):
    tms.add_tester(tester.name, tester.level)
    return None