import os

from django.conf import settings
from reportlab.pdfgen import canvas

from nmap.models import PortScannerReport
from nmap.services.PortScannerService import PortScannerService




class PortScannerReportService:

    @staticmethod
    def generate_report(idScanner,scannnerInstance):
        # to avoid circular import
        print("Generate report")
        scanner = PortScannerService.get_port_scanner_by_id(idScanner)
        ports_info = scanner["port_scanner_line"]
        scan_info = scanner["port_scanner"]
        filename = 'hello_world'+str(idScanner)+'.pdf'
        # filename = "hello_world.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        pdf = canvas.Canvas(file_path)

        # Set column widths
        col_widths = [80, 80, 120, 120, 80]
        headers = ["Protocol", "Port", "Service", "Service Version", "Status"]
        prt_scanner_line_attribut = [
            "protocol",
            "port",
            "service",
            "service_version",
            "state",
        ]

        # Set initial y coordinate for the table
        y = 700
        pdf.setFont("Helvetica-Bold", 12)

        pdf.drawString(50, y, "Domain:")
        pdf.drawString(150, y, scan_info["domain"])
        y -= 20
        pdf.drawString(50, y, "IP:")
        pdf.drawString(150, y, scan_info["ip"])
        y -= 20
        pdf.drawString(50, y, "OS Version:")
        pdf.drawString(150, y, scan_info["os_version"])
        y -= 20
        pdf.drawString(50, y, "Mac address:")
        pdf.drawString(150, y, scan_info["mac_address"])
        y -= 20
        pdf.drawString(50, y, "Uptime:")
        pdf.drawString(150, y, scan_info["uptime_in_days"] + " days")
        y -= 20
        pdf.drawString(50, y, "Network Disance:")
        pdf.drawString(150, y, scan_info["network_distance_in_hops"] + " hops")

        y -= 40

        # Draw table headers
        pdf.setFont("Helvetica-Bold", 12)
        x = 50
        for header, width in zip(headers, col_widths):
            pdf.drawString(x, y, header)
            x += width

        # Draw table rows
        pdf.setFont("Helvetica", 10)
        y -= 20  # Move y coordinate up for the first row
        for row in ports_info:
            x = 50
            for width, header in zip(col_widths, prt_scanner_line_attribut):
                pdf.drawString(x, y, str(row[header]))
                x += width
            y -= 20  # Move y coordinate down for the next row

        pdf.save()
        # save the report in the DB
        PortScannerReport.objects.create(
            port_scanner=scannnerInstance,
            filename=filename,
        )

        # Return the filename that will be in be assets folder
        return filename

    @staticmethod
    def get_report_by_id(id):
        report = PortScannerReport.objects.get(port_scanner=id)
        return report.filename