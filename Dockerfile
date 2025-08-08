FROM python:3.11-slim

# Set the working directory
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# 更新・日本語化
RUN apt-get update && apt-get -y install locales && apt-get -y upgrade && \
	localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm

# pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

# ポート開放 (uvicornで指定したポート)
EXPOSE 8080

# 実行
CMD ["python", "app/main.py"]
