FROM python:3.13-slim
ENV PYTHONUNBUFFERED=TRUE

WORKDIR /app

RUN apt update -y && apt install -y procps net-tools vim tcpdump iproute2

RUN mkdir -p /app/captures

COPY . .

CMD ["sleep", "infinity"]