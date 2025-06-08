
import time
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token





# Create your views here.
# @login_required
def frontend(request):
    template_name = 'index.html'

    context = {}

    return render(request, template_name, context)


@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'status_code': 200, 'token': token})

