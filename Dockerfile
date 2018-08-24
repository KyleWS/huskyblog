FROM alpine

RUN apk add --no-cache ca-certificates bash git curl python py-pip

COPY ./requirements.txt / 


RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app


CMD ["pserve", "main:app"]
