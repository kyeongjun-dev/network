import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # docker compose의 호스트네임인 `server`로 변경
    client_socket.connect(('server', 30000))
    print("서버에 접속했습니다.")
    print("아무 내용이나 입력 후 엔터를 누르면 서버로 메시지를 보냅니다.")
    print("10초 이상 아무것도 안 하면 서버에서 연결이 끊깁니다.")
    print("종료하려면 'exit'을 입력하세요.")

    while True:
        wait_start_time = time.time()
        message = input("> ")
        print(f"{time.time() - wait_start_time}초 이후에 메시지를 전송합니다.")
        if message.lower() == 'exit':
            break

        client_socket.sendall(message.encode('utf-8'))
        
        data = client_socket.recv(1024)
        print(f"서버 응답: {data.decode('utf-8')}")

except ConnectionRefusedError:
    print("서버에 연결할 수 없습니다.")
except (ConnectionResetError, BrokenPipeError):
    print("서버에 의해 연결이 끊겼습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
    
finally:
    print("클라이언트를 종료합니다.")
    client_socket.close()