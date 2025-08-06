"""
FROM python:3.11-slim

# Set the working directory
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /bot

# 更新・日本語化
RUN apt-get update && apt-get -y install locales && apt-get -y upgrade && \
	localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm

# pip install
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot

# ポート開放 (uvicornで指定したポート)
EXPOSE 8080

# 実行
CMD python app/main.py
"""



# ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリを指定
WORKDIR /bot

# ロケールの設定（日本語化）
RUN apt-get update && apt-get -y install locales && apt-get -y upgrade && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ Asia/Tokyo
ENV TERM xterm

# 必要な依存パッケージをインストール
COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトファイルを全てコピー
COPY . /bot

# ポートを環境変数で指定
ENV PORT 8080

# ポート開放 (FastAPI + uvicornが使用するポート)
EXPOSE 8080

# entrypoint.shを実行
ENTRYPOINT ["/bin/bash", "/bot/entrypoint.sh"]
