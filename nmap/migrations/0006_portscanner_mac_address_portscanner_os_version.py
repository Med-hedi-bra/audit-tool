# Generated by Django 5.0.2 on 2024-03-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nmap", "0005_porttcpscannerline_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="portscanner",
            name="mac_address",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="portscanner",
            name="os_version",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
