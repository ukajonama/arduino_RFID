from flask import Flask, render_template, jsonify
from threading import Thread
import serial
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Flask route 설정
@app.route('/')
def home():
    return render_template('test.html')

@app.route('/time')
def index():
    # 현재 날짜를 가져옵니다.
    now = datetime.now()
    year = now.year
    month = now.strftime('%m')
    day = now.strftime('%d')

    # 데이터베이스 디렉토리 경로 설정
    database_dir = os.path.join(os.getcwd(), f"{year}", f"{month}-{day}")

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

@app.route('/data')
def get_data():
    # 현재 날짜를 가져옵니다.
    now = datetime.now()
    year = now.year
    month = now.strftime('%m')
    day = now.strftime('%d')

    # 데이터베이스 디렉토리 경로 설정
    database_dir = os.path.join(os.getcwd(), f"{year}", f"{month}-{day}")

    # SQLite 데이터베이스 경로 설정
    db_path = os.path.join(database_dir, 'database.db')

    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 데이터베이스에서 사용자 및 시간 데이터 가져오기
    cursor.execute('SELECT * FROM user_logs')
    rows = cursor.fetchall()
    conn.close()

    # JSON 형태로 데이터 반환
    return jsonify(rows)

def run_flask_app():
    app.run()

def run_serial_reader():
    # 시리얼 포트 설정
    ser = serial.Serial('COM5', 9600)  # 포트와 보드레이트에 맞게 설정해주세요

    # 데이터베이스 디렉토리 생성
    database_dir = datetime.now().strftime('%Y/%m-%d')
    os.makedirs(database_dir, exist_ok=True)

    # SQLite 데이터베이스 경로 설정
    db_path = os.path.join(database_dir, 'database.db')

    # SQLite 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 테이블 생성 (한 번만 실행)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logs (
            uid TEXT,
            timestamp TEXT
        )
    ''')

    while True:
        # 시리얼 데이터 읽기
        uid = ser.readline().decode().strip()
        # uid 구분
        if uid == "232 251 18 13":
            uid = "김두한"
        elif uid == "83 224 214 52":
            uid = "심영"
        elif uid == "228 218 134 164":
            uid = "정상범"
        else :
            uid += "신원불명"


        # 현재 시간 가져오기
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 사용자 및 시간 데이터를 SQLite에 삽입
        cursor.execute('INSERT INTO user_logs (uid, timestamp) VALUES (?, ?)', (uid, timestamp))
        conn.commit()

        # 콘솔에 사용자 및 시간 정보 출력
        print(f"UID: {uid}, Timestamp: {timestamp}")

        # 새로운 날짜인 경우 데이터베이스 연결을 업데이트
        if datetime.now().strftime('%Y/%m-%d') != database_dir:
            database_dir = datetime.now().strftime('%Y/%m-%d')
            os.makedirs(database_dir, exist_ok=True)
            db_path = os.path.join(database_dir, 'database.db')
            conn.close()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

    # 연결 종료
    conn.close()

if __name__ == '__main__':
    # Flask 애플리케이션과 시리얼 통신 코드를 각각 별도의 스레드로 실행
    flask_thread = Thread(target=run_flask_app)
    serial_thread = Thread(target=run_serial_reader)

    flask_thread.start()
    serial_thread.start()

    app.run(host='0.0.0.0', debug= True,port=8080)
