"""Class for creating field"""
import os
from typing import Tuple

os.system("")


class Field:
    """Creating field"""

    @classmethod
    def generate_size(cls) -> Tuple:
        """Allows a user to set the size of the field or sets default"""
        input_length = input("Please input x-size of the field:")
        input_width = input("Please input y-size of the field:")

        if not input_length.isdigit() or not input_width.isdigit():
            print(f"\u001b[0;33mIncorrect data! Try again!\u001b[0m")
            return cls.generate_size()

        length, width = int(input_length), int(input_width)
        size_of_field = (length, width)
        print(f"\u001b[0;33mCounting starts from zero\u001b[0m")
        print(f"{length}x{width}")
        return size_of_field
