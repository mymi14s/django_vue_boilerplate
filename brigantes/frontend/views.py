
import time, socketio, json, asyncio
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from asgiref.sync import sync_to_async, async_to_sync
from studio_web_manager.asgi import mqtt, sio, rds
from studio_web_manager.utils import async_fetch


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



@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    user = request.user.email
    sio_sid = request.session.get('sio_sid', None)
    async_to_sync(my_message)({'msg': 'Welcome to the dashboard!'}, sid=sio_sid)

    return JsonResponse({'user': user})
