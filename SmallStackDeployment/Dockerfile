FROM  node:alpine

RUN mkdir cdk/ && apk add python3-dev && \
    apk add py-pip  && npm install -g aws-cdk

WORKDIR cdk/

CMD ["sh"]
