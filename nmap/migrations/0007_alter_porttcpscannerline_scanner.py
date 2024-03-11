# Generated by Django 5.0.2 on 2024-03-08 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nmap", "0006_portscanner_mac_address_portscanner_os_version"),
    ]

    operations = [
        migrations.AlterField(
            model_name="porttcpscannerline",
            name="scanner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scannerLine",
                to="nmap.portscanner",
            ),
        ),
    ]
