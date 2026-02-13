from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/user")
def get_user(user_id: int):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # ❌ 故意写不安全 SQL（SQL 注入风险）
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

    result = cursor.fetchall()

    # ❌ 没有关闭连接
    return {"data": result}
