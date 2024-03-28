import re
import subprocess
from ..models import DnsResolverIpv4, DnsResolverIpv6, MailServer
from application import logger


class DnsService:
    @staticmethod
    def execute_collect_ipv4_ipv6_mail_server_by_domain(domain):
        try:
            logger.info(f"Executing DNS resolution for domain: {domain}")
            # get the ipv4 addresses and mail servers
            command = f"host  {domain}"
            execution = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            result = execution.stdout
            not_found_pattern = r" not found"
            if re.search(not_found_pattern, result):
                logger.warning(f"Domain '{domain}' not found")
                return False

            ipv4_addresses = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", result)
            # Extract mail servers with priority
            mail_servers_with_priority = re.findall(
                r" mail is handled by (\d+) (.+)", result
            )

            # delete the old records
            DnsResolverIpv4.objects.filter(host=domain).delete()
            for ipv4 in ipv4_addresses:
                DnsResolverIpv4.objects.create(host=domain, ipv4=ipv4)

            MailServer.objects.filter(host=domain).delete()
            for mailServer in mail_servers_with_priority:
                MailServer.objects.create(
                    host=domain, server=mailServer[1][:-1], priority=mailServer[0]
                )

            # get the ipv6 addresses
            command = f"host -t AAAA  {domain}"
            execution = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            result = execution.stdout
            ipv6_addresses_pattern = r"has IPv6 address (.+)\n"

            ipv6_addresses = re.findall(ipv6_addresses_pattern, result)
            # delete the old records
            DnsResolverIpv6.objects.filter(host=domain).delete()
            for ipv6 in ipv6_addresses:
                DnsResolverIpv6.objects.create(host=domain, ipv6=ipv6)

            logger.info(f"DNS resolution successful for domain: {domain}")
            return True
        except:
            logger.error(
                f"Error occurred during DNS resolution for domain '{domain}': {e}"
            )
            return False

    @staticmethod
    def get_all_dns_resolver_ipv4_by_domain_as_json(domain):
        try:
            logger.info(f"Retrieving IPv4 addresses for domain: {domain}")
            ip_addresses = DnsResolverIpv4.objects.filter(host=domain)
            ip_address_list = [
                {"id": obj.id, "host": obj.host, "ipv4": obj.ipv4}
                for obj in ip_addresses
            ]

            logger.info(
                f"Retrieved {len(ip_address_list)} IPv4 addresses for domain: {domain}"
            )
            return ip_address_list
        except Exception as e:
            logger.error(
                f"Error occurred while retrieving IPv4 addresses for domain '{domain}': {e}"
            )
            return []

    @staticmethod
    def get_all_dns_resolver_ipv6_by_domain_as_json(domain):
        try:
            logger.info(f"Retrieving IPv6 addresses for domain: {domain}")
            ip_addresses = DnsResolverIpv6.objects.filter(host=domain)
            ip_address_list = [
                {"id": obj.id, "host": obj.host, "ipv6": obj.ipv6}
                for obj in ip_addresses
            ]
            logger.info(
                f"Retrieved {len(ip_address_list)} IPv6 addresses for domain: {domain}"
            )
            return ip_address_list
        except Exception as e:
            logger.error(
                f"Error occurred while retrieving IPv6 addresses for domain '{domain}': {e}"
            )
            return []

    @staticmethod
    def get_all_mail_server_by_domain_as_json(domain):
        try:
            logger.info(f"Retrieving mail servers for domain: {domain}")
            mail_servers = MailServer.objects.filter(host=domain)
            mail_servers_list = [
                {
                    "id": obj.id,
                    "host": obj.host,
                    "mail-server": obj.server,
                    "priority": obj.priority,
                }
                for obj in mail_servers
            ]
            logger.info(f"Retrieved {len(mail_servers_list)} mail servers for domain: {domain}")
            return mail_servers_list
        except Exception as e:
            logger.error(f"Error occurred while retrieving mail servers for domain '{domain}': {e}")
            return []