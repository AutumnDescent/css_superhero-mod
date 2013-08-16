import es
import playerlib
import usermsg
import gamethread
import random
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Wolverine")

def unload():
    gamethread.cancelDelayed(auto_heal)

def es_map_start(ev):
    gamethread.cancelDelayed(auto_heal)
    
def round_end(ev):
    gamethread.cancelDelayed(auto_heal)

def player_spawn(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Wolverine'):
        auto_heal()
    
def auto_heal():
    for userid in es.getUseridList():
        if not es.exists('userid',userid):
            return
        if superhero.hasHero(userid,'Wolverine'):
            player = playerlib.getPlayer(userid)
            if not playerlib.getPlayer(userid).isdead:
                health = player.health
                if health < 100:
                    player.health = health + 1
    gamethread.delayedname(2, auto_heal, auto_heal)
