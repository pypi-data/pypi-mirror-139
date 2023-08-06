import requests
import sys
sys.path.insert(0,".")
from errors import *
from mojang import MojangAPI
from vars import *
from utils import *

__all__ = ['Key']

class Key():
    def __init__(self,key):
        keyRequest = requests.get(HYPIXELAPIURL.format("key",key))

        verifyResponse(keyRequest)
        KEY.append(key)
        self.keyRequest = keyRequest.json()['record']

    def key(self):
        return self.keyRequest['key']

    def ownerUUID(self):
        return self.keyRequest['owner']

    def limit(self):
        return self.keyRequest['limit']

    def queriesInPastMin(self):
        return self.keyRequest['queriesInPastMin']
        
    def totalQueries(self):
        return self.keyRequest['totalQueries']

    def ownerIGN(self):
        return MojangAPI.get_username(self.keyRequest['owner'])