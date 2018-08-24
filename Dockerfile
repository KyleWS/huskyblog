FROM python:3.6-alpine
RUN apk add --no-cache ca-certificates bash git curl

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["pserve", "development.ini"]
