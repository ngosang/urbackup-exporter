FROM python:3.9.6-alpine3.14

COPY ./requirements.txt /requirements.txt
COPY ./urbackup-exporter.py /urbackup-exporter.py

RUN pip install -r /requirements.txt && rm -rf /root/.cache/

EXPOSE 9554
ENTRYPOINT ["/usr/local/bin/python", "/urbackup-exporter.py"]

# HELP
# docker build -t ngosang/urbackup-exporter --platform linux/amd64 .