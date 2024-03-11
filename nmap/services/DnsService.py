import re
import subprocess
from..models import DnsResolverIpv4, DnsResolverIpv6, MailServer

class DnsService:
    @staticmethod
    def execute_collect_ipv4_ipv6_mail_server_by_domain(domain):
        try:
            # get the ipv4 addresses and mail servers
            command = f"host  {domain}"
            execution = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            result = execution.stdout
            not_found_pattern = r" not found"
            if re.search(not_found_pattern, result):
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

            return True
        except:
            return False

    
    @staticmethod
    def get_all_dns_resolver_ipv4_by_domain_as_json(domain):
        ip_addresses = DnsResolverIpv4.objects.filter(host=domain)
        ip_address_list = []
        for obj in ip_addresses:
            ip_address_list.append({"id": obj.id, "host": obj.host, "ipv4": obj.ipv4})
        return ip_address_list
    
    @staticmethod
    def get_all_dns_resolver_ipv6_by_domain_as_json(domain):
        ip_addresses = DnsResolverIpv6.objects.filter(host=domain)
        ip_address_list = []
        for obj in ip_addresses:
            ip_address_list.append({"id": obj.id, "host": obj.host, "ipv6": obj.ipv6})
        return ip_address_list

    @staticmethod
    def get_all_mail_server_by_domain_as_json(domain):
        mail_servers = MailServer.objects.filter(host=domain)
        mail_servers_list = []
        for obj in mail_servers:
            mail_servers_list.append(
                {
                    "id": obj.id,
                    "host": obj.host,
                    "mail-server": obj.server,
                    "priority": obj.priority,
                }
            )
        return mail_servers_list
    
    
    
    
