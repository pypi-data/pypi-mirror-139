import requests

class Voxyl_API:

    def __init__(self, api_key):
        self.api_key = {'api': api_key}

    # Returns the correct UUID from a username with or without dashes
    # @username Any username that exists in Minecraft
    # @dashes Whether to include dashes in the UUID (True|False)
    def username_to_uuid(self, username, dashes=False):
        response = requests.get("https://api.mojang.com/users/profiles/minecraft/" + username)
        response_dict = response.json()
        if dashes == True:
            uuid_d = response_dict["id"][:8] + "-" + response_dict["id"][8:]
            uuid_d = uuid_d[:13] + "-" + uuid_d[13:]
            uuid_d = uuid_d[:18] + "-" + uuid_d[18:]
            uuid_d = uuid_d[:23] + "-" + uuid_d[23:]
            return uuid_d
        else:
            return response_dict["id"]
    
    # Returns the rank of the given username
    # @username Any username that has joined the Voxyl Network
    def get_rank(self, username):
        response = requests.get("https://api.voxyl.net/player/info/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        return response_dict["role"]
    
    # Returns the last login time of the given username
    # @username Any username that has joined the Voxyl Network
    def get_lastlogintime(self, username):
        response = requests.get("https://api.voxyl.net/player/info/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        return response_dict["lastLoginTime"]
    
    # Returns the last known name of the given username
    # @username Any username that has joined the Voxyl Network
    def get_lastloginname(self, username):
        response = requests.get("https://api.voxyl.net/player/info/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        return response_dict["lastLoginName"]
    
    # Returns the level of the given username
    # @username Any username that has joined the Voxyl Network
    def get_level(self, username):
        response = requests.get("https://api.voxyl.net/player/stats/overall/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        return response_dict["level"]
    
    # Returns the amount of exp of the given username
    # @username Any username that has joined the Voxyl Network
    def get_exp(self, username):
        response = requests.get("https://api.voxyl.net/player/stats/overall/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        return response_dict["exp"]
    
    # Returns the amount of weighted wins of the given username
    # @username Any username that has joined the Voxyl Network
    def get_weightedwins(self, username):
        response = requests.get("https://api.voxyl.net/player/stats/overall/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        return response_dict["weightedwins"]

    # Returns stats for the given username
    # @username Any username that has joined the Voxyl Network
    # @game Any game on the Voxyl Network
    # @data Any specific statistic ("wins"|"kills"|"beds"|"finals")
    def get_stats(self, username, game=None, data=None):
        response = requests.get("https://api.voxyl.net/player/stats/game/" + self.username_to_uuid(username, True), params=self.api_key)
        response_dict = response.json()
        if game == None and data == None:
            return response_dict["stats"]
        elif game != None and data == None:
            return response_dict["stats"][game]
        elif game != None and data != None:
            return response_dict["stats"][game][data]
    
    # Returns any guild info for the given guild tag
    # @tag Any valid guild tag
    # @data Any specific type of data of the given guild ("id"|"name"|"desc"|"xp"|"num"|"ownerUUID"|"time")
    def get_guildinfo(self, tag, data=None):
        response = requests.get("https://api.voxyl.net/guild/info/" + tag, params=self.api_key)
        response_dict = response.json()
        if data == None:
            return response_dict
        else:
            return response_dict[data]
    
    # Returns the amount of weighted wins of the given username
    # @place The guild with this rank will be returned
    def get_topguilds(self, place=None):
        response = requests.get("https://api.voxyl.net/guild/top/", params={'api': self.api_key.get("api"), 'num': 100})
        response_dict = response.json()
        if place == None:
            return response_dict["guilds"]
        else:
            return response_dict["guilds"][place - 1]