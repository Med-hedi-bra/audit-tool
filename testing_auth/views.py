from django.http import JsonResponse
from rest_framework.decorators import api_view
from testing_auth.services.AuthTestingService import AuthTestingService


# Create your views here.


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
                "validations":
                    {
                    "username_validation": username_validation,
                    "password_strength": password_validation,
                }
            }
        )
    return JsonResponse(response, safe=False)
