from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask App behind Gunicorn!"

# 로드밸런서 유휴 시간 초과 재현을 위한 엔드포인트
@app.route('/slow-response')
def slow_response():
    # 'wait' 쿼리 파라미터를 가져옵니다.
    # 파라미터가 없으면 10초, 타입을 정수로 변환합니다.
    try:
        wait_time = request.args.get('wait', default=10, type=int)
    except ValueError:
        # 쿼리 파라미터가 정수가 아닌 경우 10초를 사용합니다.
        wait_time = 10
    
    # 음수 값이 들어오는 것을 방지합니다.
    if wait_time < 0:
        wait_time = 0

    print(f"Request received. Waiting for {wait_time} seconds...")
    time.sleep(wait_time)
    print(f"Waited {wait_time} seconds. Sending response now.")
    return f"Finally, here is your slow response after waiting {wait_time} seconds!"