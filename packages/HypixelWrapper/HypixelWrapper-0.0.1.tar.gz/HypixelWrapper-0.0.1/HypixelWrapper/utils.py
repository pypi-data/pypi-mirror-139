import requests
from errors import *
from mojang import MojangAPI
from vars import *

def verifyResponse(response:requests.Response):
    if response.status_code ==200:
        return
    raise ERRORS[response.status_code]
    
def checkUUID(UUID:str):
    if not(len(UUID) <= 16):
        return UUID
    UUID = MojangAPI.get_uuid(UUID)
    if UUID!=None:
        return UUID
    raise PlayerNotFoundError(f'Player not found!')
    