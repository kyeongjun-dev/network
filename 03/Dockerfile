# 1. 베이스 이미지 선택
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=TRUE

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 설치
RUN apt update -y && apt install -y procps net-tools vim tcpdump iproute2

# 4. 덤프 파일을 저장할 디렉터리 생성 (선택 사항이지만 명시적으로 좋음)
RUN mkdir -p /app/captures

# 5. 01, 02에서 사용한 파일 복사
COPY . .

# 6. just sleep
CMD ["sleep", "infinity"]