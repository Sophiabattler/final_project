"""Initialization-file"""
from field import Field
from obstructions import Obstructions
from robot import Robot


def initialization():
    field = Field()
    size = field.generate_size()
    robot = Robot()
    robot.choose_shape_of_robot(size)
    obstructions = Obstructions(size)
    obstructions.build(robot.all_parts)
    robot.movement(obstructions.all_obstructions, size)
    return


if __name__ == "__main__":
    initialization()
