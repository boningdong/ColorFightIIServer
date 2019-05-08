from ..colorfight import Colorfight
from .util import *

import pytest

def test_invalid_uid():
    try:
        game = Colorfight()
        result = attack(game, 100, 0, 0, 100)
        assert(not result['success'])
    except Exception as e:
        assert(False)
        
def test_invalid_position():
    try:
        game = Colorfight()
        uid = join(game, 'a', 'a')
        game.update(True)
        result = attack(game, uid, -1, -1, 100)
        game.update(True)
        info = game.get_game_info()
        assert(len(info['error'][uid]) != 0)
    except Exception as e:
        assert(False)

def test_invalid_action_before_register():
    try:
        game = Colorfight()
        invalid_actions = [
            'test failed',
            '{"hello":"world"}',
            '{"action": "no_such_action"}',
            '{"action": "command", "cmd_list":["a 0 0 100"]}'
        ]
        for cmd in invalid_actions:
            result = game.parse_action(None, cmd)
            assert not result["success"], "{} does not trigger error".format(cmd)
    except Exception as e:
        assert False, e

def test_invalid_register():
    try:
        game = Colorfight()
        invalid_actions = [
            '{"action": "command", "cmd_list": ["a 0 0 100"]}',
            '{"action": "register", "username": ""}',
            '{"action": "register", "username": "abc"}',
            '{"action": "register", "username": "abc", "password": true}',
            '{"action": "register", "username": "abc", "password": 123}',
            '{"action": "register", "username": 123, "password": "abc}',
            '{"action": "register", "username": "", "password": "abc}',
            '{"action": "register", "username": "abcabcabcabcabcabcabcabcabc", "password": "abc}',
        ]
        for cmd in invalid_actions:
            result = game.parse_action(None, cmd)
            assert not result["success"], "{} does not trigger error".format(cmd)
    except Exception as e:
        assert False, "{}, {}".format(e, cmd)