from enum import Enum


class Action(Enum):
    DELETE_WITHDRAW = 'DELETE_WITHDRAW'
    DELETE_WAIVE = 'DELETE_WAIVE'


def is_valid_action(value):
    return value in {member.value for member in Action}
