FROM python:3.13-slim
ENV PYTHONUNBUFFERED=TRUE

WORKDIR /app

RUN apt update -y && apt install -y procps net-tools vim tcpdump iproute2 curl

RUN mkdir -p /app/captures

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sleep", "infinity"]