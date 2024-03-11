# Generated by Django 5.0.2 on 2024-03-11 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nmap", "0030_remove_portscannerreport_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="portscannerreport",
            name="port_scanner",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                primary_key=True,
                serialize=False,
                to="nmap.portscanner",
            ),
        ),
    ]
