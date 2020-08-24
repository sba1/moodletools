import configparser
import os
import requests

from xdg import BaseDirectory # type: ignore

from typing import Dict

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

def callws(config : Dict[str,str], remote : str, wsfunction : str, data : Dict[str,str] = {}):
    page = requests.post(remote + '/webservice/rest/server.php',
            data = dict({
            'wstoken':config['local_mobile_token'],
            'wsfunction':wsfunction,
            'moodlewsrestformat':'json',
            },**data))
    return page.json()
