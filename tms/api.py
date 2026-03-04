from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from tms.tms import TMS

api = FastAPI(description='tms api', title='TMS')
tms = TMS()

@api.get("/api/tms")
async def get_tms():
    return tms.to_dict()

@api.get("/api/tester")
async def get_tester(name: str):
    try:
        return tms.get_tester(name).to_dict()
    except Exception:
        raise HTTPException(status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)


class TesterRequest(BaseModel):
    name: str
    level: int

@api.post("/api/tester", status_code=status.HTTP_201_CREATED)
async def add_tester(tester: TesterRequest):
    try:
        tms.add_tester(tester.name, tester.level)
        return None
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

class ScenarioRequest(BaseModel):
    name: str

@api.post("/api/tester/{name}/scenario", status_code=status.HTTP_201_CREATED)
async def create_scenario(name: str, request: ScenarioRequest):
    """Тестировщик создаёт новый сценарий."""
    try:
        tester = tms.get_tester(name)
        tester.create_scenario(request.name)
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api.delete("/api/tester/{name}/scenario/{scenario_name}")
async def remove_scenario(name: str, scenario_name: str):
    """Тестировщик удаляет сценарий."""
    try:
        tester = tms.get_tester(name)
        tester.remove_scenario(scenario_name)
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api.post("/api/tester/{name}/scenario/{scenario_name}/take")
async def take_scenario(name: str, scenario_name: str):
    """Тестировщик берёт сценарий в работу."""
    try:
        tester = tms.get_tester(name)
        tester.take_scenario(scenario_name)
        return tester.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class StepRequest(BaseModel):
    name: str
    expected: str

@api.post("/api/tester/{name}/step", status_code=status.HTTP_201_CREATED)
async def add_step(name: str, request: StepRequest):
    """Тестировщик добавляет шаг в текущий сценарий."""
    try:
        tester = tms.get_tester(name)
        tester.add_step(request.name, request.expected)
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api.post("/api/tester/{name}/step/next")
async def take_next_step(name: str):
    """Тестировщик переходит к следующему шагу."""
    try:
        tester = tms.get_tester(name)
        tester.take_next_step()
        return tester.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class ExecuteStepRequest(BaseModel):
    actual_result: str

@api.post("/api/tester/{name}/step/execute")
async def execute_step(name: str, request: ExecuteStepRequest):
    """Тестировщик выполняет текущий шаг."""
    try:
        tester = tms.get_tester(name)
        result = tester.execute_step(request.actual_result)
        return {"passed": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

class BugRequest(BaseModel):
    steps_to_reproduce: list = None

@api.post("/api/tester/{name}/bug", status_code=status.HTTP_201_CREATED)
async def create_bug(name: str, request: BugRequest = None):
    """Тестировщик создаёт ошибку на текущем шаге."""
    try:
        tester = tms.get_tester(name)
        steps = request.steps_to_reproduce if request else None
        bug = tester.create_bug(steps)
        return bug.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class BugStatusRequest(BaseModel):
    status: str

@api.patch("/api/tester/{name}/bug/{bug_index}")
async def change_bug_status(name: str, bug_index: int, request: BugStatusRequest):
    """Тестировщик меняет статус ошибки."""
    try:
        tester = tms.get_tester(name)
        tester.change_bug_status(bug_index, request.status)
        return tester.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
