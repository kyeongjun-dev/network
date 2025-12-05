# network
파이썬을 이용한 네트워크 소켓부터 eks의 istio까지 패킷 분석을 해봅니다. (내 마음대로)

## app
client.py에 사용하는 환경변수
```
HOST # default localhost
PORT # default 8000
HOST_HEADER # default HOST
USE_TLS (true, false) # default false
```

endpoint
```
/
/slow-response?wait=10
```

cmd
```
gunicorn --workers 1 -k gevent --bind 0.0.0.0:8000 --timeout 10 --keep-alive 10 app:app --log-level debug
```

컨테이너 이미지
```
docker pull ghcr.io/kyeongjun-dev/network:dev
```