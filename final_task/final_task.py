"""Robot"""
import json
import random
import time
from functools import wraps
from typing import Callable, List, Tuple

import keyboard


class Field:
    """Creating field"""

    @classmethod
    def generate_size(cls) -> Tuple:
        """Allows a user to set the size of the field or sets default"""
        input_length = input("Please input x-size of the field:")
        input_width = input("Please input y-size of the field:")
        length = 10 if input_length == "" else int(input_length)
        width = 10 if input_width == "" else int(input_width)
        size_of_field = (length, width)
        print("Counting starts from zero")
        print(f"{length}x{width}")
        return size_of_field


class Obstructions:
    """Creates obstructions of various shapes"""

    def __init__(self, size_of_field: Tuple[int]):
        self.size_of_field = size_of_field
        self.all_obstructions = []

    def dot_obstruction(self) -> List:
        """Create dot obstruction"""
        one_point = [
            random.randint(0, self.size_of_field[0]),
            random.randint(0, self.size_of_field[0]),
        ]
        return [one_point]

    def backward_slash_obstruction(self) -> List:
        """Create backward slash obstruction"""
        first_point = [
            random.randint(1, self.size_of_field[0] - 1),
            random.randint(1, self.size_of_field[0] - 1),
        ]
        second_point = [first_point[0] - 1, first_point[1] + 1]
        return [first_point, second_point]

    def square_obstruction(self) -> List:
        """Create square obstruction"""
        first_point = [
            random.randint(1, self.size_of_field[0] - 1),
            random.randint(1, self.size_of_field[0] - 1),
        ]
        second_point = [first_point[0] + 1, first_point[1]]
        third_point = [first_point[0], first_point[1] + 1]
        fourth_point = [first_point[0] + 1, first_point[1] + 1]
        return [first_point, second_point, third_point, fourth_point]

    def build(self, all_parts) -> List:
        """Takes amount of obstructions from user and creates
        obstructions of various shapes(randomly)"""
        input_amount = input("Please input amount of obstructions:")
        amount = (
            int(self.size_of_field[0] * self.size_of_field[1] * 0.2)
            if input_amount == ""
            else int(input_amount)
        )
        funcs = [
            self.dot_obstruction,
            self.backward_slash_obstruction,
            self.square_obstruction,
        ]
        while amount > 0:
            rand_func = random.choice(funcs)
            points = []
            for point in rand_func():
                points.append(point)
            if all(point not in self.all_obstructions for point in points) and all(point != [part[0], part[1]] for part in all_parts for point in points):
                self.all_obstructions.extend(points)
                amount -= 1
            if len(self.all_obstructions) == (self.size_of_field[0] + 1) * (
                self.size_of_field[1] + 1
            ) - len(all_parts):
                print(
                    f"Too much obstructions, was not built {amount}"
                )
                print(self.all_obstructions)
                return sorted(self.all_obstructions)
        print(self.all_obstructions)
        return sorted(self.all_obstructions)


