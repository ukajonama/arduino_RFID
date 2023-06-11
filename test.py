from flask import Flask, render_template
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    # 현재 날짜를 가져옵니다.
    now = datetime.now()
    year = now.year
    month = now.strftime('%m')
    day = now.strftime('%d')

    # 데이터베이스 디렉토리 경로 설정
    database_dir = os.path.join(os.getcwd(), "2023","06-10")
    
    # SQLite 데이터베이스 경로 설정
    db_path = os.path.join(database_dir, 'database.db')

    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 데이터베이스에서 사용자 및 시간 데이터 가져오기
    cursor.execute('SELECT * FROM user_logs')
    rows = cursor.fetchall()
    conn.close()

    # 템플릿에 데이터 전달
    return render_template('time.html', rows=rows)


if __name__ == '__main__':
    app.run()
