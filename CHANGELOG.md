# Changelog

## 1.1.3 / 2022/12/06

* Update dependencies and base Docker image
* Add ppc64le & s390x architectures for Alpine, remove mips64le from Debian
* Update Grafana Dashboard

## 1.1.2 / 2022/01/22

* Avoid re-login in each request

## 1.1.1 / 2022/01/15

* Update dependencies and base Docker image
* Update readme

## 1.1.0 / 2021-10-09

* Improve logger to display datetime and reduce error verbosity. Use `TZ=Europe/Madrid` env var to configure timezone
* Add new env var `LOG_LEVEL=INFO` to set the log level
* Update documentation. Reorder sections and include an example to configure Prometheus.

## 1.0.0 / 2021-07-04

* First release
* Tested with UrBackup server 2.4.13
