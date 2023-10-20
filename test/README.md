## Test

Steps to test urbackup-exporter in local:

1. Deploy UrBackup server (you can deploy the exporter too):
```bash
docker-compose -f docker-compose-test.yml up -d
```

2. Add a new client in UrBackup UI:
* http://127.0.0.1:55414/
* Click in "Add new client", enter a name and click in "Add client".

3. Start urbackup-exporter with these environment variables:
```bash
URBACKUP_SERVER_URL=http://127.0.0.1:55414/x
LOG_LEVEL=DEBUG
```

4. Access urbackup-exporter metrics:
* http://127.0.0.1:9554/
