from django.http import JsonResponse
from rest_framework.decorators import api_view
from testing_auth.services.AuthTestingService import AuthTestingService


# Create your views here.

@api_view(['POST'])
def verify_password_strength(request):
    credantials = request.data["credentials"]
    print(credantials)
    response = []
    for cred in credantials:
        ans = AuthTestingService.verify_password_strength(cred["password"])
        response.append({"username":cred["username"],"password_strength":ans})
        

    return JsonResponse(response, safe=False)