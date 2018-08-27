FROM alpine

RUN apk add --no-cache ca-certificates bash git curl python py-pip



COPY . /app
ADD . /app

WORKDIR /app
EXPOSE 80
EXPOSE 6543

RUN pip install -e .
RUN pip install -r remove_local_modules.txt

ENTRYPOINT ["pserve", "development.ini", "--reload"]
