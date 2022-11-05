FROM python:3.9

WORKDIR /opt/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libsndfile-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]