FROM python:3.13-slim
ENV PYTHONUNBUFFERED=TRUE

WORKDIR /app

RUN apt update -y && apt install -y procps net-tools vim tcpdump iproute2

RUN mkdir -p /app/captures

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

ENV TIMEOUT=30
ENV KEEP_ALIVE=120

CMD ["sleep", "infinity"]