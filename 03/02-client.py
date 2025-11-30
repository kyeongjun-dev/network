import socket
import time

timeout_duration = 10
start_time = time.time()

while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_socket.settimeout(5)

        # docker compose의 호스트네임인 `server`로 변경
        client_socket.connect(('server', 30000))
        print("서버에 연결 시도...")
        break
    except ConnectionRefusedError:
        print("서버에 연결할 수 없습니다. 1초 후 재시도 합니다.")

        time.sleep(1)
        if time.time() - start_time > timeout_duration:
            print(f"{timeout_duration}초를 초과해서 종료합니다.")
            break
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
    finally:
        client_socket.close()

if client_socket and client_socket.fileno() != -1:
    try:
        # 예시: 데이터 전송
        # client_socket.sendall(b'Hello')
        pass
    finally:
        client_socket.close()