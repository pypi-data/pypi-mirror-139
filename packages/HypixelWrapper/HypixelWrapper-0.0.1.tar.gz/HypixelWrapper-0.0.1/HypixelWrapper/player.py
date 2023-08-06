import requests
from vars import *
from errors import * 
from mojang import MojangAPI
from math import sqrt
from utils import *

class Player():
    def __init__(self, UUID:str):
        if not KEY:
            raise APIKeyError("Key not set")

        UUID = checkUUID(UUID)

        playerResponse = requests.get(f'{HYPIXELAPIURL.format("player",KEY[0])}&uuid={UUID}')
        friendsResponse = requests.get(f'{HYPIXELAPIURL.format("friends",KEY[0])}&uuid={UUID}')

        verifyResponse(playerResponse)
        verifyResponse(friendsResponse)
        
        self.friendsJSON = friendsResponse.json()['records']
        self.playerJSON = playerResponse.json()['player']

    def ign(self):
        return self.playerJSON['displayname']

    def karma(self):
        return self.playerJSON['karma']

    def UUID(self):
        return self.playerJSON['uuid']
    
    def networkExp(self):
        return self.playerJSON['networkExp']
    
    def networkLevel(self):
        return (sqrt(int(self.playerJSON['networkExp'])*2+30625)/50)-2.5
    
    def knownAliases(self):
        return self.playerJSON['knownAliases']
 
    def loginLogoutInfo(self):
        info = {
            "firstLogin": self.playerJSON['firstLogin'],
        }

        try:
            info.update({
                "lastLogin": self.playerJSON['firstLogin'],
                "lastLogout": self.playerJSON['lastLogout'] 
            })
        except:
            info.update({
                "lastLogin": None,
                "lastLogout": None
            })

        return info
   
    def rank(self):
        rankLocations = ["prefix","rank","monthlyPackageRank","newPackageRank"]
        for rankLocation in rankLocations:
            if rankLocation in self.playerJSON:
                if self.playerJSON[rankLocation]!="NONE":
                    return self.playerJSON[rankLocation]
        
    def rankHistory(self):
        history = {}
        for rank in self.playerJSON:
            if "levelUp" in rank:
                history.update({
                        rank.replace("levelUp_",""):self.playerJSON[rank]
                    })
        return history
       
    def socialMediaLinks(self):
        linkedSocialMedia = {}
        for linked in self.playerJSON['socialMedia']['links']:
            linkedSocialMedia.update({
                linked:self.playerJSON['socialMedia']['links'][linked]
            })
        return linkedSocialMedia    
    
    def socialMediaLinked(self):
        socialMedia = {}
        for socialMediaAcc in self.playerJSON["socialMedia"]:
            if not socialMediaAcc in ["links","prompt"]:
                socialMedia.update({
                    socialMediaAcc:self.playerJSON['socialMedia'][socialMediaAcc]
                })
                
        return socialMedia    
    
    def friendCount(self):
        return len(self.friendsJSON)   
    
    def friendNameList(self):
        friendList = []
        UUID = self.UUID()
        for friend in self.friendsJSON:
            for uuid in friend:
                try:
                    if friend[uuid]!=UUID and len(friend[uuid])==32:
                        friendList.append(MojangAPI.get_username(friend[uuid]))
                except TypeError:
                    pass
        return friendList
    
    def friendUUIDList(self):
        friendList = []
        UUID = self.UUID()
        for friend in self.friendsJSON:
            for uuid in friend:
                try:
                    if friend[uuid]!=UUID and len(friend[uuid])==32:
                        friendList.append(friend[uuid])
                except TypeError:
                    pass
        return friendList
    
    def achievementPoints(self):
        return self.playerJSON['achievementPoints']
    
    def isOnline(self):
        statusResonse = requests.get(f'{HYPIXELAPIURL.format("status",KEY[0])}&uuid={self.UUID()}')
        verifyResponse(statusResonse)
        return statusResonse.json()['session']['online']
    
    def currentlyPlaying(self):
        statusResonse = requests.get(f'{HYPIXELAPIURL.format("status",KEY[0])}&uuid={self.UUID()}')
        verifyResponse(statusResonse)
        if not statusResonse.json()['session']['online']:
            raise PlayerNotOnlineError(f'{self.ign()} is not online!')
        statusResonse = statusResonse.json()['session']
        del statusResonse['online']
        return statusResonse
        
    def plusColor(self):
        return self.playerJSON['rankPlusColor']
        