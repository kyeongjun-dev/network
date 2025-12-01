import socket
import time
import errno
import sys  # 1. sys 모듈 임포트

# --- TIME_INTERVAL 설정 로직 ---
TIME_INTERVAL = 60  # 2. 기본값 60초

try:
    if len(sys.argv) > 1:
        # 3. 커맨드라인 인자(argv[1])가 있으면, 그것을 TIME_INTERVAL로 사용
        TIME_INTERVAL = int(sys.argv[1])
    else:
        # 4. 커맨드라인 인자가 없으면, 사용자에게 입력받음
        user_input = input('insert TIME_INTERVAL (default 60): ')
        
        if user_input:
            # 5. 사용자가 값을 입력한 경우
            TIME_INTERVAL = int(user_input)
        # (사용자가 아무것도 입력하지 않으면(Enter), 기본값 60이 사용됨)

except ValueError:
    print(f"Error: Invalid input. Using default TIME_INTERVAL = 60s.")
    TIME_INTERVAL = 60
except KeyboardInterrupt:
    print("\nCanceled by user. Exiting.")
    sys.exit(0)
# ------------------------------


# --- 설정 ---
HOST = 'server'
PORT = 8000
YOUR_HOST_HEADER = 'server'
# -----------

# 사용할 요청 (GET /)
REQUEST_KEEP_ALIVE = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {YOUR_HOST_HEADER}\r\n"
    # keep alive 연결 명시
    f"Connection: keep-alive\r\n"
    f"\r\n"
).encode('utf-8')


print(f"\n--- Keep-Alive Test (Non-TLS) ---")
# 6. http:// 스키마 및 포트 번호 명시
print(f"Target: http://{HOST}:{PORT}") 
print(f"Sending 'GET /' request every {TIME_INTERVAL} seconds.")
print("Press Ctrl+C to stop the test.")

s = None # finally 블록에서 s를 참조할 수 있도록 외부에 선언
try:
    # 1. 소켓 생성 연결 (Non-TLS)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to {HOST}:{PORT} (TCP)...")
    s.connect((HOST, PORT))
    print("TCP Connected!")

    # 2. 첫 번째 요청 전송 (연결 확인용)
    print("\n--- Sending first request (GET /) ---")
    s.sendall(REQUEST_KEEP_ALIVE)
    
    # 3. 첫 번째 응답 수신
    response = s.recv(4096)
    if not response:
        print("\n*** TEST FAILED: Received empty response on first request. ***")
        raise socket.error("Server returned empty response on first request")
        
    print("--- Received first response ---")
    print(response.decode('utf-8', errors='ignore').split('\r\n')[0])

    # 4. TIME_INTERVAL 간격으로 요청 무한 반복
    count = 1
    while True:
        print(f"\n--- Waiting for {TIME_INTERVAL} seconds... ---")
        time.sleep(TIME_INTERVAL)
        
        count += 1
        print(f"--- Sending keep-alive request #{count} (GET /) ---")
        s.sendall(REQUEST_KEEP_ALIVE)
        
        # 응답 수신
        response = s.recv(4096)
        
        # 서버가 연결을 닫았는지 확인 (0바이트 수신)
        if not response:
            print("\n*** TEST FAILED: Server closed connection (recv() returned 0 bytes) ***")
            raise socket.error(errno.ECONNRESET, "Connection closed by peer (recv() returned 0)")
        
        print(f"--- Received response #{count} ---")
        print(response.decode('utf-8', errors='ignore').split('\r\n')[0])


except socket.error as e:
    # 5. 연결이 끊어지면 "실패"로 간주 (Keep-Alive 실패)
    if e.errno in (errno.ECONNRESET, errno.EPIPE):
        print(f"\n*** TEST FAILED: Connection was reset by peer! ***")
        print(f"Error (Code: {e.errno}): {e.strerror}")
    else:
        print(f"\n*** TEST FAILED: Caught unexpected socket error ***")
        print(f"Error (Code: {e.errno}): {e.strerror}")
except KeyboardInterrupt:
    # 6. 사용자가 Ctrl+C로 정상 종료
    # (루프가 시작되기 전에 중단될 경우 'count' 변수가 없을 수 있어 'locals()'로 확인)
    req_count_str = f" after {count} requests" if 'count' in locals() else ""
    print(f"\n\n--- Test manually interrupted by user (Ctrl+C){req_count_str}. ---")
    print("*** TEST STOPPED ***")
except Exception as e:
    print(f"\n*** TEST FAILED: Caught a non-socket error ***")
    print(f"Error: {e}")

finally:
    if s:
        try:
            # 소켓을 닫기 전에 남은 데이터를 싹 비웁니다.
            s.settimeout(0.1) # 타임아웃을 짧게 설정
            while True:
                data = s.recv(4096)
                if not data: break
        except Exception:
            pass # 타임아웃이나 에러가 나면 그냥 무시
            
        s.close() # 이제 버퍼가 비었으므로 FIN을 보냄
        print("\nSocket closed.")