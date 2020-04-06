FROM  node:alpine

RUN mkdir cdk/ && apk add python3-dev && \
    apk add py-pip  && npm install -g aws-cdk && \
    pip3 install aws-cdk.aws_ec2 && pip3 install  aws_cdk.aws_iam &&\
    pip3 install boto3

WORKDIR cdk/

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["sh"]