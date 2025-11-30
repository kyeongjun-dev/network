import socket

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # docker compose의 호스트네임인 `server`로 변경
    client_socket.connect(('server', 30000))
    print("서버에 연결 시도...")
except ConnectionRefusedError:
    print("서버에 연결할 수 없습니다. 서버가 이미 종료된 것 같습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
finally:
    client_socket.close()