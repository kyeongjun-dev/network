import socket

timeout_duration = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 30000))
server_socket.listen()
print("클라이언트 접속을 기다립니다...")

# accept()는 블로킹 상태로 무한정 대기
client_socket, addr = server_socket.accept()
print(f"{addr} 에서 접속했습니다. 이제부터 {timeout_duration}초 내에 데이터를 보내야 합니다.")

# 'accept'로 생성된 클라이언트와의 통신 소켓에 타임아웃(timeout_duration) 설정
client_socket.settimeout(timeout_duration)

while True:
    try:
        # recv()는 데이터가 들어올 때까지 여기서 실행을 멈춤(blocking)
        # settimeout() 때문에 timeout_duration초가 지나면 socket.timeout 예외를 발생시킴
        data = client_socket.recv(1024)
        
        # 클라이언트가 연결을 정상적으로 종료한 경우
        if not data:
            print("클라이언트가 연결을 끊었습니다.")
            break
            
        print(f"수신 메시지: {data.decode('utf-8')}")
        client_socket.sendall("메시지를 잘 받았습니다!".encode('utf-8'))

    except socket.timeout:
        print(f"{timeout_duration}초 동안 데이터 수신이 없어 연결을 종료합니다.")
        break # while 루프 탈출
        
    except ConnectionResetError:
        print("클라이언트와의 연결이 비정상적으로 끊어졌습니다.")
        break

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        break

# 소켓 정리
print(f"{addr} 와의 연결을 닫습니다.")
client_socket.close()
server_socket.close()