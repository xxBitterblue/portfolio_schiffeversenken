from game.CustomErrors.GameError import GameError
from game.CustomErrors.GameOrPlayerNotFoundError import GameOrPlayerNotFoundError
from .models import Ship, Game, Board
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import numpy as np
from numpy.linalg import norm
import math


class GameService:
    def __init__(self):
        self.all_games = {}
        self.layer = get_channel_layer()

    def launch_game(self, game_id, player_id):
        """Launchs game with a given game_id and adds a player to the game."""
        if game_id not in self.all_games.keys():
            self.all_games[game_id] = Game(game_id)

        curr_game = self.all_games[game_id]
        curr_game.set_player(player_id)

        if curr_game.game_ready:
            content = {
                "game_ready": True,
                "game_id": curr_game.id
            }
            self.send_socket_msg(game_id, 'launch_game', content)

        socket_name = "/game/" + str(curr_game.id) + "/"
        return socket_name, curr_game.game_ready, curr_game.id

    def start_game(self, game_id, player_id, all_ships):
        """Adds the ships of a player to a given game.
        Sends a 'game_started' socket msg when all players have started the game."""
        try:
            curr_game = self.all_games[game_id]
            new_board = Board(str(player_id) + "_board", all_ships)
            curr_game.player[player_id] = new_board
        except KeyError:
            raise GameOrPlayerNotFoundError(f"Game with id: { game_id } or player with id: { player_id } not found.")

        if None in self.all_games[game_id].player.values():
            return False
        else:
            curr_game.current_attacker = player_id
            content = {
                'start_game': True,
                'all_player': [{"id": key, "life_points": val.life} for key, val in curr_game.player.items()],
                'start_player': player_id
            }
            self.send_socket_msg(game_id, 'start_game', content)
            return True

    def attack(self, game_id, attacker_player_id, attacked_player_id, coordinates):
        """Evaluates the attack from a player to another and calculates potential damage done to all ships."""
        attacked_ships = []
        try:
            curr_game = self.all_games[game_id]
            attacked_board = curr_game.player[attacked_player_id]
        except KeyError:
            raise GameOrPlayerNotFoundError(f"Game with id: { game_id } or player with id: { attacked_player_id } not found.")

        if curr_game.current_attacker is not attacker_player_id:
            raise GameError("Its not your turn.")

        for ship in attacked_board.all_ships:
            if ship.life_points > 0:
                damage = self.calculate_damage(ship, coordinates["x"], coordinates["y"])
                if damage > 0:
                    if ship.life_points - damage <= 0:
                        damage = ship.life_points

                    ship.life_points -= damage
                    attacked_board.life -= damage
                    attacked_ships.append(ship)

        curr_game.current_attacker = attacked_player_id

        content = {
            'attacker_player_id': attacker_player_id,
            'attacked_player_id': attacked_player_id,
            'total_hits': len(attacked_ships),
            'affected_ships': [ship.__dict__ for ship in attacked_ships]
        }
        self.send_socket_msg(curr_game.id, 'attack_evaluation', content)

        if len(attacked_ships) > 0:
            content = {
                'affected_player_id': attacked_player_id,
                'new_life_points': attacked_board.life
            }
            self.send_socket_msg(curr_game.id, 'score_changed', content)

        if attacked_board.life == 0:
            self.send_socket_msg(curr_game.id, 'game_finished', {'winner_player_id': attacker_player_id})

    def send_socket_msg(self, game_id, event_type, content):
        """Basic method that sends a socket msg for a game with given event and content."""
        async_to_sync(self.layer.group_send)(f'game_{game_id}', {
            'type': event_type,
            'content': content
        })

    def calculate_damage(self, ship, x, y):
        """Calculates the damage that is done to a ship."""
        ship_bounding_box = ship.calculate_bounding_box()
        ship_life_proportion = ship.max_life / ship.size

        # would be direct hit
        if (x >= ship_bounding_box[0][0] and y >= ship_bounding_box[0][1]) and (x <= ship_bounding_box[3][0] and y <= ship_bounding_box[3][1]):
            return math.ceil(ship_life_proportion * 0.5)

        distance = math.ceil(self.calculate_distances(ship_bounding_box, x, y))
        damage = math.ceil(((ship.size_factor * 1.5) - distance)/2) if (distance <= ship.size_factor * 1.5) else 0
        return damage

    def calculate_distances(self, bounding_box, x, y):
        """Calculates the distance of a ship represented as bounding box and x,y coordinates."""
        bounding_box_numpy = [np.array(box) for box in bounding_box]
        hit_point = np.array([x, y])
        distance = [
            norm(np.cross(bounding_box_numpy[0] - bounding_box_numpy[1], bounding_box_numpy[1] - hit_point)) / norm(bounding_box_numpy[0] - bounding_box_numpy[1]),
            norm(np.cross(bounding_box_numpy[0] - bounding_box_numpy[2], bounding_box_numpy[2] - hit_point)) / norm(bounding_box_numpy[0] - bounding_box_numpy[2]),
            norm(np.cross(bounding_box_numpy[1] - bounding_box_numpy[3], bounding_box_numpy[3] - hit_point)) / norm(bounding_box_numpy[1] - bounding_box_numpy[3]),
            norm(np.cross(bounding_box_numpy[2] - bounding_box_numpy[3], bounding_box_numpy[3] - hit_point)) / norm(bounding_box_numpy[2] - bounding_box_numpy[3])
        ]

        rect_x_max = max([x[0] for x in bounding_box])
        rect_x_min = min([x[0] for x in bounding_box])

        rect_y_max = max([y[1] for y in bounding_box])
        rect_y_min = min([y[1] for y in bounding_box])

        dx = max(rect_x_min - x, 0, x - rect_x_max) # max(a,b,c)
        dy = max(rect_y_min - y, 0, y - rect_y_max)

        distance = math.sqrt(dx*dx + dy*dy)
        return distance
