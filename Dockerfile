FROM python:3.12-slim-bookworm
WORKDIR /home/os-kafka-bridge
COPY . .

RUN apt-get update && \
    apt-get install -y librdkafka1 \
                       krb5-user \
                       libsasl2-modules-gssapi-mit \
                       librdkafka-dev \
                       libsasl2-dev \
                       libkrb5-dev \
                       libssl-dev \
                       g++ && \
                       pip install -r requirements.txt --no-cache-dir && \
                       apt-get -y remove libkrb5-dev libsasl2-dev librdkafka-dev libssl-dev g++ && \
    apt-get -y autoremove && \
    apt-get -y clean

CMD ["faststream", "run", "main:app"]