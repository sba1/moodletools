import configparser
import getpass
import os
import sys
import requests

from xdg import BaseDirectory # type: ignore

from typing import Dict, Optional

def config() -> Dict[str, Dict[str, str]]:
    """Returns the moodlecli configuration.
    """
    config = configparser.ConfigParser()
    dict = {} # type: Dict[str, Dict[str, str]]
    for path in BaseDirectory.load_config_paths('moodlecli'):
        config.read(os.path.join(path, 'moodlecli.ini'))

    for section in config:
        for key in config[section]:
            if section not in dict:
                dict[section] = {}

            dict[section][key] = config[section][key]

    return dict

def store_config(config : Dict[str, Dict[str, str]]) -> None:
    cfg = configparser.ConfigParser()
    for section in config.keys():
        cfg.add_section(section)
        for key in config[section].keys():
            cfg.set(section, key, config[section][key])
    save_path = BaseDirectory.save_config_path('moodlecli')
    os.makedirs(save_path, exist_ok=True)
    with open(os.path.join(save_path, 'moodlecli.ini'), 'w') as cfgfile:
        cfg.write(cfgfile)

def config_resolve_remote(config : Dict[str, Dict[str, str]], remote : str) -> Optional[str]:
    """Tries to resolve the given remote name to the primary short name"""
    if remote in config:
        return remote

    for r in config:
        if config[r]['url'] == remote:
            return r

    return None

def rem_remote(name:str) -> None:
    cfg = config()
    key = config_resolve_remote(cfg, name)
    if key is not None:
        del cfg[key]
        store_config(cfg)

def get_token(url : str, service : str) -> Optional[str]:
    """Query the given URL for the token for the given service."""
    if not url.startswith('https://'):
        print("An unsecured connection is about to be established, do you want to continue (y/N)? ", end='', flush=True)
        answer = sys.stdin.readline().strip()
        if answer != 'y':
            return None

    print("User: ", end='', flush=True)
    username = sys.stdin.readline()
    password = getpass.getpass()

    page = requests.post(url + '/login/token.php',
        data = {
            'username': username,
            'password': password,
            'service': service,
            })
    return page.json()['token']

def callws(config : Dict[str,str], remote : str, wsfunction : str, data : Dict[str,str] = {}):
    if 'local_mobile_token' not in config:
        print('There is no local_mobile_token configured for remote {0}!'.format(
            remote), file=sys.stderr)
        return None

    if 'url' not in config:
        print('There is no url configured for remote {0}'.format(
            remote), file=sys.stderr)

    page = requests.post(config['url'] + '/webservice/rest/server.php',
            data = dict({
            'wstoken':config['local_mobile_token'],
            'wsfunction':wsfunction,
            'moodlewsrestformat':'json',
            },**data))
    return page.json()

def get_site_info(config : Dict[str,str], remote : str):
    site_info = callws(config, remote, 'core_webservice_get_site_info')
    if not site_info or 'userid' not in site_info:
        if site_info and site_info['message']:
            message = site_info['message']
            print(f'Command failed with message: {message}', file=sys.stderr)
        sys.exit('Could not determine userid.')
    return site_info
