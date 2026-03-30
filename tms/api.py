from fastapi import FastAPI, Form, Query, Body, File, UploadFile, Depends
from fastapi.responses import PlainTextResponse
from typing import Optional

from pydantic import BaseModel
from tms.db import SQLiteDatabase


api = FastAPI()


db = SQLiteDatabase("tms.db")


def get_db():
    yield db

class TesterModel(BaseModel):
    id: 'Optional[int]' = None
    name: 'str'
    grade: 'int'

# POST + JSON
@api.post("/testers")
async def create_tester(
    tester: TesterModel,
    db: SQLiteDatabase = Depends(get_db)
):
    """Create a new tester - POST + JSON"""
    tester.id = db.create("testers", name=tester.name, grade=tester.grade)
    return tester

# PUT + QUERY
@api.put("/testers/{tester_id}")
async def update_tester_grade(
    tester_id: int,
    grade: str = Query(..., description="New grade for tester"),
    db: SQLiteDatabase = Depends(get_db)
):
    """Update tester grade - PUT + query parameter"""
    tester = db.read("testers", id=tester_id)
    if not tester:
        return {"error": "Tester not found"}

    db.update("testers", tester_id, grade=grade)
    return tester


@api.post("/bugs")
async def create_bug(
    tester_id: int = Query(..., description="ID of the tester creating the bug"),
    title: str = Form(...),
    description: str = Form(...),
    severity: str = Form(...),
    steps: Optional[str] = Form(None),
    db: SQLiteDatabase = Depends(get_db)
):
    """Create a bug - POST with query param (tester_id) + form data"""
    tester = db.read("testers", id=tester_id)
    if not tester:
        return {"error": "Tester not found"}

    bug_id = db.create(
        "bugs",
        title=title,
        description=description,
        steps=steps,
        status="open",
        tester_id=tester_id,
        attachments=None
    )

    return {
        "id": bug_id,
        "title": title,
        "description": description,
        "severity": severity,
        "steps": steps,
        "tester_id": tester_id
    }


@api.put("/bugs/{bug_id}", response_class=PlainTextResponse)
async def update_bug_field(
    bug_id: int,
    field: str = Query(..., pattern="^(title|description|steps|status)$"),
    new_value: str = Body(..., media_type="text/plain"),
    db: SQLiteDatabase = Depends(get_db)
):
    """Update bug field - PUT + plain text body"""
    bug = db.read("bugs", id=bug_id)
    if not bug:
        return "Bug not found"

    db.update("bugs", bug_id, **{field: new_value})
    return f"Bug {bug_id} field '{field}' updated to: {new_value}"


@api.post("/bugs/{bug_id}/attachments")
async def attach_file(
    bug_id: int,
    file: UploadFile = File(...),
    db: SQLiteDatabase = Depends(get_db)
):
    """Add attachment to bug - POST + file upload"""
    bug = db.read("bugs", id=bug_id)
    if not bug:
        return {"error": "Bug not found"}

    attachments = bug.get("attachments")
    if attachments:
        attachments = f"{attachments},{file.filename}"
    else:
        attachments = file.filename

    db.update("bugs", bug_id, attachments=attachments)

    return {
        "bug_id": bug_id,
        "filename": file.filename,
        "content_type": file.content_type
    }


@api.get("/testers")
async def list_testers(db: SQLiteDatabase = Depends(get_db)):
    """Get all testers"""
    return db.read("testers")


@api.get("/bugs")
async def list_bugs(
    tester_id: Optional[int] = None,
    status: Optional[str] = None,
    db: SQLiteDatabase = Depends(get_db)
):
    """Get all bugs or filter by tester_id and/or status"""
    if tester_id and status:
        return db.read("bugs", tester_id=tester_id, status=status)
    elif tester_id:
        return db.read("bugs", tester_id=tester_id)
    elif status:
        return db.read("bugs", status=status)
    else:
        return db.read("bugs")