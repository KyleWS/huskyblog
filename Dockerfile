FROM alpine

RUN apk add --no-cache ca-certificates bash git curl python py-pip



COPY . /app
ADD . /app

WORKDIR /app
EXPOSE 80

RUN pip install -e .
RUN pip install -r requirements.txt

ENTRYPOINT ["/app"]
