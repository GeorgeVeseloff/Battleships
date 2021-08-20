from random import randint

class Error(Exception):
    pass

class OutOfOceanError(Error):
    def __repr__(self):
        return 'These coordinates are not within the ocean'

class PointInUseError(Error):
    def __repr__(self):
        return 'You have already shot at this point'

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ocean:
    def __init__(self):
        self.ocean = [["~" for column in range(6)] for row in range(6)]
        self.used_points = []
        self.ships_in_ocean = []
        self.ships_afloat = 7

    def view_ocean(self):
        for row in self.ocean:
            print(" ".join(row))
        return ""

    def draw_ship(self, ship):
        for point in ship.create_points_in_ship():
            if not self.is_in_ocean(point) or point in self.used_points:
                raise PointInUseError
        ship_occupies_position = ship.create_points_in_ship()
        for point in ship_occupies_position:
            self.ocean[point.x][point.y] = "#"
            self.used_points.append(point)
        self.ships_in_ocean.append(ship)
        self.proximity_warning(ship)


    def proximity_warning(self, ship):
        # prohibited_points = list(product([-1, 0, 1], repeat = 2))
        prohibited_points = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for point in ship.create_points_in_ship():
            for x_offset, y_offset in prohibited_points:
                current_coordinates = Point(point.x + x_offset, point.y + y_offset)
                if current_coordinates not in self.used_points and self.is_in_ocean(current_coordinates):
                    self.ocean[current_coordinates.x][current_coordinates.y] = "^"
                    self.used_points.append(current_coordinates)


    def is_in_ocean(self, point):
        ocean_limits = [0, 1, 2, 3, 4, 5]
        return point.x in ocean_limits and point.y in ocean_limits

    def take_a_shot(self, point):

        if not self.is_in_ocean(point):
            raise OutOfOceanError

        if point in self.used_points:
            raise PointInUseError

        for ship in self.ships_in_ocean:
            if point in ship.create_points_in_ship():
                ship.hp -= 1
                self.used_points.append(point)
                if ship.hp == 0:
                    print('It has sunk')
                    self.proximity_warning(ship)
                    self.ocean[point.x][point.y] = "H"
                    self.ships_afloat -= 1
                    return True
                else:
                    print('It is a hit')
                    self.ocean[point.x][point.y] = "H"
                    return True

        print('You missed')
        self.ocean[point.x][point.y] = "O"
        self.used_points.append(point)
        return False

    def clear_used_point(self):
        self.used_points = []


class Ship:
    def __init__(self, anchor, hull_size, is_horizontal = True):
        self.anchor = anchor
        self.hull_size = hull_size
        self.is_horizontal = is_horizontal
        self.hp = hull_size

    def __repr__(self):
        return f"{self.create_points_in_ship()}, hull size {self.hull_size}, orientation {self.is_horizontal}"

    def create_points_in_ship(self):
        points_in_ship = []
        start_position_x = self.anchor.x
        start_position_y = self.anchor.y
        if self.is_horizontal:
            for coordinate in range(self.hull_size):
                points_in_ship.append(Point(start_position_x + coordinate, start_position_y))
        else:
            for coordinate in range(self.hull_size):
                points_in_ship.append(Point(start_position_x, start_position_y + coordinate))
        return points_in_ship

class Game:
    def __int__(self):
        player_ocean = self.random_ocean()
        computer_ocean = self.random_ocean()


    def random_ocean(self, is_visible = True):
        if is_visible:
            ocean = None
            while ocean is None:
                ocean = self.random_placement()
                return ocean
        else:
            ocean = None
            while ocean is None:
                ocean = self.random_placement(False)
                return ocean


    def random_placement(self, is_visible = True):
        hull_sizes = [3, 2, 2, 1, 1, 1, 1]
        ocean = Ocean()
        tries = 0
        for ship_size in hull_sizes:
            while True:
                tries += 1
                if tries > 100000:
                    return None
                ship = Ship(Point(randint(0, 5), randint(0, 5)), ship_size, randint(0, 1))
                try:
                    ocean.draw_ship(ship)
                    break
                except PointInUseError:
                    pass
        ocean.clear_used_point()
        if not is_visible:
            ocean.ocean = [["~" for column in range(6)] for row in range(6)]
        return ocean

    def pick_a_target(self, is_player = False):
        if not is_player:
            target = Point(randint(0, 5), randint(0, 5))
            return target
        else:
            while True:
                raw_input = input("Pick a target (two integers from 1 to 5 separated by space)").split()
                if len(raw_input) != 2:
                    print("Target has to be two integers separated by space")
                    continue
                x, y = raw_input
                if not(x.isdigit()) or not (y.isdigit()):
                    print("Target has to be integers")
                    continue
                x, y = int(x), int(y)
                allowed_range = [1, 2, 3, 4, 5, 6]
                if (x not in allowed_range) or (y not in allowed_range):
                    print("Integers have to be from 1 to 6")
                    continue
                target = Point(x - 1, y - 1)
                return target

    def game_loop(self):
        player_ocean = self.random_ocean()
        computer_ocean = self.random_ocean(is_visible = False)
        print("Player ocean")
        player_ocean.view_ocean()
        print("Computer ocean")
        computer_ocean.view_ocean()

        game_is_over = False
        while not game_is_over:
            is_successful_shot = False
            while not is_successful_shot:
                try:
                    target = self.pick_a_target()
                    player_ocean.take_a_shot(target)
                    print(f"Computer targets {target}")
                    player_ocean.view_ocean()
                    if player_ocean.ships_afloat == 0:
                        print("Computer won!")
                        game_is_over = True
                    is_successful_shot = True
                except PointInUseError:
                    continue
            is_successful_shot = False
            while not is_successful_shot:
                try:
                    print("Computer ocean")
                    computer_ocean.view_ocean()
                    target = self.pick_a_target(is_player=True)
                    computer_ocean.take_a_shot(target)
                    print(f"Player targets {target}")
                    print("Computer ocean")
                    computer_ocean.view_ocean()
                    if computer_ocean.ships_afloat == 0:
                        print("Player won!")
                        game_is_over = True
                    is_successful_shot = True
                except PointInUseError:
                    continue





game1 = Game()
game1.game_loop()


