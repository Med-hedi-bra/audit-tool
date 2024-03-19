from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse
from nmap.services.DnsService import DnsService
from nmap.services.NmapService import NmapService
from nmap.services.PortScannerReportService import PortScannerReportService
from .services.PortScannerService import PortScannerService
import ipaddress
from django.conf import settings

import os
from django.views.decorators.csrf import csrf_exempt



@api_view(["GET"])
def get_all_port_scanner(request):
    port_scanners = PortScannerService.get_all_port_scanner()
    return JsonResponse(port_scanners, safe=False)

@api_view(["GET"])
def get_port_scanner_by_id(request,id):
    port_scanners = PortScannerService.get_port_scanner_by_id(id)
    return JsonResponse(port_scanners, safe=False)


@api_view(["POST"])
def get_host_infomations_by_domain(request):
    # the logic is to get all IPv4 addresses of the domain and then execute the port scan for each one
 
    if "domain" in request.data and request.data["domain"]:
        if "top_ports" in request.data:

            if (
                request.data["top_ports"]
                and request.data["top_ports"] > 0
                and request.data["top_ports"] < 65535
            ):
                top_ports = request.data["top_ports"]
            else:
                return JsonResponse({"Error": "The Top Port  is not valid"}, status=400)
        else:
            top_ports = None

        domain = request.data["domain"]
        DnsService.execute_collect_ipv4_ipv6_mail_server_by_domain(domain)
        all_dns_resolvers_json = (
            DnsService.get_all_dns_resolver_ipv4_by_domain_as_json(domain)
        )
        response = []
        print("Function:get_host_infomations_by_domain \n")
        for ip_address in all_dns_resolvers_json:
            print("Scan for IP ADDRESS: ", ip_address["ipv4"])
            scanner = NmapService.execute_port_scan(
                ip_address["ipv4"], domain, top_ports
            )
            if not scanner:
                return JsonResponse(
                    {
                        "error": f"An error occurred when trying to execute the port scan for the ip {ip_address['ipv4']}"
                    },
                    safe=False,
                )
            else:
                idScan = scanner["id"]
                response.append(PortScannerService.get_port_scanner_by_id(idScan))

        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({"Error": "You have to deliver a domain name"}, status=400)


@api_view(["POST"])
def get_host_infomations_by_ip(request):

    if "ip" in request.data and request.data["ip"]:
        ip = request.data["ip"]

        # Enable user-defined port range for the scan
        if "top_ports" in request.data:

            if (
                request.data["top_ports"]
                and request.data["top_ports"] > 0
                and request.data["top_ports"] < 65535
            ):
                top_ports = request.data["top_ports"]
            else:
                return JsonResponse({"Error": "The Top Port  is not valid"}, status=400)
        else:
            top_ports = None
        try:
            # we should validate that is a valid ip address
            ipaddress.ip_address(ip)
            print("IP: ", ip)
            scan = NmapService.execute_port_scan(ip, "", top_ports)
            if scan:
                idScan = scan["id"]
                response = PortScannerService.get_port_scanner_by_id(idScan)
                return JsonResponse(response, safe=False)
            else:
                return JsonResponse(
                    {
                        "error": f"An error occurred when trying to execute the port scan for the ip {ip}"
                    },
                    safe=False,
                )

        except ValueError:
            # this error is thrown when the ip address is not valid
            return JsonResponse({"Error": "The IP address is not valid"}, status=400)

    else:
        return JsonResponse({"Error": "You have to deliver an IP address"}, status=400)


@api_view(["POST"])
def collect_ipv4_ipv6_mail_server(request):
    if "domain" in request.data and request.data["domain"]:
        domain = request.data["domain"]
        is_information_collected = (
            DnsService.execute_collect_ipv4_ipv6_mail_server_by_domain(domain)
        )

        if is_information_collected:
            ipv4_addresses = DnsService.get_all_dns_resolver_ipv4_by_domain_as_json(
                domain
            )
            ipv6_adresses = DnsService.get_all_dns_resolver_ipv6_by_domain_as_json(
                domain
            )
            mail_server = DnsService.get_all_mail_server_by_domain_as_json(domain)
            response = {
                "data": {
                    "IPv4": ipv4_addresses,
                    "IPv6": ipv6_adresses,
                    "MailServer": mail_server,
                }
            }

            return JsonResponse(
                response,
                safe=False,
            )
        else:
            return JsonResponse(
                {"Error": f"IPv4 not found for host {domain}"}, safe=False, status=404
            )
    else:
        return JsonResponse({"Error": "You have to deliver a domain name"}, status=400)


@api_view(["GET"])
def convert_domain_to_ipv4(request):
    if "domain" in request.query_params and request.query_params["domain"]:
        domain = request.query_params["domain"]
        DnsService.execute_collect_ipv4_ipv6_mail_server_by_domain(domain)
        ipv4_addresses = DnsService.get_all_dns_resolver_ipv4_by_domain_as_json(domain)
        return JsonResponse({"data": ipv4_addresses}, safe=False)

    else:
        return JsonResponse({"Error": "You have to deliver a domain name"}, status=400)


@api_view(["GET"])
def convert_domain_to_ipv6(request):
    if "domain" in request.query_params and request.query_params["domain"]:
        domain = request.query_params["domain"]
        # to ensure that we have the data
        DnsService.execute_collect_ipv4_ipv6_mail_server_by_domain(domain)
        ipv6_addresses = DnsService.get_all_dns_resolver_ipv6_by_domain_as_json(domain)
        return JsonResponse({"data": ipv6_addresses}, safe=False)

    else:
        return JsonResponse({"Error": "You have to deliver a domain name"}, status=400)


from drf_yasg.utils import swagger_auto_schema


# @swagger_auto_schema(
#         responses={200: MailServerSerializer(many=True)}
# )

@api_view(["GET"])
def convert_domain_to_mail_server(request):
    if "domain" in request.query_params and request.query_params["domain"]:
        domain = request.query_params["domain"]
        DnsService.execute_collect_ipv4_ipv6_mail_server_by_domain(domain)
        mail_servers = DnsService.get_all_mail_server_by_domain_as_json(domain)
        return JsonResponse({"data": mail_servers}, safe=False)

@api_view(["GET"])
def get_repport(request,id):
    filename = PortScannerReportService.get_report_by_id(id)
    pdf_url = request.build_absolute_uri(settings.MEDIA_URL + filename)
    return Response({'pdf_url': pdf_url})

@api_view(["GET"])
def get_technologies(request):
    if "url" not in request.data:
        return JsonResponse({"error":"Invalid request"}, status=400)
    try:
        response = NmapService.get_technologies(request.data["url"])
        return JsonResponse(response, safe=False)
    except:
        return JsonResponse({"error":"Error fetching technologies"}, status=400)

@csrf_exempt
@api_view(['POST'])
def extract_robots_txt(request):
    if "url" not in request.data:
        return JsonResponse({"error":"Invalid request"}, status=400)
    url = request.data["url"]
    try:
        ans = NmapService.extract_robots_txt(url)
        return JsonResponse({"robots_content":ans}, safe=False)
    except Exception as e:
        return JsonResponse({"error":"Error fetching robots.txt content"}, status=400)
     