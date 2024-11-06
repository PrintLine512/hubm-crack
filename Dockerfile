FROM python:3.11-slim
#FROM ubuntu:22.04
WORKDIR /app

# Копируем файл crack.py в контейнер
COPY crack.py /app/crack.py

# Устанавливаем необходимые пакеты и загружаем UPX
RUN apt-get update && apt-get install -y wget xz-utils && \
    mkdir -p /app/upx && \
    wget https://github.com/upx/upx/releases/download/v4.2.4/upx-4.2.4-amd64_linux.tar.xz && \
    tar -xJf upx-4.2.4-amd64_linux.tar.xz -C /app/upx --strip-components=1 && \
    rm upx-4.2.4-amd64_linux.tar.xz

# Указываем команду, которая будет выполнена при запуске контейнера
ENTRYPOINT ["python", "/app/crack.py"]
