import json

from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from user.models import User


# Create your views here.
def user_reg(request):
    """ Function for user registraion with hash password """
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user = User.objects.create_user(**data)
            return JsonResponse({"message": "User registration Successful"})
        return JsonResponse({"message": "Wrong method"})
    except Exception as e:
        return JsonResponse({"message": e})


def user_login(request):
    """ Function for user login """
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user = authenticate(request, **data)
            if not user:
                return JsonResponse({"message": "Invalid credentials"})
            return JsonResponse({"message": "Login Successful"})
        return JsonResponse({"message": "Wrong method"})
    except Exception as e:
        return JsonResponse({"message": e})
