import socket

timeout_duration = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# docker compose의 호스트네임인 `server`로 변경
server_socket.bind(('server', 30000))
server_socket.listen()
print("클라이언트 접속을 기다립니다...")

client_socket, addr = server_socket.accept()
print(f"{addr} 에서 접속했습니다. 이제부터 {timeout_duration}초 내에 데이터를 보내야 합니다.")

client_socket.settimeout(timeout_duration)

while True:
    try:
        data = client_socket.recv(1024)
        
        if not data:
            print("클라이언트가 연결을 끊었습니다.")
            break
            
        print(f"수신 메시지: {data.decode('utf-8')}")
        client_socket.sendall("메시지를 잘 받았습니다!".encode('utf-8'))

    except socket.timeout:
        print(f"{timeout_duration}초 동안 데이터 수신이 없어 연결을 종료합니다.")
        break
        
    except ConnectionResetError:
        print("클라이언트와의 연결이 비정상적으로 끊어졌습니다.")
        break

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        break

print(f"{addr} 와의 연결을 닫습니다.")
client_socket.close()
server_socket.close()