FROM python:3.12-alpine
ENV TZ "Europe/Moscow"
RUN mkdir /home/bot
WORKDIR /home/bot
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev zbar zbar-dev
RUN python -m pip install --upgrade pip
ADD requirements.txt .
RUN pip install -U -r requirements.txt
ADD . .
CMD ["python3", "main.py"]
