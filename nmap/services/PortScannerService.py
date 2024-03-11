
import os
from reportlab.pdfgen import canvas

from django.conf import settings
from nmap.models import PortScanner
from nmap.serializers import PortScannerReportSerializer, PortScannerSerializer, PortScannerLineSerializer


class PortScannerService:

    @staticmethod 
    def get_all_port_scanner():
        answer = []
        port_scanner = PortScanner.objects.all()
        for port_scanner_item in port_scanner:
            port_scanner_line = port_scanner_item.portscannerline_set.all()
            port_scanner_data = PortScannerSerializer(port_scanner_item).data
            port_scanner_line_data = PortScannerLineSerializer(
                port_scanner_line, many=True
            ).data
            answer.append(
                {
                    "port_scanner": port_scanner_data,
                    "port_scanner_line": port_scanner_line_data,
                }
            )
        return answer

    @staticmethod
    def get_port_scanner_by_id(id):
        port_scanner = PortScanner.objects.get(id=id)
        port_scanner_line = port_scanner.portscannerline_set.all()
        port_scanner_data = PortScannerSerializer(port_scanner).data
        port_scanner_line_data = PortScannerLineSerializer(
            port_scanner_line, many=True
        ).data
        answer = {
            "port_scanner": port_scanner_data,
            # "port_scanner_report": port_scanner_report_data,
            "port_scanner_line": port_scanner_line_data,
        }
        return answer

    @staticmethod
    def create_port_scanner(ip, domain, os_version, mac_address, uptime_in_days, network_distance_in_hops,port_info=[]):
 
        port_scanner = PortScanner.objects.create(
            ip=ip,
            domain=domain,
            os_version=os_version,
            mac_address=mac_address,
            idUser=1,
            uptime_in_days=uptime_in_days,
            network_distance_in_hops=network_distance_in_hops,
        ) 
        for element in port_info:
            port_scanner.portscannerline_set.create(
                port=element["port"],
                protocol=element["protocol"],
                service=element["service"],
                state=element["state"],
                service_version=element["service_version"],
            )
        from .PortScannerReportService import PortScannerReportService
        PortScannerReportService.generate_report(port_scanner.id,port_scanner)
        return PortScannerSerializer(port_scanner).data


        

       
        