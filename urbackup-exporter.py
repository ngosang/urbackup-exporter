#!/usr/bin/env python3

import os
import time

import prometheus_client
import prometheus_client.core
import urbackup_api


class UrbackupCollector(object):
    def __init__(self, server, username, password, export_client_backups):
        self.server = server
        self.username = username
        self.password = password
        self.export_client_backups = export_client_backups
        # test connection
        urbackup_api.urbackup_server(self.server, self.username, self.password)

    def collect(self):

        common_label_names = [
            "client_name",
            "client_group",
            "client_id",
            "client_version",
            "client_os_version"
        ]

        client_online = prometheus_client.core.GaugeMetricFamily(
            "urbackup_client_online",
            "Whether or not the client is answering the server",
            labels=common_label_names)

        client_status = prometheus_client.core.GaugeMetricFamily(
            "urbackup_client_status",
            "Status number, purpose unknown",
            labels=common_label_names)

        client_lastseen = prometheus_client.core.GaugeMetricFamily(
            "urbackup_client_lastseen",
            "Timestamp the client was last seen online",
            labels=common_label_names)

        backup_ok = prometheus_client.core.GaugeMetricFamily(
            "urbackup_backup_ok",
            "Whether or not the last backup was successful",
            labels=common_label_names + ["backup_type"])

        backup_issues = prometheus_client.core.GaugeMetricFamily(
            "urbackup_backup_issues",
            "Number of issues during the last backup",
            labels=common_label_names + ["backup_type"])

        backup_lasttime = prometheus_client.core.GaugeMetricFamily(
            "urbackup_backup_lasttime",
            "Timestamp of the last backup",
            labels=common_label_names + ["backup_type"])

        backup_number_total = prometheus_client.core.CounterMetricFamily(
            "urbackup_backup_number_total",
            "Number of backups",
            labels=common_label_names + ["backup_type", "archived"])

        backup_size_total = prometheus_client.core.CounterMetricFamily(
            "urbackup_backup_size_total",
            "Total size of backups in bytes",
            labels=common_label_names + ["backup_type", "archived"])

        api = urbackup_api.urbackup_server(self.server, self.username, self.password)
        for client in api.get_status():
            common_label_values = [
                client["name"],
                client.get("groupname", "N/A"),
                str(client["id"]),
                client.get("client_version_string", "N/A"),
                client.get("os_version_string", "N/A")
            ]

            client_online.add_metric(common_label_values, float(client["online"]))
            client_status.add_metric(common_label_values, float(client["status"]))
            client_lastseen.add_metric(common_label_values, self.float_or_default(client["lastseen"], 0.0))
            backup_ok.add_metric(common_label_values + ["file"], float(client["file_ok"]))
            backup_ok.add_metric(common_label_values + ["image"], float(client["image_ok"]))
            backup_issues.add_metric(common_label_values + ["file"],
                                     self.float_or_default(client["last_filebackup_issues"], 0.0))
            backup_lasttime.add_metric(common_label_values + ["file"],
                                       self.float_or_default(client["lastbackup"], 0.0))
            backup_lasttime.add_metric(common_label_values + ["image"],
                                       self.float_or_default(client["lastbackup_image"], 0.0))

            if self.export_client_backups:
                count_archived, count_no_archived, size_archived, size_no_archived = self.calc_client_backups(
                    api.get_clientbackups(client["id"]))
                backup_number_total.add_metric(common_label_values + ["file", "yes"], count_archived)
                backup_number_total.add_metric(common_label_values + ["file", "no"], count_no_archived)
                backup_size_total.add_metric(common_label_values + ["file", "yes"], size_archived)
                backup_size_total.add_metric(common_label_values + ["file", "no"], size_no_archived)
                count_archived, count_no_archived, size_archived, size_no_archived = self.calc_client_backups(
                    api.get_clientimagebackups(client["id"]))
                backup_number_total.add_metric(common_label_values + ["image", "yes"], count_archived)
                backup_number_total.add_metric(common_label_values + ["image", "no"], count_no_archived)
                backup_size_total.add_metric(common_label_values + ["image", "yes"], size_archived)
                backup_size_total.add_metric(common_label_values + ["image", "no"], size_no_archived)

        yield client_online
        yield client_status
        yield client_lastseen
        yield backup_ok
        yield backup_issues
        yield backup_lasttime

        if self.export_client_backups:
            yield backup_number_total
            yield backup_size_total

    @staticmethod
    def calc_client_backups(client_backups):
        count_archived = 0
        size_archived = 0
        size_no_archived = 0
        for client_backup in client_backups:
            if client_backup["archived"] == 1:
                count_archived += 1
                size_archived += client_backup["size_bytes"]
            else:
                size_no_archived += client_backup["size_bytes"]
        count_no_archived = len(client_backups) - count_archived

        return count_archived, count_no_archived, size_archived, size_no_archived

    @staticmethod
    def float_or_default(x, default=0.0):
        try:
            return float(x)
        except ValueError:
            return default


if __name__ == "__main__":
    print("Starting UrBackup Prometheus Exporter ...")

    urbackup_server_url = os.environ["URBACKUP_SERVER_URL"]
    urbackup_server_username = os.environ.get("URBACKUP_SERVER_USERNAME", "admin")
    urbackup_server_password = os.environ.get("URBACKUP_SERVER_PASSWORD", "1234")
    export_client_backups = os.environ.get("EXPORT_CLIENT_BACKUPS", "true").lower() == "true"
    exporter_port = int(os.environ.get("LISTEN_PORT", 9554))
    exporter_address = os.environ.get("LISTEN_ADDRESS", "")

    prometheus_client.core.REGISTRY.register(UrbackupCollector(
        urbackup_server_url, urbackup_server_username, urbackup_server_password, export_client_backups))
    prometheus_client.start_http_server(exporter_port, exporter_address)
    print("Ready!")

    while True:
        time.sleep(60)
