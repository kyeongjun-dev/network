import socket

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 30000))
server_socket.listen()

try:
    # accept()는 클라이언트가 연결할 때까지 여기서 실행을 멈춤(blocking)
    client_socket, addr = server_socket.accept()
    print(f"{addr} 에서 접속했습니다.")
    
    # 연결 성공 후 로직 (여기서는 간단히 연결 종료)
    client_socket.close()
except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    # 소켓 정리
    server_socket.close()
    print("서버 소켓을 닫았습니다.")