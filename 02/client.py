import socket
import time

timeout_duration = 10  # 총 대기 시간 (초)
start_time = time.time() # 시작 시간 기록

# 반복문을 돌면서 소켓을 신규로 생성해서 연결 시도
while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 타임아웃 설정 (연결 과정 자체가 느린 경우를 대비)
        client_socket.settimeout(5)

        client_socket.connect(('127.0.0.1', 30000))
        print("서버에 연결 시도...")

        # 연결 성공 시 반복문 탈출
        break
    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다. 1초 후 재시도 합니다.")

        # 재시도 하는 로직 추가
        time.sleep(1)
        if time.time() - start_time > timeout_duration:
            print(f"{timeout_duration}초를 초과해서 종료합니다.")
            break
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
    finally:
        client_socket.close()

# 연결 성공 후 로직 (예: client_socket이 닫히지 않은 경우)
if client_socket and client_socket.fileno() != -1:
    # 여기서 데이터 통신 로직 수행
    try:
        # 예시: 데이터 전송
        # client_socket.sendall(b'Hello')
        pass
    finally:
        client_socket.close()