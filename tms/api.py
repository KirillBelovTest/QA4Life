# main.py
from fastapi import FastAPI, HTTPException
from tms.db import Tester, Bug, sqlite3

app = FastAPI()
conn = sqlite3.connect("tms.db", check_same_thread=False)

# создаем таблицы
cursor = conn.cursor()
cursor.execute(Tester.create_table())
cursor.execute(Bug.create_table())
conn.commit()

# API
@app.post("/testers")
def create_tester(name: str, level: str):
    if Tester.get_by_name(conn, name):
        raise HTTPException(400, "Tester exists")
    t = Tester(name, level)
    t.save(conn)
    return {"id": t.id, "name": t.name, "level": t.level}

@app.get("/testers")
def get_testers():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM testers")
    return [{"id": row[0], "name": row[1], "level": row[2]} for row in cursor.fetchall()]

@app.put("/testers/{name}")
def update_tester(name: str, level: str):
    t = Tester.get_by_name(conn, name)
    if not t:
        raise HTTPException(404, "Tester not found")
    t.update_level(conn, level)
    return {"id": t.id, "name": t.name, "level": t.level}

@app.post("/bugs")
def create_bug(title: str, description: str, tester_name: str):
    t = Tester.get_by_name(conn, tester_name)
    if not t:
        raise HTTPException(404, "Tester not found")
    b = Bug(title, description, t.id)
    b.save(conn)
    return {"id": b.id, "title": b.title, "status": b.status}

@app.put("/bugs/{bug_id}")
def update_bug_status(bug_id: int, status: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bugs WHERE id = ?", (bug_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(404, "Bug not found")
    b = Bug(row[1], row[2], row[4])
    b.id = row[0]
    b.status = row[3]
    b.update_status(conn, status)
    return {"id": b.id, "status": b.status}

@app.get("/bugs")
def get_bugs():
    bugs = Bug.get_all(conn)
    return [{"id": b.id, "title": b.title, "status": b.status} for b in bugs]