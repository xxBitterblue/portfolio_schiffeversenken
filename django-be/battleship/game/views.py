import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from game.CustomErrors.GameError import GameError
from game.CustomErrors.GameLaunchError import GameLaunchError
from game.CustomErrors.GameOrPlayerNotFoundError import GameOrPlayerNotFoundError
from .models import Ship
from .services import factory


@csrf_exempt
@api_view(['POST'])
def launch_game(request, game_id):
    player_id = request.user.id
    try:
        result = game_service.launch_game(game_id, player_id)
        return JsonResponse({
            'socket_name': result[0],
            'game_id': result[2],
            'game_ready': result[1]
        })
    except GameLaunchError as ex:
        return HttpResponseBadRequest(ex)


@csrf_exempt
@api_view(['POST'])
def start_game(request, game_id):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            player_id = request.user.id
            all_ships = [Ship(x["id"], x["x"], x["y"], x["alignment"], x["size"], x["life"]) for x in json_data['ships']]

            players_ready = game_service.start_game(game_id, player_id, all_ships)
            return JsonResponse({"allPlayersReady": players_ready, "currentUser": player_id})
    except KeyError:
        return HttpResponseBadRequest('JSON key error')
    except (GameOrPlayerNotFoundError, GameError) as ex:
        return HttpResponseBadRequest(ex)


@csrf_exempt
@api_view(['POST'])
def attack(request, game_id):
    try:
        if request.method == 'POST':
            json_data = json.loads(request.body)
            attacker_player_id = request.user.id
            attacked_player_id = json_data['attacked_player_id']
            coordinates = json_data['coordinates']

            game_service.attack(game_id, attacker_player_id, attacked_player_id, coordinates)
            return HttpResponse('')
    except KeyError:
        return HttpResponseBadRequest('JSON key error')
    except GameOrPlayerNotFoundError as ex:
        return HttpResponseBadRequest(ex)


game_service = factory.create('game_service')
