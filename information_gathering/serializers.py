from rest_framework import serializers



from .models import (
    PortScannerLine,
    DnsResolverIpv4,
    DnsResolverIpv6,
    MailServer,
    PortScanner,
    PortScannerReport,
)


class PortScannerLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortScannerLine
        fields = ["id", "port", "protocol", "service", "state","service_version"]

class PortScannerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortScannerReport
        fields = ["id", "filename"]

class PortScannerSerializer(serializers.ModelSerializer):
    scanner_line = PortScannerLineSerializer(many=True, read_only=True)
    class Meta:
        model = PortScanner
        fields = ["id","created_at", "domain", "ip","scanner_line","os_version","mac_address","uptime_in_days","network_distance_in_hops", "idUser"]


class DnsResolverIpv4Serializer(serializers.ModelSerializer):
    class Meta:
        model = DnsResolverIpv4
        fields = ["id", "host", "ipv4"]


class DnsResolverIpv6Serializer(serializers.ModelSerializer):
    class Meta:
        model = DnsResolverIpv6
        fields = ["id", "host", "ipv6"]


class MailServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailServer
        fields = ["id", "host", "server", "priority"]
        

