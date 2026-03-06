from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from tms.tms import TMS

api = FastAPI(description='tms api', title='TMS')
tms = TMS()

# tms

@api.get("/api/tms")
async def get_tms():
    return tms.to_dict()

# tester

class TesterRequest(BaseModel):
    name: str
    level: int

@api.get("/api/tester")
async def get_tester(name: str):
    try:
        return tms.get_tester(name).to_dict()
    except Exception:
        raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

@api.post("/api/tester", status_code=status.HTTP_201_CREATED)
async def add_tester(tester: TesterRequest):
    try:
        tms.add_tester(tester.name, tester.level)
        return None
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

@api.delete("/api/tester", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tester(name: str):
    try:
        tms.remove_tester(name)
        return None
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

@api.put("/api/tester", status_code=status.HTTP_204_NO_CONTENT)
async def update_tester(name: str, request: TesterRequest):
    try:
        tms.rename_tester(name, request.name)
        tms.promote_tester(name, request.level) # ;D
        return None
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

@api.patch("/api/tester", status_code=status.HTTP_204_NO_CONTENT)
async def change_tester(name: str, request: dict):
    try:
        if 'new_name' in request:
            tms.rename_tester(name, request['new_name'])
        if 'new_level' in request:
            tms.promote_tester(name, request['new_level'])
        return None
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

# tester

class ScenarioRequest(BaseModel):
    name: str

@api.post('/api/scenario/', status_code=status.HTTP_201_CREATED)
async def create_scenario(tester: str, request: ScenarioRequest):
    try:
        tms.get_tester(tester).create_scenario(request.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

@api.delete('/api/scenario/', status_code=status.HTTP_201_CREATED)
async def delete_scenario(tester: str, request: ScenarioRequest):
    try:
        tms.get_tester(tester).remove_scenario(request.name)
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)