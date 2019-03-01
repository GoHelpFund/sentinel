import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from helpd import HelpDaemon
from help_config import HelpConfig


def test_helpd():
    config_text = HelpConfig.slurp_config_file(config.help_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000003c7c7081971e51d8d48bb75be79a61f3fa1f0e95e88822d93e1e667e530'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000a5e44bccde3ad9b350959d39f1609c18d2ab7d3643fdb97d6dd1cf8b207'

    creds = HelpConfig.get_rpc_creds(config_text, network)
    helpd = HelpDaemon(**creds)
    assert helpd.rpc_command is not None

    assert hasattr(helpd, 'rpc_connection')

    # Help testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
    # test commands without arguments
    info = helpd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert helpd.rpc_command('getblockhash', 0) == genesis_hash
