import json
import time
import requests
from zapv2 import ZAPv2
from application import logger
from dotenv import load_dotenv
import os

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
        
        OwaspZapScan.spider(target)
        logger.info(f"Active Scanning target {target}")
        scanID = OwaspZapScan.zap.ascan.scan(target)
        logger.info(f"Scan ID: {scanID}")
        while int(OwaspZapScan.zap.ascan.status(scanID)) < 100:
            # Loop until the scanner has finished
            print('Scan progress %: {}'.format(OwaspZapScan.zap.ascan.status(scanID)))
            time.sleep(5)
        logger.info('Active Scan completed')
        # Print vulnerabilities found by the scanning
        print('Hosts: {}'.format(', '.join(OwaspZapScan.zap.core.hosts)))

        
        
        alerts = OwaspZapScan.zap.core.alerts(baseurl=target)
        report_json = OwaspZapScan.zap.core.jsonreport(apikey=api_key)
        report_html = OwaspZapScan.zap.core.htmlreport(apikey=api_key)

        with open("zap_passive_scan_report.json", "w") as report_file:
            report_file.write(report_json)
        
        with open("zap_passive_scan_report.html", "w") as report_file:
            report_file.write(report_html)
        with open("zap_passive_scan_reportRapport.json", "w") as file:
            json.dump(alerts, file,indent=4)



# TODO: 
# 1. Add a method to generate an owasp report
# 2. Extract alerts information and saved it dbase
# 3. Add boot function to launch owasp docker container to create logs folder, owasp report folder also
# 4. Add env varibales as apiKey
