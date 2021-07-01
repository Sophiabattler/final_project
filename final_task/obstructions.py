"""Class for creating obstructions"""
import os
import random
from typing import List, Tuple

os.system("")


class Obstructions:
    """Creates obstructions of various shapes"""

    def __init__(self, size_of_field: Tuple[int, int]):
        self.size_of_field = size_of_field
        self.all_obstructions = []
        self.amount = 0

    def dot_obstruction(self) -> List:
        """Create dot obstruction"""
        one_point = [
            random.randint(0, self.size_of_field[0]),
            random.randint(0, self.size_of_field[0]),
        ]
        return [one_point]

    def slash_obstruction(self) -> List:
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
        self.amount = (
            int(self.size_of_field[0] * self.size_of_field[1] * 0.2)
            if input_amount == ""
            else int(input_amount)
        )
        funcs = [
            self.dot_obstruction,
            self.slash_obstruction,
            self.square_obstruction,
        ]
        while self.amount > 0:
            rand_func = random.choice(funcs)
            points = []
            for point in rand_func():
                points.append(point)

            if all(point not in self.all_obstructions for point in points) and all(
                point != [part[0], part[1]] for part in all_parts for point in points
            ):
                self.all_obstructions.extend(points)
                self.amount -= 1

            if len(self.all_obstructions) == (self.size_of_field[0] + 1) * (
                self.size_of_field[1] + 1
            ) - len(all_parts):
                print(
                    f"\u001b[0;33mToo much obstructions, was not built {self.amount}\u001b[0m"
                )
                print(f"\u001b[0;30;45m{self.all_obstructions}\u001b[0m")
                return self.all_obstructions

        print(f"\u001b[0;30;45m{self.all_obstructions}\u001b[0m")
        return self.all_obstructions
