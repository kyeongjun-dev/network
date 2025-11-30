import socket

try:
    # AF_INET : ipv4 사용, SOCK_STREAM : tcp 사용
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 30000))
    print("서버에 연결 시도...")
except ConnectionRefusedError:
    print("서버에 연결할 수 없습니다. 서버가 이미 종료된 것 같습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
finally:
    client_socket.close()