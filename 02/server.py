import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 30000))
server_socket.listen()

timeout_duration = 10  # 총 대기 시간 (초)

try:
    # 서버 소켓이 클라이언트의 접속을 기다리는 시간을 timeout_duration으로 설정
    server_socket.settimeout(timeout_duration)
    
    client_socket, addr = server_socket.accept()
    print(f"{addr} 에서 접속했습니다.")
    
    client_socket.close()
except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    server_socket.close()
    print("서버 소켓을 닫았습니다.")