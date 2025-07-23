
import time, socketio, json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework import status
from asgiref.sync import sync_to_async
from brigantes.asgi import mqtt, sio, rds
from brigantes.utils import async_fetch


@sio.event
async def my_message(data, sid=None):
    await sio.emit('message', data, to='anonymous' if sid is None else sid)



# @login_required
async def frontend(request):
    template_name = 'index.html'
    
    return render(request, template_name, {})


@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'token': token}, status=status.HTTP_200_OK)


async def test(request):
    user = await sync_to_async(lambda: request.user.email)()
    print(f"Is authenticated: {user}")
    print(request.session.get('sio_sid', 'No SID found'), 'no')
    await my_message({'msg': 'Welcome to the dashboard!'}, sid=request.session.get('sio_sid', None))
    return JsonResponse({'user': user})

    
    

