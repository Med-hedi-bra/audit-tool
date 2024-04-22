import json
import time
from django.conf import settings
import requests
from zapv2 import ZAPv2
from application import logger
from dotenv import load_dotenv
import os
from .owasp_zap_scan_crud import OwaspZapScanCrud

load_dotenv()
api_key = os.getenv("ZAP_DOCKER_API_KEY")
http_proxy = os.getenv("ZAP_HTTP_PROXY")
https_proxy = os.getenv("ZAP_HTTPS_PROXY")

class OwaspZapScan:
    zap = ZAPv2(
    apikey=api_key,
    proxies={"http": http_proxy, "https": https_proxy},
)
    

    @staticmethod
    def spider(target):
        
        logger.info(f"Spidering target {target}")
        scanID = OwaspZapScan.zap.spider.scan(target)
        while int(OwaspZapScan.zap.spider.status(scanID)) < 100:
            print("Spider progress %: {}".format(OwaspZapScan.zap.spider.status(scanID)))
            time.sleep(1)
        logger.info("Spider has completed!")
        print("Spider has completed!")

    
    
    @staticmethod
    def active_scan(target):
        # In this code scanID is refered to the scan in the zap container, and zapScan is the scan in the database
        OwaspZapScan.spider(target)
        logger.info(f"Active Scanning target {target}")
        scanID = OwaspZapScan.zap.ascan.scan(target)
        zapScan = OwaspZapScanCrud.create_zap_scan(target)
        logger.info(f"Scan ID: {scanID}")
        
        
        while int(OwaspZapScan.zap.ascan.status(scanID)) < 100:
            # Loop until the scanner has finished
            print('Scan progress %: {}'.format(OwaspZapScan.zap.ascan.status(scanID)))
            zapScan = OwaspZapScanCrud.update_zap_scan_progress(zapScan["id"], OwaspZapScan.zap.ascan.status(scanID))
            time.sleep(5)
        logger.info('Active Scan completed')
        print('Hosts: {}'.format(', '.join(OwaspZapScan.zap.core.hosts)))

         
        
        
        report_html = OwaspZapScan.zap.core.htmlreport(apikey=api_key)
        
      
        # alerts = OwaspZapScan.zap.core.alerts(baseurl=target)
        # report_json = OwaspZapScan.zap.core.jsonreport(apikey=api_key)
        # with open("zap_passive_scan_report.json", "w") as report_file:
        #     report_file.write(report_json)
        
        # with open("zap_passive_scan_report.html", "w") as report_file:
        #     report_file.write(report_html)
        # with open("zap_passive_scan_reportRapport.json", "w") as file:
        #     json.dump(alerts, file,indent=4)
            
        owasp_report_directory = settings.ZAP_REPORTS_ROOT
        with open(owasp_report_directory + f"/zap_active_scan_report{zapScan['id']}.html", "w") as report_file:
            report_file.write(report_html)
        
        OwaspZapScanCrud.set_zap_scan_report(zapScan["id"], f"zap_active_scan_report{zapScan['id']}.html")



# TODO: 
# 1. Add a method to generate an owasp report
# 3. Add boot function to launch owasp docker container 
# 4. Add a method to stop the owasp docker container when the project is stoped