import socket
import time
import errno
import sys
import os   # 환경변수 사용을 위해 추가
import ssl  # TLS 지원을 위해 추가

# --- 1. 환경변수 및 기본 설정 로직 ---
# os.getenv('환경변수명', '기본값')
HOST = os.getenv('HOST', 'localhost')

# PORT는 환경변수로 받으면 문자열이므로 int로 변환
try:
    PORT = int(os.getenv('PORT', 8000))
except ValueError:
    print("Warning: Invalid PORT environment variable. Using default 8000.")
    PORT = 8000

HOST_HEADER = os.getenv('HOST_HEADER', HOST)

# TLS 사용 여부 확인 (환경변수 USE_TLS가 'true'거나 '1'이면 켜짐)
use_tls_env = os.getenv('USE_TLS', 'false').lower()
USE_TLS = use_tls_env in ('true', '1', 'yes')

# --- 2. TIME_INTERVAL 설정 로직 ---
TIME_INTERVAL = 60  # 기본값

try:
    if len(sys.argv) > 1:
        TIME_INTERVAL = int(sys.argv[1])
    else:
        # 자동화를 위해 환경변수가 설정되어 있거나, 사용자 입력이 없으면 넘어감
        print(f"Insert TIME_INTERVAL (default 60): ", end='', flush=True)
        # 3초 정도 기다리거나 하지 않고 바로 입력 받음 (기존 로직 유지)
        # 입력을 건너뛰고 싶다면 엔터를 누르면 됨
        import select
        # 윈도우/리눅스 호환 입력 처리는 복잡하므로 기존 로직 유지하되 안내 메시지 강화
        user_input = input() 
        
        if user_input:
            TIME_INTERVAL = int(user_input)

except ValueError:
    print(f"Error: Invalid input. Using default TIME_INTERVAL = 60s.")
    TIME_INTERVAL = 60
except KeyboardInterrupt:
    print("\nCanceled by user. Exiting.")
    sys.exit(0)

# --- 3. 설정 값 화면 출력 ---
print(f"\n================ CONFIGURATION ================")
print(f" HOST             : {HOST}")
print(f" PORT             : {PORT}")
print(f" USE TLS (HTTPS)  : {'Yes' if USE_TLS else 'No'}")
print(f" HOST HEADER      : {HOST_HEADER}")
print(f" TIME_INTERVAL    : {TIME_INTERVAL} seconds")
print(f"===============================================\n")

# --- 4. 요청 패킷 생성 ---
REQUEST_KEEP_ALIVE = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {HOST_HEADER}\r\n"
    f"Connection: keep-alive\r\n"
    f"\r\n"
).encode('utf-8')

print(f"--- Keep-Alive Test Started ---")
protocol = "https" if USE_TLS else "http"
print(f"Target: {protocol}://{HOST}:{PORT}") 
print(f"Sending 'GET /' request every {TIME_INTERVAL} seconds.")
print("Press Ctrl+C to stop the test.")

raw_socket = None  # TCP 원본 소켓
conn_socket = None # 실제 통신용 소켓 (TLS면 래핑된 소켓, 아니면 원본)

try:
    # 1. 소켓 생성 및 TCP 연결
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to {HOST}:{PORT} (TCP)...")
    raw_socket.connect((HOST, PORT))
    print("TCP Connected!")

    # 2. TLS 핸드셰이크 (옵션)
    if USE_TLS:
        # 제공해주신 TLS 로직
        print("Performing TLS Handshake...")
        # create_default_context는 기본적으로 인증서 검증을 수행함
        context = ssl.create_default_context()
        
        # 만약 사설 인증서/localhost 테스트라 에러가 난다면 아래 주석 해제하여 검증 무시 가능
        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE
        
        # wrap_socket 반환값을 통신용 소켓으로 지정
        conn_socket = context.wrap_socket(raw_socket, server_hostname=HOST)
        print(f"TLS Handshake successful! (Cipher: {conn_socket.cipher()[0]})")
    else:
        # TLS가 아니면 원본 소켓을 그대로 사용
        conn_socket = raw_socket

    # 3. 첫 번째 요청 전송 (연결 확인용)
    print("\n--- Sending first request (GET /) ---")
    conn_socket.sendall(REQUEST_KEEP_ALIVE)
    
    # 4. 첫 번째 응답 수신
    response = conn_socket.recv(4096)
    if not response:
        print("\n*** TEST FAILED: Received empty response on first request. ***")
        raise socket.error("Server returned empty response on first request")
        
    print("--- Received first response ---")
    # 헤더 첫 줄만 출력
    print(response.decode('utf-8', errors='ignore').split('\r\n')[0])

    # 5. TIME_INTERVAL 간격으로 요청 무한 반복
    count = 1
    while True:
        print(f"\n--- Waiting for {TIME_INTERVAL} seconds... ---")
        time.sleep(TIME_INTERVAL)
        
        count += 1
        print(f"--- Sending keep-alive request #{count} (GET /) ---")
        conn_socket.sendall(REQUEST_KEEP_ALIVE)
        
        # 응답 수신
        response = conn_socket.recv(4096)
        
        if not response:
            print("\n*** TEST FAILED: Server closed connection (recv() returned 0 bytes) ***")
            raise socket.error(errno.ECONNRESET, "Connection closed by peer")
        
        print(f"--- Received response #{count} ---")
        print(response.decode('utf-8', errors='ignore').split('\r\n')[0])


except socket.error as e:
    if e.errno in (errno.ECONNRESET, errno.EPIPE):
        print(f"\n*** TEST FAILED: Connection was reset by peer! ***")
        print(f"Error (Code: {e.errno}): {e.strerror}")
    else:
        print(f"\n*** TEST FAILED: Caught unexpected socket error ***")
        print(f"Error: {e}")
except ssl.SSLError as e:
    print(f"\n*** TEST FAILED: SSL/TLS Error ***")
    print(f"Error: {e}")
except KeyboardInterrupt:
    req_count_str = f" after {count} requests" if 'count' in locals() else ""
    print(f"\n\n--- Test manually interrupted by user (Ctrl+C){req_count_str}. ---")
    print("*** TEST STOPPED ***")
except Exception as e:
    print(f"\n*** TEST FAILED: Caught a non-socket error ***")
    print(f"Error: {e}")

finally:
    # 소켓 정리
    if conn_socket:
        try:
            conn_socket.close()
        except:
            pass
    elif raw_socket:
        # TLS 핸드셰이크 전에 실패했을 경우를 대비
        try:
            raw_socket.close()
        except:
            pass
    print("\nSocket closed.")