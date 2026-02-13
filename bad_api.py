from fastapi import FastAPI
import sqlite3
from contextlib import closing

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    # ✅ 自动关闭连接 + 防SQL注入
    with closing(sqlite3.connect("test.db")) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()

    if row is None:
        return {"error": "not found"}

    # sqlite3.Row 转 dict
    return dict(row)
