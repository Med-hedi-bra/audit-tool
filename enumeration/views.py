from django.conf import settings
from django.http import JsonResponse
from requests import Response
from rest_framework.decorators import api_view
from enumeration.services.auth_testing_service import AuthTestingService
from rest_framework.decorators import api_view
import json
from django.views.decorators.csrf import csrf_exempt
from .services.owasp_zap_scan_service import OwaspZapScan
from .services.owasp_zap_scan_crud import OwaspZapScanCrud

# Create your views here. 




@api_view(["GET"])
def get_owasp_report(request, id):
    filename = OwaspZapScan.get_report_filename_by_id(id)
    zap_report_url = request.build_absolute_uri(settings.ZAP_REPORTS_URL + filename)
    return JsonResponse({'pdf_url': zap_report_url})

@api_view(["GET"])
def owasp_spider(request):
    if "target" not in request.query_params:
        return JsonResponse({"error": "Invalid request"}, status=400)
    target = request.query_params["target"]
    OwaspZapScan.spider(target)
    return JsonResponse({"message": "This is the OWASP spider endpoint"}, status=200)


@api_view(["GET"])
def owasp_scan(request):
    if "target" not in request.query_params:
        return JsonResponse({"error": "Invalid request"}, status=400)
    target = request.query_params["target"]
    response = OwaspZapScan.active_scan(target)
    return JsonResponse({"data":response}, status=200)


@api_view(["POST"])
def verify_username_and_password_strength(request):
    if "credentials" not in request.data:
        return JsonResponse({"error": "Invalid request"}, status=400)
    credantials = request.data["credentials"]
    response = []
    for cred in credantials:
        password_validation = AuthTestingService.verify_password_strength(
            cred["password"]
        )
        username_validation = AuthTestingService.verify_username_strength(
            cred["username"]
        )
        response.append(
            {
                "username": cred["username"],
                "validations": {
                    "username_validation": username_validation,
                    "password_strength": password_validation,
                },
            }
        )
    return JsonResponse(response, safe=False)


@csrf_exempt
@api_view(["POST"])
def check_role_authorization(request):
    # Get the JSON data from the request body
    json_data = json.loads(request.body)

    # Extract information from the JSON
    all_roles = json_data.get("roles")
    services = json_data.get("services")
    auth_uri = json_data.get("auth_uri")
    token_path = json_data.get("token_path_in_response")
    website_url = json_data.get("website_url")

    response = AuthTestingService.check_role_authorization(
        website_url=website_url,
        all_roles=all_roles,
        services=services,
        auth_uri=auth_uri,
        token_path=token_path,
    )
    return JsonResponse(response, safe=False)
