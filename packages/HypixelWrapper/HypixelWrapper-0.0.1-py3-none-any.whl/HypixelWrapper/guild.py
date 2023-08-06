import sys
sys.path.insert(0,".")
from errors import *
from vars import *
from utils import *
import requests
from mojang import MojangAPI

class Guild():
    def __init__(self,id=None,UUID=None,name=None):
        if not KEY:
            raise APIKeyError("Key not set")
        if id!=None:
            guildResponse = requests.get(f'{HYPIXELAPIURL.format("guild",KEY[0])}&id={id}')
        elif UUID!=None:
            guildResponse = requests.get(f'{HYPIXELAPIURL.format("guild",KEY[0])}&player={UUID}')
        elif name!=None:
            guildResponse = requests.get(f'{HYPIXELAPIURL.format("guild",KEY[0])}&name={name}')
            if guildResponse.json()['guild'] == None:
                raise GuildNotFoundError(f'Unable to find guild with name: {name}!')
        else:
            raise GuildNotFoundError(f'You need to specify a guild!')
        
        verifyResponse(guildResponse)
            
        self.guildJSON = guildResponse.json()['guild']
        
    def guildId(self):
        return self.guildJSON['_id']
    
    def name(self):
        return self.guildJSON['name']
    
    def created(self):
        return self.guildJSON['created']
    
    def tag(self):
        return self.guildJSON['tag']
    
    def tagColor(self):
        if 'tagColor' in self.guildJSON:
            return self.guildJSON['tagColor']
    
    def description(self):
        if 'description' in self.guildJSON:
            return self.guildJSON['description']
    
    def isPubliclyListed(self):
        if 'publiclyListed' in self.guildJSON:
            return self.guildJSON['publiclyListed']
    
    def guildExp(self):
        return self.guildJSON['exp']
    
    def guildExpByGame(self):
        return self.guildJSON['guildExpByGameType']
    
    def preferredGames(self):
        if 'preferredGames' in self.guildJSON:
            return self.guildJSON['preferredGames']
        
    def ranks(self):
        return self.guildJSON['ranks']
    
    def rank(self,name:str):
        for rank in self.guildJSON["ranks"]:
            for rankTag in rank:
                try:
                    if rank[rankTag].lower() == name.lower():
                        return rank
                except AttributeError:
                    pass
                
    def onlinePlayers(self):
        return self.guildJSON['achievements']['ONLINE_PLAYERS']
    
    def guildLevel(self):
        expNeeded = [
        100000,
        150000,
        250000,
        500000,
        750000,
        1000000,
        1250000,
        1500000,
        2000000,
        2500000,
        2500000,
        2500000,
        2500000,
        2500000,
        3000000,]

        level = 0
        exp = self.guildExp()

        for i in range(0, 1000):
            need = 0
            if i >= len(expNeeded):
                need = expNeeded[len(expNeeded) - 1]
            else:
                need = expNeeded[i]

            if (exp - need) < 0:
                return round((level + (exp / need)) * 100) / 100
            level += 1
            exp -= need
            
    def memberCount(self):
        return len(self.guildJSON['members'])
    
    def memberList(self):
        members = []
        for member in self.guildJSON['members']:
            members.append(MojangAPI.get_username(member['uuid']))
            
        return members
    
    def member(self,UUID:str):
        member = {}
        UUID = checkUUID(UUID)
        for memebers in self.guildJSON['members']:
            if memebers['uuid'] == UUID:
                member = memebers
                del member['expHistory']
                return member
            
        raise PlayerNotFoundError(f'Player is not in the guild!')
    
    def expHistory(self,UUID:str):
        UUID = checkUUID(UUID)
        for members in self.guildJSON['members']:
            if members['uuid']==UUID:
                return members['expHistory']
            
        raise PlayerNotFoundError(f'Player is not in the guild!')
    
    def gexpToday(self,UUID:str):
        UUID = checkUUID(UUID)
        for members in self.guildJSON['members']:
            if members['uuid']==UUID:
                return members['expHistory'][list(members['expHistory'].keys())[0]]
            
        raise PlayerNotFoundError(f'Player is not in the guild!')