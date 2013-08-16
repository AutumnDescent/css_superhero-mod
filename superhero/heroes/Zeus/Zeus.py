import es
import playerlib
import random
import gamethread
import psyco
psyco.full()
from collections import defaultdict
from playerlib import getPlayerList
MAX_SPAWNS = 1
spawns = defaultdict(int)
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Zeus")

def unload():
    gamethread.cancelDelayed(respawn)

def es_map_start(ev):
    gamethread.cancelDelayed(respawn)

def round_start(ev):
    spawns.clear()
    
def player_death(ev):
    userid = ev['userid']
    team = int(es.getplayerteam(userid))
    if team == 2: s_team = '#all,#t'
    if team == 3: s_team = '#all,#ct'
    PlayerList = playerlib.getPlayerList(s_team)
    for player in PlayerList:
        loop_userid = player.userid
        loop_userid != userid
        if superhero.hasHero(player.userid,'Zeus'):
            if spawns[loop_userid] < MAX_SPAWNS:
                if int(player.userid) != int(userid):
                    rand = int(random.randint(1,1))
                    if rand == 1:
                        spawns[loop_userid] += 1
                        gamethread.delayed(2,respawn,(userid,player))              
                
def respawn(userid,player):
    es.setplayerprop(userid, "CCSPlayer.m_iPlayerState", 0)
    es.setplayerprop(userid, "CCSPlayer.baseclass.m_lifeState", 512)
    command = 'es_xspawnplayer '+userid
    gamethread.delayed(0.01,es.server.queuecmd,(command))
    spawner = es.getplayername(player.userid)
    other = es.getplayername(userid)
    es.msg('#multi','#green[SH]',other,'#lightgreenhas been respawned by#green',spawner,'#lightgreenZeus!')