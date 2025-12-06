from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask App behind Gunicorn!"

@app.route('/slow')
def slow():
    try:
        wait_time = request.args.get('wait', default=10, type=int)
    except ValueError:
        # 쿼리 파라미터가 정수가 아닌 경우 10초를 사용합니다.
        wait_time = 10

    print(f"Request received. Busy waiting for {wait_time} seconds...")
    # CPU를 계속 사용하는 반복문 사용
    end_time = time.time() + wait_time
    while time.time() < end_time:
        pass  # 아무것도 안 하지만 CPU는 계속 씀 (Yield 안 함)

    print(f"Waited {wait_time} seconds. Sending response now.")
    return f"Finally, here is your slow response..."