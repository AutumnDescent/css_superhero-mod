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
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded HobGoblin")

def unload():
    gamethread.cancelDelayed(check_nade)

def es_map_start(ev):
    gamethread.cancelDelayed(check_nade)

def round_end(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'HobGoblin'):
        gamethread.cancelDelayed(check_nade)

def player_spawn(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'HobGoblin'):
        player = playerlib.getPlayer(userid)          
        if not player.isdead:
            gamethread.cancelDelayed(check_nade)
            check_nade()
    
def check_nade():
    for userid in superhero.Users:
        rand = random.randint(5,15)
        if not es.exists('userid',userid):
            return
        if superhero.hasHero(userid,'HobGoblin'):
            player = playerlib.getPlayer(userid)          
            if not player.isdead:
                if int(es.getplayerprop(userid, "CBasePlayer.localdata.m_iAmmo.011")) != 1:
                    gamethread.delayed(2, es.server.queuecmd, 'es_xgive %s weapon_hegrenade' % userid)
                es.delayed(rand,'es_xdoblock superhero/heroes/HobGoblin/check_nade')
    
def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    damage = int(ev['dmg_health'])
    weapon = ev['weapon']
    if userid != attacker:
        if superhero.hasHero(attacker,'HobGoblin'):
            if weapon == 'hegrenade':
                rand = random.randint(10,50)*2
                es.server.queuecmd('damage %s %i 1024 %s' % (userid,rand,attacker))

def weapon_fire(ev):
    userid = ev['userid']
    weapon = ev['weapon']
    if superhero.hasHero(userid,'HobGoblin'):
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