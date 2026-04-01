from fastapi import FastAPI, Form, Query, Body, File, UploadFile, Depends
from fastapi.responses import PlainTextResponse
from typing import Optional

from tms.db import TMSDatabase
from tms.tms import Tester, Bug

api = FastAPI()


db = TMSDatabase("tms.db")


def get_db():
    yield db


# POST /testers
# content-type: application/json
#
# {
#   "name": "kirill",
#   "grade": 1
# }
@api.post("/testers")
async def create_tester(
    tester: Tester,
    db: TMSDatabase = Depends(get_db)
):
    """Создает нового тестировщика и возвращает его id."""
    tester.save(db)
    return tester.id

# PUT /testers/1?grade=3
@api.put("/testers/{tester_id}")
async def update_tester_grade(
    tester_id: int,
    grade: int = Query(..., description="New grade for tester"),
    db: TMSDatabase = Depends(get_db)
):
    """Изменяет уровень тестировщика."""
    tester = Tester.get_from_table(db, tester_id)
    tester.grade = grade
    tester.save(db)
    return tester


# POST /bugs?author_id=1
# content-type: application/x-www-form-urlencoded
#
# title='authorization failed'&status=opened
@api.post("/bugs")
async def create_bug(
    title: str = Form(...),
    status: str = Form(...),
    author_id: int = Query(..., description="ID of the tester creating the bug"),
    db: TMSDatabase = Depends(get_db)
):
    """Тестировщик создает новый баг в системе.
    ID тестировщика в query.
    Информация о баге в теле в виде url form encoded."""
    tester = Tester.get_from_table(db, author_id)
    bug = Bug(**{'title': title, 'status': status, 'author_id': tester.id})
    return bug.save(db)


# PUT /bugs/1?filed=status
# content-type: text/plain
#
# closed
@api.put("/bugs/{id}", response_class=PlainTextResponse)
async def update_bug_field(
    id: int,
    field: str = Query(..., pattern="^(title|status|author_id)$"),
    new_value: str = Body(..., media_type="text/plain"),
    db: TMSDatabase = Depends(get_db)
):
    """Обновляет баг в базе.
    Сначала получает его из базы по id.
    Затем сохраняет новые поля."""
    bug = Bug.get_from_table(db, id)
    setattr(bug, field, new_value)
    bug.save(db)
    return f"Bug {id} field '{field}' updated to: {new_value}"


# GET /testers
# GET /testers?id=1
# GET /testers&grade=1
@api.get("/testers")
async def list_testers(db: TMSDatabase = Depends(get_db),
                       id: Optional[int] = None,
                       name: Optional[str] = None,
                       grade: Optional[str] = None) -> Tester | list[Tester]:
    """Получает тестеров с фильтрами.
    Если указан id - то один тестер.
    Если id не указан - то список."""
    return Tester.get_from_table(db, id, name, grade)


# GET /bugs
# GET /bugs?id=1
# GET /bugs?status=closed
@api.get("/bugs")
async def list_bugs(
    id: Optional[int] = None,
    title: Optional[str] = None,
    status: Optional[str] = None,
    author_id: Optional[int] = None,
    db: TMSDatabase = Depends(get_db)
) -> Bug | list[Bug]:
    """Получает баги с фильтрами.
    Если указан id - то один баг.
    Если id не указан - то список багов."""
    return Bug.get_from_table(db, id, title, status, author_id)