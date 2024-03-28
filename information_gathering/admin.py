from django.contrib import admin
from .models import (
    PortScannerLine,
    PortScanner,
    DnsResolverIpv4,
    DnsResolverIpv6,
    MailServer,
    PortScannerReport,
)

# Register your models here.
admin.site.register(PortScanner)
admin.site.register(PortScannerLine)
admin.site.register(DnsResolverIpv4)
admin.site.register(DnsResolverIpv6)
admin.site.register(MailServer)
admin.site.register(PortScannerReport)
