import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_backends
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from brigantes.exceptions import http_exception

# Create your views here.

def user_login(request):
    data = json.loads(request.body)

    email = data.get('email')
    password = data.get('password')
    if not (email and password):
        return JsonResponse({"status_code": 400, "error":"Email and Password must be supplied."})
    
    user = authenticate(request, username=email, password=password)
    if not user:
        return JsonResponse({"status_code": 400, "error": "Invalid authentication credetials."})

    auth = login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    obj_dict = user.as_dict()
    return JsonResponse({
        "status_code": 200,
        "data": {
            "user": obj_dict,
            "is_authenticated": request.user.is_authenticated,  
        }})

