import requests_html
import requests
import sys
sys.path.insert(0,".")
from errors import *

class GuildLeaderboard:
    def __init__(self):
        Guilds = list((requests_html.HTML(html=requests.get(
            "https://sk1er.club/leaderboards/newdata/GUILD_LEVEL",headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
                                          .content).find('table',first=True).find('tbody',first=True).text).splitlines())
        index = 2
        self.Guildleaderboard = []
        for x in range(1000):
            self.Guildleaderboard.append((Guilds[index],Guilds[index+1],Guilds[index+3]))
            index += 8
        
    def isOnLeaderboard(self,guild:str):
        for guildName in self.Guildleaderboard:
            if guildName[0] == guild:
                return True
        return False
                        
    def top(self,top=10):
        topGuilds = []
        for index in range(top):
            topGuilds.append(self.Guildleaderboard[index][0])
        return topGuilds
    
    def guildPlacement(self,guild:str):
        for guildName in self.Guildleaderboard:
            if guildName[0] == guild:
                return self.Guildleaderboard.index(guildName)+1
        raise GuildNotFoundError(f'The guild {guild} is not on the leaderboard!')
    
    def guildLvl(self,guild:str):
        try:
            index = self.guildPlacement(guild)-1
            return self.Guildleaderboard[index][1]
        except TypeError:
            raise GuildNotFoundError(f'The guild {guild} is not on the leaderboard!')
        
    def guildExp(self,guild:str):
        try:
            index = self.guildPlacement(guild)-1
            return self.Guildleaderboard[index][2]
        except TypeError:
            raise GuildNotFoundError(f'The guild {guild} is not on the leaderboard!')
