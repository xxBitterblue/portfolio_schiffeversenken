from game.CustomErrors.GameLaunchError import GameLaunchError


class Game:
    def __init__(self, id):
        self.id = id
        self.player = {}
        self.current_attacker = None
        self.game_ready = False

    def set_player(self, player_id):
        if self.game_ready:
            raise GameLaunchError("Already enough player")
        elif player_id in self.player.keys():
            raise GameLaunchError("Already in game")
        else:
            self.player[player_id] = None
            if len(self.player.keys()) == 2:
                self.game_ready = True

    def __str__(self):
        dict_as_list = [f"key: {key} val: {str(val)}" for key, val in self.player.items()]
        return f'id: {self.id} player: {dict_as_list}'


class Board:
    def __init__(self, id, all_ships):
        self.id = id
        self.all_ships = all_ships
        self.life = sum([ship.life_points for ship in all_ships])

    def __str__(self):
        return f'id: {self.id} ships: ' + "".join(str(e) for e in self.all_ships)


class Ship:
    def __init__(self, id, x, y, alignment, size, life_points):
        self.id = id
        self.x = x
        self.y = y
        self.alignment = alignment
        self.size = size
        self.life_points = life_points
        self.max_life = life_points
        self.size_factor = 40

    def calculate_bounding_box(self):
        bounding_box = [(self.x, self.y)]
        if self.alignment == "horizontal":
            x_top_right = self.x + (self.size * self.size_factor)
            y_bottom_left = self.y + self.size_factor
            bounding_box.append((x_top_right, self.y))
            bounding_box.append((self.x, y_bottom_left))
            bounding_box.append((x_top_right, y_bottom_left))
        else:
            y_bottom_left = self.y + (self.size * self.size_factor)
            x_top_right = self.x + self.size_factor
            bounding_box.append((x_top_right, self.y))
            bounding_box.append((self.x, y_bottom_left))
            bounding_box.append((x_top_right, y_bottom_left))
        return bounding_box

    def __str__(self):
        return f'id: {self.id} x: {self.x} y: {self.y}'
