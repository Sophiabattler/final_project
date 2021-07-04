"""Test for robot"""
import builtins
from unittest import mock
from unittest.mock import patch

from final_task.field import Field
from final_task.obstructions import Obstructions
from final_task.robot import Robot


def test_generate_size_with_correct_data():
    with mock.patch.object(builtins, "input", side_effect=["5", "6"]):
        assert Field.generate_size() == (5, 6)


def test_generate_size_with_incorrect_data_firstly():
    with mock.patch.object(builtins, "input", side_effect=["1", "q", "1", "2"]):
        assert Field.generate_size() == (1, 2)


def test_dot_shape_of_the_robot_with_small_size_of_the_field():
    robot = Robot()
    size = (1, 1)
    robot.choose_shape_of_robot(size)
    assert robot.all_parts == [[0, 0, "↑"]]


def test_dot_shape_of_the_robot_with_incorrect_data_firstly():
    robot = Robot()
    size = (5, 5)
    with mock.patch.object(builtins, "input", side_effect=["wrong_shape", "dot"]):
        robot.choose_shape_of_robot(size)
        assert robot.all_parts == [[2, 2, "↑"]]


def test_line_shape_of_the_robot_with_incorrect_data_firstly():
    robot = Robot()
    size = (5, 10)
    with mock.patch.object(builtins, "input", side_effect=["wrong_shape", "line"]):
        robot.choose_shape_of_robot(size)
        assert robot.all_parts == [[2, 6], [2, 5, "↑"], [2, 4]]


def test_cross_shape_of_the_robot_with_incorrect_data_firstly():
    robot = Robot()
    size = (10, 10)
    with mock.patch.object(builtins, "input", side_effect=["wrong_shape", "cross"]):
        robot.choose_shape_of_robot(size)
        assert robot.all_parts == [[5, 6], [5, 4], [5, 5, "↑"], [6, 5], [4, 5]]


def test_building_obstructions_different_shapes_when_too_much_obstructions():
    size = (5, 5)
    robot = Robot()
    with mock.patch.object(builtins, "input", side_effect=["cross", "40"]):
        robot.choose_shape_of_robot(size)
        obstructions = Obstructions(size)
        obstructions.build(robot.all_parts)
        assert obstructions.amount > 0
        for obstruction in obstructions.all_obstructions:
            assert obstruction not in robot.all_parts
            assert obstruction != [robot.coordinates[0], robot.coordinates[1]]
            assert [size[0], size[1]] >= obstruction >= [0, 0]


def test_building_obstructions_different_shapes_when_not_too_much_obstructions():
    size = (5, 5)
    robot = Robot()
    with mock.patch.object(builtins, "input", side_effect=["cross", "5"]):
        robot.choose_shape_of_robot(size)
        obstructions = Obstructions(size)
        obstructions.build(robot.all_parts)
        assert obstructions.amount == 0
        for obstruction in obstructions.all_obstructions:
            assert obstruction not in robot.all_parts
            assert obstruction != [robot.coordinates[0], robot.coordinates[1]]
            assert [size[0], size[1]] >= obstruction >= [0, 0]


@patch.object(builtins, "input", side_effect=["line", "d", "esc"])
def test_robot_can_not_move_if_an_obstruction(test_input):
    size = (4, 4)
    robot = Robot()
    all_obstructions = [[3, 3], [3, 4], [4, 3], [4, 4]]
    robot.choose_shape_of_robot(size)
    assert robot.all_parts == [[2, 3], [2, 2, "↑"], [2, 1]]
    robot.movement(all_obstructions, size)
    assert robot.all_parts == [[2, 3], [2, 2, "↑"], [2, 1]]


@patch.object(builtins, "input", side_effect=["line", "u", "esc"])
def test_robot_does_u_turn_and_move_if_there_is_not_an_obstruction(test_input):
    size = (4, 4)
    robot = Robot()
    all_obstructions = [[3, 3], [3, 4], [4, 3], [4, 4]]
    robot.choose_shape_of_robot(size)
    assert robot.all_parts == [[2, 3], [2, 2, "↑"], [2, 1]]
    robot.movement(all_obstructions, size)
    assert robot.all_parts == [[2, 3], [2, 2, "↓"], [2, 1]]


@patch.object(builtins, "input", side_effect=["line", "s", "d", "esc"])
def test_robot_remembers_its_path(test_input):
    size = (4, 4)
    robot = Robot()
    all_obstructions = [[3, 3], [3, 4], [4, 3], [4, 4]]
    robot.choose_shape_of_robot(size)
    assert robot.all_parts == [[2, 3], [2, 2, "↑"], [2, 1]]
    robot.movement(all_obstructions, size)
    assert robot.path == {
        1: [[2, 3], [2, 2, "↑"], [2, 1]],
        2: [[2, 2], [2, 1, "↑"], [2, 0]],
        3: [[3, 2], [3, 1, "↑"], [3, 0]],
    }


@patch.object(builtins, "input", side_effect=["dot", "s", "s", "s", "esc"])
def test_robot_can_not_move_outside_the_field(test_input):
    size = (1, 1)
    robot = Robot()
    all_obstructions = []
    robot.choose_shape_of_robot(size)
    assert robot.all_parts == [[0, 0, "↑"]]
    robot.movement(all_obstructions, size)
    assert robot.all_parts == [[0, 0, "↑"]]
    assert robot.path == {0: [[0, 0, "↑"]]}
