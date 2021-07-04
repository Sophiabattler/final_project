"""Class for manipulation with robot"""
import json
import os
import time
from functools import wraps
from typing import Callable, List, Tuple

os.system("")


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
        print(f"\u001b[0;30;42mCurrent position:{self.all_parts}\u001b[0m")

        if len(self.path) > 1:
            print(f"\u001b[0;33mLast position:{self.path[self.i - 1]}\u001b[0m")

    return wrapper


class Robot:
    """class allows user to choose the shape of the robot,
    manipulate the robot (change direction and coordinates),
    save the path taken by the robot and import it into a json-file"""

    def __init__(self):
        self.path = {}
        self.coordinates = []
        self.all_parts = []
        self.i = 0
        self.vision_range = 4
        self.max_len = 0

    def choose_shape_of_robot(self, field_size: Tuple):
        """Takes size of the field and allows user to choose
        the shape of the robot depends on size of the field"""
        if field_size[0] > 1 and field_size[1] > 1:
            robot_shapes = {
                "dot": self.dot_robot,
                "line": self.line_robot,
                "cross": self.cross_robot,
            }
            input_shape = input(
                "Please input shape of the robot(available: cross, line, dot):"
            )
            if input_shape in robot_shapes:
                return robot_shapes[input_shape](field_size)
            print("\u001b[0;30;43mWrong shape, try again\u001b[0m")
            return self.choose_shape_of_robot(field_size)

        if field_size[0] < 2 and field_size[1] < 2:
            print("\u001b[0;30;43mOnly dot-robot available\u001b[0m")
            return self.dot_robot(field_size)

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
            print(
                f"\u001b[0;30;41mYou can't move here, there is an obstruction\u001b[0m"
            )
            return self

        if condition:
            print(
                f"\u001b[0;30;41mYou can't move here, there is an edge of the field\u001b[0m"
            )
            return self

        return func_turn()

    def save_path(self):
        """Save path of the robot in json-file"""
        with open("path.json", "w", encoding="utf-8") as file:
            json.dump(self.path, file, ensure_ascii=False)

    def print_matrix(self, all_obstructions: List):
        """Print picture of еру robot in in a user-defined range"""
        self.max_len = 3 if len(self.all_parts) > 1 else 1
        input_vision_range = input("Please input vision range:")
        if not input_vision_range.isdigit():
            return self.print_matrix(all_obstructions)
        self.vision_range = int(input_vision_range)
        size = self.vision_range * 2 + self.max_len
        matrix_for_print = [[" " for _ in range(size)] for _ in range(size)]
        middle = int(len(matrix_for_print) / 2), int(len(matrix_for_print) / 2)
        matrix_for_print[int(len(matrix_for_print) / 2)][
            int(len(matrix_for_print) / 2)
        ] = self.coordinates[2]
        shift_x = self.coordinates[0] - middle[0]
        shift_y = self.coordinates[1] - middle[1]

        for part in self.all_parts:
            if part != self.coordinates:
                matrix_for_print[-1 - (part[1] - shift_y)][part[0] - shift_x] = "x"

        for obstruction in all_obstructions:
            if obstruction[0] - shift_x in range(size) and -1 - (
                obstruction[1] - shift_y
            ) in range(-size, 0):
                matrix_for_print[size - 1 - (obstruction[1] - shift_y)][
                    obstruction[0] - shift_x
                ] = "z"

        for i in matrix_for_print:
            new_string = " ".join(value.strip('"') for value in i)
            print(f"\u001b[0m{new_string}\u001b[0m")

    def movement(self, all_obstructions: List, field_size: Tuple):
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
        i - make an image of robot and surroundings (with curtain R)
        esc - program exit
        """
        print(
            "\u001b[0;33mCommand list:\n"
            "w - up (relative to the robot)\n"
            "s - down (relative to the robot)\n"
            "a - left (relative to the robot)\n"
            "d - right (relative to the robot)\n"
            "r - turn-right (90 degrees)\n"
            "l - turn-left (90 degrees)\n"
            "u - u-turn (180 degrees)\n"
            "p - keep path of the robot to json-file\n"
            "i - make an image of robot and surroundings (with curtain R)\n"
            "esc - program exit\u001b[0m"
        )
        pressed_key = ""
        while pressed_key != "esc":
            pressed_key = input("Input command:")
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

            if pressed_key == "i":
                self.print_matrix(all_obstructions)

            command_dict = {
                "p": self.save_path,
                "r": self.turn_right,
                "l": self.turn_left,
                "u": self.u_turn,
                "d": {
                    "↑": right_for_up,
                    "→": down_for_up,
                    "↓": left_for_up,
                    "←": up_for_up,
                },
                "w": {
                    "↑": up_for_up,
                    "→": right_for_up,
                    "↓": down_for_up,
                    "←": left_for_up,
                },
                "a": {
                    "↑": left_for_up,
                    "→": up_for_up,
                    "↓": right_for_up,
                    "←": down_for_up,
                },
                "s": {
                    "↑": down_for_up,
                    "→": left_for_up,
                    "↓": up_for_up,
                    "←": right_for_up,
                },
            }

            if pressed_key in command_dict:
                if type(command_dict[pressed_key]) != dict:
                    command_dict[pressed_key]()
                else:
                    if self.coordinates[2] in command_dict[pressed_key]:
                        self.change_coordinates(
                            *command_dict[pressed_key][self.coordinates[2]]
                        )

        return self
