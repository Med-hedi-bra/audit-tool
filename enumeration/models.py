from django.db import models

# Create your models here.

# class Scanner(models.Model):
#     id = models.AutoField(primary_key=True)
#     id_user = models.IntegerField(default=0)
#     id_port_scanner = models.IntegerField(default=0)
#     target = models.TextField()
#     zap_scanner = models.OneToOneField('ZapScan', on_delete=models.CASCADE, null=True)

    
#     def __str__(self):
#         return f"ID: {self.id}  | Created_at: {self.created_at} | Domain: {self.domain} | IP: {self.ip} | OS Version: {self.os_version} | MAC Address: {self.mac_address} | UserID: {self.idUser} | Uptime in days: {self.uptime_in_days} | Network Distance in hops: {self.network_distance_in_hops}"



class ZapScan(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    target = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, null=True)  
    def __str__(self):
        return f'{self.id} | {self.file_name} | {self.progress} | {self.created_at}'
    
    
