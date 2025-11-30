# 1. 베이스 이미지 선택
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=TRUE

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 애플리케이션 코드 복사
COPY app.py .

# 5. Gunicorn이 사용할 포트 노출
EXPOSE 8000

ENV TIMEOUT=30
ENV KEEP_ALIVE=120

# 6. 컨테이너 실행 명령어
# Gunicorn을 사용하여 4개의 워커로 0.0.0.0:8000 주소에서 앱을 실행합니다.
CMD ["gunicorn", "--workers", "4", "-k", "gevent", "--bind", "0.0.0.0:8000", "--timeout", "${TIMEOUT}", "--keep-alive", "${KEEP_ALIVE}", "app:app"]