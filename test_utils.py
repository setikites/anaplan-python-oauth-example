"""
test cases for utils
"""

import pytest
import shlex
import utils

def test_shlex():
    # I want to write this
    command = '-d -g Brian'

    # command parsers want this
    as_list = ['-d', '-g', 'Brian']

    # shlex.split() does the work for me
    assert shlex.split(command) == as_list


@pytest.mark.parametrize(
    'command, register, client_id, token_ttl, auth_flow, code, secret',
    [
        # no params
        ("", False, None, None, False, None, None),
        # each param
        ("-r", True, None, None, False, None, None),
        ("--client_id Name", False, 'Name', None, False, None, None),
        ("--token_ttl Name", False, None, 'Name', False, None, None),
        ("-a", False, None, None, True, None, None),
        ("--code Name", False, None, None, False, 'Name', None),
        ("--secret Name", False, None, None, False, None, 'Name'),
        # all params
        ("-r --client_id Client --token_ttl Token -a --secret Secret --code Code", True, 'Client', 'Token', True, 'Code', 'Secret'),
        # long form
        ("--register", True, None, None, False, None, None),
        ("--auth_flow", False, None, None, True, None, None),


    ])
def test_parse_args(command, register, client_id, token_ttl, auth_flow, code, secret):
    args = utils.read_cli_arguments(shlex.split(command))

    # or split them up, either works
    assert args.register == register
    assert args.client_id == client_id
    assert args.token_ttl == token_ttl
    assert args.auth_flow == auth_flow
    assert args.code == code
    assert args.secret == secret
    
