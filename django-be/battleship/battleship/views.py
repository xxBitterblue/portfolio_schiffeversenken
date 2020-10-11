import json

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    try:
        json_data = json.loads(request.body)
        username = json_data["username"]
        password = json_data["password"]

        if username is None or password is None:
            return HttpResponseBadRequest('')

        user = authenticate(username=username, password=password)

        if not user:
            return HttpResponseNotFound('')

        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key, 'user_id': user.id})
    except KeyError:
        return HttpResponseBadRequest('')


@csrf_exempt
def register(request):
    try:
        json_data = json.loads(request.body)
        username = json_data["username"]
        password = json_data["password"]

        if username is None or password is None:
            return HttpResponseBadRequest('')

        user = User.objects.create_user(username=username,
                                        email=username,
                                        password=password)
        user.save()
        return HttpResponse("")
    except KeyError:
        return HttpResponseBadRequest('')
