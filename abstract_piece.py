from constants import Colour, Letter
from coordinate import Coordinate


class Piece:
    def __init__(self, colour, piece_type, location, game_pieces, game_tiles):
        self.game_pieces = game_pieces
        self.game_tiles = game_tiles
        self.colour = colour
        self.type = piece_type
        self.location = location
        self.new_location = ""
        self.enemy_colour = Colour.get_opposite(colour)
        self.enemy_king_location = get_king(game_pieces, self.enemy_colour)
        self.legal_moves = set()
        self.attack_moves = set()

    def __str__(self):
        return f"{self.colour} {self.type} at {self.location}"

    def move_to(self, new_location: str):
        """moves piece to new location"""
        self.remove()
        self.game_pieces[new_location] = self
        self.location = new_location
        self.unmoved = False

    def remove(self):
        """removes piece from game pieces"""
        del self.game_pieces[self.location]

    def find_direction(self):
        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        v1, v2 = movement(self.new_location, self.location)
        if 0 in (v1, v2) or abs(v1) == abs(v2):
            return sign(v1), sign(v2)
        else:
            return "invalid"

    def is_move_blocked(self, new_location):
        self.new_location = new_location
        direction = self.find_direction()
        if direction != "invalid":
            location = add_coordinate(self.location, direction)
            while location != new_location:
                if location in self.game_pieces.keys():
                    return True
                location = add_coordinate(location, direction)
            return False

    def is_attack_valid(self, m1, m2, location):
        pass

    def get_attacks(self):
        am = self.attack_moves
        piece_location = self.location

        am.clear()
        for location in self.game_tiles.keys():
            m1, m2 = movement(location, piece_location)
            if self.is_attack_valid(m1, m2, location):
                am.add(location)
        if piece_location in am:
            am.remove(piece_location)


def movement(location1: str, location2: str) -> tuple:
    c1 = Coordinate.create_from_str(location1)
    c2 = Coordinate.create_from_str(location2)
    return Coordinate.diff_vector(c1, c2)


def add_coordinate(start: str, vector: tuple) -> str:
    x0, y0 = Letter.to_num(start[0]), int(start[1])
    x1 = x0 + vector[0]
    y1 = y0 + vector[1]
    return f"{Letter.num_to_lower(x1)}{y1}"


def get_king(game_pieces: dict, colour) -> str:
    for piece in game_pieces.values():
        if piece.type == "king" and piece.colour == colour:
            return piece.location


def get_attacked_positions(pieces: dict, attacked_by: str = "white", skip="") -> set:
    res = set()
    for piece in pieces.values():
        if piece.location == skip:
            continue
        piece.get_attacks()
        for move in piece.attack_moves:
            if attacked_by == "white" and piece.colour == "white":
                res.add(move)
            elif attacked_by == "black" and piece.colour == "black":
                res.add(move)
    return res
