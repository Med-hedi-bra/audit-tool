import logging
import os
from django.conf import settings
# Get an instance of a logger
logger = logging.getLogger(__name__)

 
def create_reports_directory():
    current_directory = os.getcwd()
    owasp_report_directory = current_directory + "/reports/owasp"
    skipfish_report_directory = current_directory + "/reports/skipfish"
    
    if not os.path.exists(current_directory + "/reports"):
        os.makedirs(current_directory + "/reports")
        logger.info("Reports directory created successfully")
    if not os.path.exists(owasp_report_directory):
        os.makedirs(owasp_report_directory)
    if not os.path.exists(skipfish_report_directory):
        os.makedirs(skipfish_report_directory)
 
create_reports_directory()   