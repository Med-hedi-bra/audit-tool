import json
import time
import requests
from zapv2 import ZAPv2



# target = "https://juice-shop.herokuapp.com"



class OwaspZapScan:
    #use .env
    apiKey = "mohamed"
    zap = ZAPv2(
    apikey=apiKey,
    proxies={"http": "http://127.0.0.1:8091", "https": "http://127.0.0.1:8091"},
)
    

    @staticmethod
    def spider(target):

        print("Spidering target {}".format(target))

        scanID = OwaspZapScan.zap.spider.scan(target)

        while int(OwaspZapScan.zap.spider.status(scanID)) < 100:
            print("Spider progress %: {}".format(OwaspZapScan.zap.spider.status(scanID)))
            time.sleep(1)

        print("Spider has completed!")
        return scanID
    
    
    @staticmethod
    def testing(target):

        # TODO : explore the app (Spider, etc) before using the Active Scan API, Refer the explore section
        print('Active Scanning target {}'.format(target))
        scanID = OwaspZapScan.zap.ascan.scan(target)
        print('Scan ID: {}'.format(scanID))
        while int(OwaspZapScan.zap.ascan.status(scanID)) < 100:
            # Loop until the scanner has finished
            print('Scan progress %: {}'.format(OwaspZapScan.zap.ascan.status(scanID)))
            time.sleep(5)

        print('Active Scan completed')
        # Print vulnerabilities found by the scanning
        print('Hosts: {}'.format(', '.join(OwaspZapScan.zap.core.hosts)))
        print('Alerts: ')
        print(OwaspZapScan.zap.core.alerts(baseurl=target))
        
        
        
        report_json = OwaspZapScan.zap.core.jsonreport(apikey=OwaspZapScan.apiKey)
        report_html = OwaspZapScan.zap.core.htmlreport(apikey=OwaspZapScan.apiKey)

        with open("zap_passive_scan_report.json", "w") as report_file:
            report_file.write(report_json)
        
        with open("zap_passive_scan_report.html", "w") as report_file:
            report_file.write(report_html)

