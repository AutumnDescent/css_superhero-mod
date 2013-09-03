import es
import playerlib
import usermsg
import gamethread
import random
superhero = es.import_addon('superhero')
import psyco
psyco.full()
delayname = 'sh_wolverine_%s'
WOLVERINE_DELAY = 0.7

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Wolverine")

def unload():
    gamethread.cancelDelayed(auto_heal)

def es_map_start(ev):
    gamethread.cancelDelayed(auto_heal)
    
def round_end(ev):
    gamethread.cancelDelayed(auto_heal)

def player_disconnect(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def player_spawn(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid,'Wolverine'):
        return
    gamethread.cancelDelayed(delayname % ev['userid'])
    auto_heal(userid)

def selected():
    userid = es.getcmduserid()
    if not superhero.hasHero(userid,'Wolverine'):
        return
    player = playerlib.getPlayer(userid)
    if not player.isdead:
        auto_heal(userid)
    
def auto_heal(userid):
    userid = str(userid)
    if not superhero.hasHero(userid,'Wolverine'):
        return
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        health = player.health
        if health < 100:
            player.health = health + 1
        gamethread.delayedname(WOLVERINE_DELAY, delayname % player, auto_heal, player)
