import socket
import time
import errno
import sys
import os
import ssl

# --- 1. 환경변수 및 기본 설정 로직 ---
HOST = os.getenv('HOST', 'localhost')

try:
    PORT = int(os.getenv('PORT', 8000))
except ValueError:
    print("Warning: Invalid PORT environment variable. Using default 8000.")
    PORT = 8000

YOUR_HOST_HEADER = os.getenv('YOUR_HOST_HEADER', HOST)

# TLS 사용 여부
use_tls_env = os.getenv('USE_TLS', 'false').lower()
USE_TLS = use_tls_env in ('true', '1', 'yes')

# [NEW] 요청할 엔드포인트 설정 (기본값: /)
ENDPOINT = os.getenv('ENDPOINT', '/')

# --- 2. TIME_INTERVAL 설정 로직 ---
TIME_INTERVAL = 60 

try:
    if len(sys.argv) > 1:
        TIME_INTERVAL = int(sys.argv[1])
    else:
        # 사용자 편의를 위해 입력 대기 없이 넘어가는 것이 자동화에 유리하므로
        # 입력 안내만 하고 짧게 처리하거나, 여기서는 간단히 기본값 사용 안내만 출력합니다.
        # (필요시 input 로직 활성화 가능)
        print(f"Interval not specified. Using default TIME_INTERVAL = {TIME_INTERVAL}s")

except ValueError:
    print(f"Error: Invalid input. Using default TIME_INTERVAL = 60s.")
    TIME_INTERVAL = 60
except KeyboardInterrupt:
    sys.exit(0)

# --- 3. 설정 값 화면 출력 ---
print(f"\n================ CONFIGURATION ================")
print(f" HOST             : {HOST}")
print(f" PORT             : {PORT}")
print(f" USE TLS (HTTPS)  : {'Yes' if USE_TLS else 'No'}")
print(f" HOST HEADER      : {YOUR_HOST_HEADER}")
print(f" ENDPOINT         : {ENDPOINT}")  # [NEW] 화면 출력
print(f" TIME_INTERVAL    : {TIME_INTERVAL} seconds")
print(f"===============================================\n")

# --- 4. 요청 패킷 생성 ---
# f-string 안에 ENDPOINT 변수를 넣습니다.
REQUEST_KEEP_ALIVE = (
    f"GET {ENDPOINT} HTTP/1.1\r\n"
    f"Host: {YOUR_HOST_HEADER}\r\n"
    f"Connection: keep-alive\r\n"
    f"\r\n"
).encode('utf-8')

print(f"--- Keep-Alive Test Started ---")
protocol = "https" if USE_TLS else "http"
print(f"Target: {protocol}://{HOST}:{PORT}{ENDPOINT}") 
print(f"Sending 'GET {ENDPOINT}' request every {TIME_INTERVAL} seconds.")
print("Press Ctrl+C to stop the test.")

raw_socket = None
conn_socket = None 

try:
    # 1. 소켓 생성 및 TCP 연결
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to {HOST}:{PORT} (TCP)...")
    raw_socket.connect((HOST, PORT))
    print("TCP Connected!")

    # 2. TLS 핸드셰이크 (옵션)
    if USE_TLS:
        print("Performing TLS Handshake...")
        context = ssl.create_default_context()
        # context.check_hostname = False
        # context.verify_mode = ssl.CERT_NONE
        conn_socket = context.wrap_socket(raw_socket, server_hostname=HOST)
        print(f"TLS Handshake successful! (Cipher: {conn_socket.cipher()[0]})")
    else:
        conn_socket = raw_socket

    # 3. 첫 번째 요청 전송
    print(f"\n--- Sending first request (GET {ENDPOINT}) ---")
    conn_socket.sendall(REQUEST_KEEP_ALIVE)
    
    # 4. 첫 번째 응답 수신
    response = conn_socket.recv(4096)
    if not response:
        print("\n*** TEST FAILED: Received empty response on first request. ***")
        raise socket.error("Server returned empty response on first request")
        
    print("--- Received first response ---")
    print(response.decode('utf-8', errors='ignore').split('\r\n')[0])

    # 5. TIME_INTERVAL 간격으로 요청 무한 반복
    count = 1
    while True:
        print(f"\n--- Waiting for {TIME_INTERVAL} seconds... ---")
        time.sleep(TIME_INTERVAL)
        
        count += 1
        print(f"--- Sending keep-alive request #{count} (GET {ENDPOINT}) ---")
        conn_socket.sendall(REQUEST_KEEP_ALIVE)
        
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
    if conn_socket:
        try: conn_socket.close()
        except: pass
    elif raw_socket:
        try: raw_socket.close()
        except: pass
    print("\nSocket closed.")