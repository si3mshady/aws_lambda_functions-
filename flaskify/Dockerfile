FROM alpine:3.12
WORKDIR /app
COPY . .
RUN apk update && \
    apk upgrade

RUN apk add   py-pip 

RUN pip install flask 
CMD ["python3","webserver.py"]