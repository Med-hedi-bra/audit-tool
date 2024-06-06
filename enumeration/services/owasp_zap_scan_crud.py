from ..models import ZapScan
from ..serializers import ZapScanSerializer

from application import logger

class OwaspZapScanCrud:
    
    @staticmethod
    def create_zap_scan(target):
        logger.info(f"Creating Zap scan for target {target}")
        zap_scan = ZapScan.objects.create(target=target)    
        zap_scan_serialized = ZapScanSerializer(zap_scan).data
        return zap_scan_serialized
    
    @staticmethod
    def update_zap_scan_progress(id_zap_scan, progress):
        logger.info(f"Updating progress for Zap scan {id_zap_scan} to {progress}")
        zap_scan = ZapScan.objects.get(id=id_zap_scan)
        zap_scan.progress = progress
        zap_scan.save()
        zap_scan_serialized = ZapScanSerializer(zap_scan).data
        return zap_scan_serialized
    
    
    @staticmethod 
    def set_zap_scan_report(id_zap_scan, file_name):
        logger.info(f"Setting report for Zap scan {id_zap_scan}")
        zap_scan = ZapScan.objects.get(id=id_zap_scan)
        zap_scan.file_name = file_name
        zap_scan.save()
        zap_scan_serialized = ZapScanSerializer(zap_scan).data
        return zap_scan_serialized
        
    @staticmethod
    def get_zap_scan_by_id(id_zap_scan):
        zap_scan = ZapScan.objects.get(id=id_zap_scan)
        zap_scan_serialized = ZapScanSerializer(zap_scan).data
        return zap_scan_serialized
    