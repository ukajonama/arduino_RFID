import serial
import sqlite3
from datetime import datetime
import os

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
