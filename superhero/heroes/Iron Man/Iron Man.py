import es
import gamethread
import playerlib
from playerlib import getPlayer, UseridError
from effectlib import drawBox
superhero = es.import_addon('superhero')
delayname = 'sh_ironman_%s'
FUEL_REGEN_DELAY = 0.5
import psyco
psyco.full()

def load():
    es.dbgmsg(0, "[SH] Iron Man successfully loaded")

def unload():
    for userid in es.getUseridList():
        gamethread.cancelDelayed(delayname % userid)

def es_map_start(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def player_spawn(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid, 'Iron Man'):
        return
    fuel_regen(userid)

def round_end(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def player_hurt(ev):
    armor = int(ev['es_userarmor'])
    if armor < 150 and armor + int(ev['dmg_armor']) >= 150:
        player = getPlayer(ev['userid'])
        gamethread.cancelDelayed(delayname % player)
        gamethread.delayedname(FUEL_REGEN_DELAY, delayname % player, fuel_regen, player)

def player_death(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def player_disconnect(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def power():
    userid = str(es.getcmduserid())
    gamethread.cancelDelayed(delayname % userid)
    IronManLoop(getPlayer(userid))

def poweroff():
    userid = str(es.getcmduserid())
    gamethread.cancelDelayed(delayname % userid)
    gamethread.delayedname(FUEL_REGEN_DELAY, delayname % userid, fuel_regen, getPlayer(userid))

def IronManLoop(player):
    armor = player.armor
    if player.armor <= 1:
        es.tell(player, '#multi', '#green[SH]#lightgreen Not enough fuel, wait until it regens.')
        return # Stop this loop
    player.armor = armor - 2
    player.set("push", (0, 145, True))
    loc = player.location
    drawBox(loc, [loc[0] + 10, loc[1] + 10, loc[2]], "materials/sprites/laser.vmt", "materials/sprites/halo01.vmt", 0.2, 20, 20, 255, 0, 0, 255, 10, 0, 0, 0, 0)
    drawBox(loc, [loc[0] - 10, loc[1] - 10, loc[2]], "materials/sprites/laser.vmt", "materials/sprites/halo01.vmt", 0.2, 20, 20, 255, 128, 0, 255, 10, 0, 0, 0, 0)
    drawBox([loc[0] - 5, loc[1] - 5, loc[2]], [loc[0] + 5, loc[1] + 5, loc[2]], "materials/sprites/laser.vmt", "materials/sprites/halo01.vmt", 0.2, 20, 20, 0, 0, 255, 255, 10, 0, 0, 0, 0)
    es.emitsound('player', player, 'ambient/explosions/exp4.wav', 0.3, 0.4)
    gamethread.delayedname(0.1, delayname % player, IronManLoop, player)

def fuel_regen(userid):
    userid = str(userid)
    for player in playerlib.getPlayerList('#alive'):
        value = player.armor = (player.armor + 1) #min(player.armor + 1, 150)
        if value < 150:
            gamethread.delayedname(FUEL_REGEN_DELAY, delayname % player, fuel_regen, player)