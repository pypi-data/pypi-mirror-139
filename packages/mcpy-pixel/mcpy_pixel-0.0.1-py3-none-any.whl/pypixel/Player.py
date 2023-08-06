class Player:

    @classmethod
    def from_json(cls, json_obj):
        player = cls()
        player.uuid = str(json_obj['player']['uuid'])
        player.displayname = str(json_obj['player']['displayname'])
        player.id = str(json_obj['player']['_id'])
        player.playername = str(json_obj['player']['playername'])

        return player