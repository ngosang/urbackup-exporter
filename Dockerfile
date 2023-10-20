FROM python:3.12-slim-bookworm

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY ./urbackup-exporter.py /urbackup-exporter.py

EXPOSE 9554
ENTRYPOINT ["/usr/local/bin/python", "-u", "/urbackup-exporter.py"]

# Help
#
# Local build
# docker build -t ngosang/urbackup-exporter:local .
#
# Multi-arch build
# docker buildx create --use
# docker buildx build -t ngosang/urbackup-exporter:local --platform linux/386,linux/amd64,linux/arm/v7,linux/arm64/v8,linux/ppc64le,linux/s390x .
#
# add --push to publish in DockerHub
