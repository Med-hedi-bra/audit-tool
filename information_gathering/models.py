from django.db import models

# Create your models here.


 

 
class PortScanner(models.Model):
    id = models.AutoField(primary_key=True)
    idUser = models.IntegerField()
    #if its a scan by domain ip will be null else the inverse
    domain = models.TextField()
    ip = models.TextField()
    os_version = models.TextField()
    mac_address = models.TextField()
    uptime_in_days = models.TextField()
    network_distance_in_hops = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    def __str__(self):
        return f"ID: {self.id}  | Created_at: {self.created_at} | Domain: {self.domain} | IP: {self.ip} | OS Version: {self.os_version} | MAC Address: {self.mac_address} | UserID: {self.idUser} | Uptime in days: {self.uptime_in_days} | Network Distance in hops: {self.network_distance_in_hops}"


class PortScannerReport(models.Model):
    port_scanner = models.OneToOneField(PortScanner,on_delete=models.DO_NOTHING,primary_key=True)
    filename = models.TextField()
    
    def __str__(self):
        return f"ID: {self.port_scanner.id} | Filename: {self.filename}"


class PortScannerLine(models.Model):
    id = models.AutoField(primary_key=True)
    port_scanner = models.ForeignKey(PortScanner, on_delete=models.CASCADE,)
    port = models.TextField()
    protocol = models.TextField()
    service = models.TextField()
    state = models.TextField()
    service_version = models.TextField()
   

    def __str__(self):
        return f"ID: {self.id} | IdScannerr:{self.port_scanner.id} | Protocol: {self.protocol} | Port: {self.port} | Service: {self.service} | Service_version: {self.service_version} | State: {self.state}"



class DnsResolverIpv4(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.TextField()
    ipv4 = models.TextField()
    
    def __str__(self):
       return f"ID: {self.id} | Host: {self.host} | IPv4: {self.ipv4}"


class DnsResolverIpv6(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.TextField()
    ipv6 = models.TextField()
    def __str__(self):
        return f"ID: {self.id} | Host: {self.host} | IPv6: {self.ipv6}"

    
    
class MailServer(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.TextField()
    server = models.TextField()
    priority = models.IntegerField()
    
    def __str__(self):
        return f"ID: {self.id} | Host: {self.host} | Server: {self.server} | Priority: {self.priority}"

    
