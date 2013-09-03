import es
import playerlib
from playerlib import getPlayer
import spe_effects
import gamethread
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Daredevil")

def unload():
    gamethread.cancelDelayed(beacon)

def player_spawn(ev):
    userid = int(ev['userid'])
    if not superhero.hasHero(userid,'Daredevil'):
        return
    gamethread.cancelDelayed("beacon_%i" % userid)
    beacon(userid)

def es_map_start(ev):
    gamethread.cancelDelayed(beacon)

def player_disconnect(ev):
    userid = int(ev['userid'])
    gamethread.cancelDelayed("beacon_%i" % userid)

def player_death(ev):
    userid = int(ev['userid'])
    gamethread.cancelDelayed("beacon_%i" % userid)

def selected():
    userid = es.getcmduserid()
    if not superhero.hasHero(userid,'Daredevil'):
        return
    gamethread.cancelDelayed("beacon_%i" % userid)
    beacon(userid)

def beacon(userid):
    userid = int(userid)
    for player in playerlib.getPlayerList('#alive'):
        if player.team == 2:
            iRed = 255
            iBlue = 0
        else:
            iRed = 0
            iBlue = 255
        spe_effects.beamRingPoint(
        userid, #'#all', # users
        0., # fDelay
        player.location, # vOrigin
        0., # fStartRadius
        600., # fEndRadius
        'sprites/lgtning.vmt', # szModelPath
        1, # iHaloIndex
        0, # iStartFrame
        255, # iFrameRate
        0.3, # fLife
        12, # fWidth
        0, # iSpread
        2., # fAmplitude
        iRed, # iRed
        0, # iGreen
        iBlue, # iBlue
        255, # iAlpha
        0.5, # iSpeed
        0, # iFlags
        )
    gamethread.delayedname(2, 'beacon_%i' % userid, beacon, userid)