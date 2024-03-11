# Generated by Django 5.0.2 on 2024-03-04 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nmap", "0002_dnsresolveripv4_dnsresolveripv6_mailserver"),
    ]

    operations = [
        migrations.CreateModel(
            name="PortScanner",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("domain", models.TextField()),
                ("ip", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="PortTcpScannerLine",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("port", models.TextField()),
                ("protocol", models.TextField()),
                ("service", models.TextField()),
                ("state", models.TextField()),
                (
                    "scanner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nmap.portscanner",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="PortTcpScanner",
        ),
    ]
