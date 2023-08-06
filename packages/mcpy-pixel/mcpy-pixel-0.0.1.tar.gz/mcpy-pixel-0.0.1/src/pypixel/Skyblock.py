import requests
import json
from types import SimpleNamespace

class Skyblock:

    def get_profiles(uuid):
        from pypixel.Client import Client
        res = requests.get(f'https://api.hypixel.net/skyblock/profiles?uuid={uuid}&key={Client.apikey}')
        dump = json.loads(res.text)
        dencdata = dump['profiles'][0]
        data = json.dumps(dencdata)
        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return x