def _coord(func) -> Callable:
    """Wrapper-function adds current coordinates to path
    and prints current and last position of the robot"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.i += 1
        parts = []
        coord = []
        for part in self.all_parts:
            if part != self.coordinates:
                for index in range(2):
                    coord.append(part[index])
            else:
                for index in range(3):
                    coord.append(self.coordinates[index])
            parts.append(coord)
            coord = []
        self.path[self.i] = parts
        print(f"Current position:{self.all_parts}")
        if len(self.path) > 1:
            print(f"Last position:{self.path[self.i - 1]}")

    return wrapper


class Robot:
    """class allows user to choose the shape of the robot,
    manipulate the robot (change direction and coordinates),
    save the path taken by the robot and import it into a json-file"""

    def __init__(self):
        self.path = {}
        self.coordinates = []
        self.i = 0
        self.all_parts = []

    def choose_shape_of_robot(self, field_size: Tuple):
        """Takes size of the field and allows user to choose
        the shape of the robot depends on size of the field"""
        if field_size[0] > 1 and field_size[1] > 1:
            input_shape = input(
                "Please input shape of the robot(available: cross, line, dot):"
            )
            if input_shape == "dot":
                return self.dot_robot(field_size)
            if input_shape == "line":
                return self.line_robot(field_size)
            if input_shape == "cross":
                return self.cross_robot(field_size)
            print("Wrong shape, try again")
            return self.choose_shape_of_robot(field_size)
        if field_size[0] < 2 and field_size[1] > 1:
            input_shape = input(
                "Please input shape of the robot(available: line, dot):"
            )
            if input_shape == "dot":
                return self.dot_robot(field_size)
            if input_shape == "line":
                return self.line_robot(field_size)
            print("Wrong shape, try again")
            return self.choose_shape_of_robot(field_size)
        if field_size[0] < 2 and field_size[1] < 1:
            input_shape = input("Please input shape of the robot(available: dot):")
            if input_shape == "dot":
                return self.dot_robot(field_size)
            print("Wrong shape, try again")
            return self.choose_shape_of_robot(field_size)

    @_coord
    def dot_robot(self, field_size: Tuple):
        """Gives coordinates of dot-shape robot"""
        self.i -= 1
        self.coordinates = [int((field_size[0]) / 2), int((field_size[1]) / 2), "↑"]
        self.all_parts.append(self.coordinates)

    @_coord
    def line_robot(self, field_size: Tuple):
        """Gives coordinates of line-shape robot"""
        self.coordinates = [int((field_size[0]) / 2), int((field_size[1]) / 2), "↑"]
        first_part = [self.coordinates[0], self.coordinates[1] + 1]
        second_part = [self.coordinates[0], self.coordinates[1] - 1]
        self.all_parts = [first_part, self.coordinates, second_part]

    @_coord
    def cross_robot(self, field_size: Tuple):
        """Gives coordinates of cross-shape robot"""
        self.coordinates = [int((field_size[0]) / 2), int((field_size[1]) / 2), "↑"]
        part_up = [self.coordinates[0], self.coordinates[1] + 1]
        part_down = [self.coordinates[0], self.coordinates[1] - 1]
        part_right = [self.coordinates[0] + 1, self.coordinates[1]]
        part_left = [self.coordinates[0] - 1, self.coordinates[1]]
        self.all_parts = [part_up, part_down, self.coordinates, part_right, part_left]

    @_coord
    def right(self):
        """Shifts all parts of the robot to the right
        (relative to the screen orientation)"""
        for num in range(len(self.all_parts)):
            self.all_parts[num][0] += 1

    @_coord
    def left(self):
        """Shifts all parts of the robot to the left
        (relative to the screen orientation)"""
        for num in range(len(self.all_parts)):
            self.all_parts[num][0] -= 1

    @_coord
    def up(self):
        """Shifts all parts of the robot up
        (relative to the screen orientation)"""
        for num in range(len(self.all_parts)):
            self.all_parts[num][1] += 1

    @_coord
    def down(self):
        """Shifts all parts of the robot down
        (relative to the screen orientation)"""
        for num in range(len(self.all_parts)):
            self.all_parts[num][1] -= 1

    @_coord
    def turn_left(self):
        """Changes the direction of the robot's movement by 90 degrees
        to the left (relative to the screen orientation)"""
        turns = ["←", "↑", "→", "↓"]
        ind = turns.index(self.coordinates[2])
        self.coordinates[2] = turns[ind - 1]

    @_coord
    def turn_right(self):
        """Changes the direction of the robot's movement by 90 degrees
        to the right (relative to the screen orientation)"""
        turns = ["←", "↑", "→", "↓"]
        ind = turns.index(self.coordinates[2])
        self.coordinates[2] = turns[ind + 1] if ind < 3 else turns[0]

    @_coord
    def u_turn(self):
        """Changes the direction of the robot's movement
        by 180 degrees (relative to the screen orientation)"""
        turns = ["←", "↑", "→", "↓"]
        ind = turns.index(self.coordinates[2])
        self.coordinates[2] = turns[ind - 2]

    def change_coordinates(self, i, j, all_obstructions, condition, func_turn):
        """Checks if the ship will not collide with an obstruction
        or hit the edge of the field if the user wants to move the robot.
        If not, it calls a function that allows user to do this"""
        if any(
            [part[0] + i, part[1] + j] in all_obstructions for part in self.all_parts
        ):
            print("You can't move here, there is an obstruction")
            return self
        elif condition:
            print("You can't move here, there is an edge of the field")
            return self
        else:
            return func_turn()

    def save_path(self):
        """Save path of the robot in json-file"""
        with open("path.json", "w", encoding="utf-8") as file:
            json.dump(self.path, file, ensure_ascii=False)

    def movement(self, all_obstructions, field_size):
        """Takes size of the field and coordinates of obstructions.
        The function is responsible for the ability to control the robot from the keyboard.
        Command list:
        w - up (relative to the robot)
        s - down (relative to the robot)
        a - left (relative to the robot)
        d - right (relative to the robot)
        r - turn-right (90 degrees)
        l - turn-left (90 degrees)
        u - u-turn (180 degrees)
        p - keep path of the robot to json-file
        esc - program exit
        """
        print('To exit press "esc"')
        pressed_key = ""
        while pressed_key != "esc":
            pressed_key = keyboard.read_key()
            time.sleep(0.5)
            right_for_up = (
                1,
                0,
                all_obstructions,
                any(part[0] + 1 > field_size[0] for part in self.all_parts),
                self.right,
            )
            left_for_up = (
                -1,
                0,
                all_obstructions,
                any(part[0] - 1 < 0 for part in self.all_parts),
                self.left,
            )
            up_for_up = (
                0,
                1,
                all_obstructions,
                any(part[1] + 1 > field_size[1] for part in self.all_parts),
                self.up,
            )
            down_for_up = (
                0,
                -1,
                all_obstructions,
                any(part[1] - 1 < 0 for part in self.all_parts),
                self.down,
            )

            if pressed_key == "p":
                self.save_path()

            if pressed_key == "r":
                # turn right
                self.turn_right()

            if pressed_key == "l":
                # turn left
                self.turn_left()

            if pressed_key == "u":
                # u-turn
                self.u_turn()

            if self.coordinates[2] == "↑":
                if pressed_key == "d":
                    # right 1
                    self.change_coordinates(*right_for_up)

                elif pressed_key == "w":
                    # up 2
                    self.change_coordinates(*up_for_up)

                elif pressed_key == "a":
                    # left 3
                    self.change_coordinates(*left_for_up)

                elif pressed_key == "s":
                    # down 4
                    self.change_coordinates(*down_for_up)

            elif self.coordinates[2] == "→":
                if pressed_key == "d":
                    # right 4
                    self.change_coordinates(*down_for_up)

                elif pressed_key == "w":
                    # up 1
                    self.change_coordinates(*right_for_up)

                elif pressed_key == "a":
                    # left 2
                    self.change_coordinates(*up_for_up)

                elif pressed_key == "s":
                    # down 3
                    self.change_coordinates(*left_for_up)

            elif self.coordinates[2] == "↓":
                if pressed_key == "d":
                    # right 3
                    self.change_coordinates(*left_for_up)

                elif pressed_key == "w":
                    # up 4
                    self.change_coordinates(*down_for_up)

                elif pressed_key == "a":
                    # left 1
                    self.change_coordinates(*right_for_up)

                elif pressed_key == "s":
                    # down 2
                    self.change_coordinates(*up_for_up)

            elif self.coordinates[2] == "←":
                if pressed_key == "d":
                    # right 2
                    self.change_coordinates(*up_for_up)

                elif pressed_key == "w":
                    # up 1
                    self.change_coordinates(*left_for_up)

                elif pressed_key == "a":
                    # left 4
                    self.change_coordinates(*down_for_up)

                elif pressed_key == "s":
                    # down 3
                    self.change_coordinates(*right_for_up)
        return self


if __name__ == "__main__":
    field = Field()
    size = field.generate_size()
    robot = Robot()
    start_robot = robot.choose_shape_of_robot(size)
    obstructions = Obstructions(size)
    built = obstructions.build(robot.all_parts)
    move = robot.movement(obstructions.all_obstructions, size)
