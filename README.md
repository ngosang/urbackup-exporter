# UrBackup Exporter

Prometheus exporter for the [UrBackup](https://www.urbackup.org/) backup system.

Inspired by [h3po work](https://gist.github.com/h3po/36cab38d2b443c0523c4c9e83203f382).

## Requirements

 * Python 3
 * [prometheus-client](https://github.com/prometheus/client_python)
 * [urbackup-server-web-api-wrapper](https://github.com/uroni/urbackup-server-python-web-api-wrapper)

Tested with UrBackup server 2.4.13.

## Configuration

All configuration is done with environment variables.

- `URBACKUP_SERVER_URL`: UrBackup server URL including host, port and API endpoint. Example: `http://192.168.1.100:55414/x`
- `URBACKUP_SERVER_USERNAME`: (Optional) Username to login in the server. Only required if authorization is enabled. The default is `admin`.
- `URBACKUP_SERVER_PASSWORD`: (Optional) Password to login in the server. Only required if authorization is enabled. The default is `1234`.
- `EXPORT_CLIENT_BACKUPS`: (Optional) Export detailed metrics for each client. This option can generate a lot of metrics if there many configured clients. The default is `true`.
- `LISTEN_PORT`: (Optional) The address the exporter should listen on. The default is `9554`.
- `LISTEN_ADDRESS`: (Optional) The address the exporter should listen on. The default is
   to listen on all addresses.

## Install

```bash
pip install -r /requirements.txt

export URBACKUP_SERVER_URL=http://192.168.1.100:55414/x
python urbackup-exporter.py
```

## Docker

TODO

## Exported metrics

| Name                          | Type    | Description                  |
| ----------------------------- | ------- | ---------------------------- |
| urbackup_client_online        | gauge   | Whether or not the client is answering the server |
| urbackup_client_status        | gauge   | Status number, purpose unknown |
| urbackup_client_lastseen      | gauge   | Timestamp the client was last seen online |
| urbackup_backup_ok            | gauge   | Whether or not the last backup was successful |
| urbackup_backup_issues        | gauge   | Number of issues during the last backup |
| urbackup_backup_lasttime      | gauge   | Timestamp of the last backup |
| urbackup_backup_number_total  | counter | Number of backups |
| urbackup_backup_size_total    | counter | Total size of backups in bytes |

## Grafana dashboard

TODO
