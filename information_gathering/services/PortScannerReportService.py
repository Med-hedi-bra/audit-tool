import os

from django.conf import settings
from reportlab.pdfgen import canvas

from ..models import PortScannerReport
from .PortScannerService import PortScannerService
from application import logger




class PortScannerReportService:

    @staticmethod
    def generate_report(scannerInstance):
        try:
            logger.info("Generating report")

            # Retrieve scanner information
            scanner = PortScannerService.get_port_scanner_by_id(scannerInstance.id)
            ports_info = scanner["port_scanner_line"]
            scan_info = scanner["port_scanner"]

            # Set filename for the report
            filename = f'hello_world{scannerInstance.id}.pdf'
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Create PDF canvas
            pdf = canvas.Canvas(file_path)

            # Set column widths and headers
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

            # Write scanner information to the PDF
            info_fields = [
                ("Domain:", scan_info["domain"]),
                ("IP:", scan_info["ip"]),
                ("OS Version:", scan_info["os_version"]),
                ("Mac address:", scan_info["mac_address"]),
                ("Uptime:", f"{scan_info['uptime_in_days']} days"),
                ("Network Distance:", f"{scan_info['network_distance_in_hops']} hops"),
            ]
            for label, value in info_fields:
                pdf.drawString(50, y, label)
                pdf.drawString(150, y, value)
                y -= 20

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

            # Save the report in the DB
            PortScannerReport.objects.create(
                port_scanner=scannerInstance,
                filename=filename,
            )

            logger.info("Report generated successfully")
            # Return the filename that will be in the assets folder
            return filename
        except Exception as e:
            logger.error(f"Error occurred during report generation: {e}")
            return None
    @staticmethod
    def get_report_by_id(id):
        try:
            logger.info(f"Retrieving report with ID: {id}")
            
            report = PortScannerReport.objects.get(port_scanner=id)
            filename = report.filename
            
            logger.info(f"Report retrieved successfully with ID: {id}")
            return filename
        except PortScannerReport.DoesNotExist:
            logger.error(f"Report with ID {id} does not exist")
            return None
        except Exception as e:
            logger.error(f"Error occurred while retrieving report with ID {id}: {e}")
            return None