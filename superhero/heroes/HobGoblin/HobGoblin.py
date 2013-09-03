import es
from gamethread import delayed
import playerlib
import weaponlib
import spe_effects
import usermsg
import time
import random
import gamethread
from random import randint
import psyco
psyco.full()
superhero = es.import_addon('superhero')
rand = random.randint(5,15)
delayname = 'sh_hobgob_%s'
GOBHE_DELAY = rand

def load():
    es.dbgmsg(0, "[SH] Successfully loaded HobGoblin")

def unload():
    gamethread.cancelDelayed(check_nade)

def es_map_start(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def round_end(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def player_disconnect(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def player_spawn(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid,'HobGoblin'):
        return
    gamethread.cancelDelayed(delayname % ev['userid'])
    check_nade(userid)

def selected():
    userid = es.getcmduserid()
    if not superhero.hasHero(userid,'HobGoblin'):
        return
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        check_nade(userid)
    
def check_nade(userid):
    userid = str(userid)
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        if int(es.getplayerprop(userid, "CBasePlayer.localdata.m_iAmmo.011")) != 1:
            gamethread.delayed(0.1, es.server.cmd, 'es_xgive %s weapon_hegrenade' % userid)
        gamethread.cancelDelayed(delayname % player)
        gamethread.delayedname(GOBHE_DELAY, delayname % player, check_nade, player)
    
def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    damage = int(ev['dmg_health'])
    weapon = ev['weapon']
    if userid != attacker:
        if not superhero.hasHero(attacker,'HobGoblin'):
            return
        if weapon == 'hegrenade':
            rand = random.randint(10,50)*2
            es.server.queuecmd('damage %s %i 1024 %s' % (userid,rand,attacker))

def weapon_fire(ev):
    userid = ev['userid']
    weapon = ev['weapon']
    if not superhero.hasHero(userid,'HobGoblin'):
        return
    if weapon == 'hegrenade': delayed(0.2, HG_Trail, userid)

def HG_Trail(uid):
    handle = es.getplayerhandle(uid)
    index = 0
    for index in es.getEntityIndexes('hegrenade_projectile'):
        if handle == es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity'):
            spe_effects.beamFollow(
                '#all', # users
                0., # fDelay
                index, # iEntityIndex
                'sprites/laser.vmt', # szModelPath
                1, # iHaloIndex
                0.5, # fLife
                16, # fWidth
                4, # fEndWidth
                0, # fFadeLength
                0, # iRed
                255, # iGreen
                0, # iBlue
                255, # iAlpha
            )
