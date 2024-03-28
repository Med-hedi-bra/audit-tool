from io import StringIO
import subprocess
import re
from urllib.parse import urljoin
import requests
from ..serializers import (
    PortScannerSerializer,
)
from .PortScannerService import PortScannerService
from application import logger
import webtech

DEFAULT_TOP_PORTS_SCAN = 1000


class NmapService:

    @staticmethod
    def extract_os_version(nmap_output):
        pattern_os_version = r"Aggressive OS guesses: (.+?)\n"
        pattern_os_version_2 = r"OS details: (.+?)\n"
        match_os_version = re.findall(pattern_os_version, nmap_output, re.DOTALL)
        if match_os_version:
            os_version = match_os_version[0].split(",")[0] if match_os_version else ""
        else:
            match_os_version = re.findall(pattern_os_version_2, nmap_output, re.DOTALL)
            os_version = (
                match_os_version[0].split(":")[1].strip() if match_os_version else ""
            )
        return os_version

    @staticmethod
    def extract_mac_addresse(nmap_output):
        pattern_mac = r"MAC Address: (.+?)\n"
        match_mac = re.findall(pattern_mac, nmap_output, re.DOTALL)
        if match_mac:
            temp = match_mac[0].split(" ")[0]
            mac = temp
        else:
            mac = ""
        return mac

    @staticmethod
    def extract_ports_info(nmap_output):
        res = []
        matching_lines = []
        pattern = r"^\d+/tcp.+"
        lines = nmap_output.split("\n")
        for line in lines:
            if re.match(pattern, line):
                matching_lines.append(line.strip())
        for line in matching_lines:
            temp = re.sub(r"\s+", " ", line).split(" ")
            port = temp[0].split("/")[0]
            protcol = temp[0].split("/")[1]
            state = temp[1]
            service = temp[2]
            service_version = " ".join(temp[3:]) if len(temp) > 3 else ""
            res.append(
                {
                    "port": port,
                    "protocol": protcol,
                    "state": state,
                    "service": service,
                    "service_version": service_version,
                }
            )
        return res

    @staticmethod
    def extract_uptime(nmap_output):
        pattern_uptime = r"Uptime guess: (.+?) days.*\n"
        match_uptime = re.findall(pattern_uptime, nmap_output, re.DOTALL)
        uptime = match_uptime[0] if match_uptime else ""
        uptime = "".join(uptime.split("."))
        # uptime = int(uptime)
        return uptime

    @staticmethod
    def extract_network_distance(nmap_output):
        pattern_network_distance = r"Network Distance: (.+?) hops.*\n"
        match_network_distance = re.findall(
            pattern_network_distance, nmap_output, re.DOTALL
        )
        network_distance = (
            match_network_distance[0].strip() if match_network_distance else ""
        )
        # network_distance = int(network_distance)
        return network_distance


    @staticmethod
    def execute_port_scan(ip, domain, top_ports):
        try:
            if top_ports is None:
                command = f"sudo nmap -sV -O -v --port-ratio 0.03 {ip}"
            else:
                command = f"sudo nmap -sV -O -v --top-port {top_ports} {ip}"

            logger.info(f"Executing port scan for IP: {ip}, Domain: {domain}, Top ports: {top_ports}")
            execution = subprocess.run(command, shell=True, capture_output=True, text=True)
            result = execution.stdout

            ports_info = NmapService.extract_ports_info(result)
            mac = NmapService.extract_mac_addresse(result)
            os_version = NmapService.extract_os_version(result)
            uptime = NmapService.extract_uptime(result)
            network_distance = NmapService.extract_network_distance(result)

            scanner = PortScannerService.create_port_scanner(
                ip=ip,
                domain=domain,
                os_version=os_version,
                mac_address=mac,
                port_info=ports_info,
                uptime_in_days=uptime,
                network_distance_in_hops=network_distance,
            )
            serialized_data = PortScannerSerializer(scanner).data
            logger.info(f"Port scan completed successfully for IP: {ip}, Domain: {domain}, Top ports: {top_ports}")
            return serialized_data
        except Exception as e:
            logger.error(f"Error occurred during port scan for IP: {ip}, Domain: {domain}, Top ports: {top_ports}: {e}")
            return False
    @staticmethod
    def get_technologies(target):
        try:
            logger.info(f"Retrieving technologies for URL: {target}")
            wt = webtech.WebTech(options={'json': True})
            report = wt.start_from_url(target)
            logger.info("Technologies retrieved successfully")
            return report
        except webtech.utils.ConnectionException as e:
            logger.error(f"Connection error occurred while retrieving technologies for URL: {url}: {e}")
            raise e
    @staticmethod
    def extract_robots_txt(url):
        try:
            logger.info(f"Extracting robots.txt for URL: {url}")
            
            robots_url = urljoin(url, "/robots.txt")
            response = requests.get(robots_url)
            response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
            
            robots_content = StringIO(response.text)
            routes = []
            for line in robots_content:
                line = line.strip()
                if line and not line.startswith('#'):
                    routes.append(line)

            logger.info("Robots.txt extracted successfully")
            return routes
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while extracting robots.txt for URL: {url}: {e}")
            raise e