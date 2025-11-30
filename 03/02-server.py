import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# docker compose의 호스트네임인 `server`로 변경
server_socket.bind(('server', 30000))
server_socket.listen()

timeout_duration = 10

try:
    server_socket.settimeout(timeout_duration)
    
    client_socket, addr = server_socket.accept()
    print(f"{addr} 에서 접속했습니다.")
    
    client_socket.close()
except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    server_socket.close()
    print("서버 소켓을 닫았습니다.")