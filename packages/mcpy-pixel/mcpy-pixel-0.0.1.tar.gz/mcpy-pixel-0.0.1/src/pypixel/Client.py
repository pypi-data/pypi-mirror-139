import requests
import json
from pypixel.Player import *

class Client:
    def __init__(self, apikey):
        Client.apikey = apikey
    
    def get_uuid(self, plrname):
        res = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{plrname}')
        resj = res.json()
        return(resj['id'])
    
    def get_player(self, uuid):
        res = requests.get(f'https://api.hypixel.net/player?uuid={uuid}&key={self.apikey}')
        resj = json.loads(res.text)
        return Player.from_json(resj)



