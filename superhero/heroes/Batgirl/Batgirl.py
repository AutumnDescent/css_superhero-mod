from path import path
import es
import gamethread
import playerlib
import spe
import spe_effects
import time
import vecmath
from vecmath import Vector

superhero = es.import_addon('superhero')

####################
## Hero variables ##
####################
global hero
hero = {}
hero['name'] = 'TRP'
hero['cooldown'] = 0.5
hero['last_used'] = {}
hero['target'] = {}
hero['delay'] = 0.1
hero['delay_name'] = 'sh_trp_%s'

################################################
## getViewCoords() & createVector() variables ##
################################################
SIZE_VECTOR     = 12
SIZE_TRACE_T    = 84
MAX_COORD_RANGE = 16384

def load():
    spe.parseINI('superhero/heroes/%s/signatures.ini' % (hero['name']))
    es.dbgmsg(0, "[SH] Successfully loaded TRP")

def unload():
    userid = es.getcmduserid()
    gamethread.cancelDelayed(hero['delay_name'] % (userid))

def selected():
    global hero
    userid = es.getcmduserid()
    if not superhero.hasHero(userid, hero['name']):
        return

    ts = time.time()
    hero['last_used'][userid] = (ts - hero['cooldown'])
    hero['target'][userid] = False

def player_spawn(ev):
    global hero
    userid = ev['userid']
    if not superhero.hasHero(userid, hero['name']):
        return

    ts = time.time()
    hero['last_used'][userid] = (ts - hero['cooldown'])
    hero['target'][userid] = False

def player_death(ev):
    gamethread.cancelDelayed(hero['delay_name'] % (ev['userid']))

def player_disconnect(ev):
    gamethread.cancelDelayed(hero['delay_name'] % (ev['userid']))

def round_end(ev):
    gamethread.cancelDelayed(hero['delay_name'] % (ev['userid']))

def getViewCoords(userid, mask=0xFFFFFFFF, collisiongroup=0):
    player   = playerlib.getPlayer(userid)
    startvec = player.getEyeLocation()

    # Create start and end vector pointers
    pStart = createVector(*startvec)
    pEnd   = createVector(*list(Vector(startvec) + Vector(player.viewvector) \
        * MAX_COORD_RANGE))

    # Allocate space for the CGameTrace object
    ptr = spe.alloc(SIZE_TRACE_T)

    # Call UTIL_TraceLine()
    spe.call('TraceLine', pStart, pEnd, mask, spe.getPlayer(int(userid)),
        collisiongroup, ptr)

    # Wrap the end vector...
    x = spe.makeObject('Vector', ptr + 12)

    # ... and save the result
    result = x.x, x.y, x.z

    # Deallocate reserved space
    spe.dealloc(pStart)
    spe.dealloc(pEnd)
    spe.dealloc(ptr)

    # Finally, return the result
    return result

def createVector(x, y, z):
    obj = spe.makeObject('Vector', spe.alloc(SIZE_VECTOR))
    obj.x = x
    obj.y = y
    obj.z = z

    return obj.base

def power():
    global hero
    userid = es.getcmduserid()
    if not superhero.hasHero(userid, hero['name']):
        return

    ts = time.time()
    if not userid in hero['last_used']:
        hero['last_used'][userid] = (ts - hero['cooldown'])

    if not ts > hero['last_used'][userid]:
        cts = (hero['last_used'][userid] - ts + 1)
        if cts > 2:
            ext = 's'
        else:
            ext = ''
        es.tell(userid, '#green', '[%s] Cooldown: %d second%s left.' % (hero['name'], cts, ext))
        return

    es.tell(userid, '#green', '[%s] Power: Activated.' % (hero['name']))
    hero['last_used'][userid] = (ts + hero['cooldown'])
    hero['target'][userid] = vecmath.Vector(getViewCoords(userid))

    TRPLoop(userid)

    #vO = es.getplayerprop(userid, 'CBaseEntity.m_vecOrigin')
    #m = 1000
    #es.setplayerprop(userid, 'CCSPlayer.baseclass.localdata.m_vecBaseVelocity', '%s,%s,%s' % (vC[0]*m, vC[1]*m, vC[2]*m))

def poweroff():
    global hero
    userid = es.getcmduserid()
    heroB = {}
    heroB['target'] = {}
    for t in hero['target']:
        if not t == userid:
            heroB['target'][t] = hero['target'][t]
    hero['target'] = heroB['target']
    gamethread.cancelDelayed(hero['delay_name'] % (userid))

def TRPLoop(userid):
    global hero
    userid = str(userid)
    player = playerlib.getPlayer(userid)
    vC = player.viewVector()
    loc = es.getplayerlocation(userid)
    origin1 = vecmath.Vector(loc[0], loc[1], loc[2] + 50)
    origin2 = vecmath.Vector(getViewCoords(userid))

    if player.team == 2:
        iRed = 255
        iBlue = 0
    else:
        iRed = 0
        iBlue = 255

    spe_effects.beamPoints(
        '#all',                          # users
        0,                               # fDelay
        origin1,                         # vStartOrigin
        origin2,                         # vEndOrigin
        'sprites/laser.vmt',             # szModelPath
        0,                               # iHaloIndex
        0,                               # iStartFrame
        255,                             # iFrameRate
        hero['delay'],                   # fLife
        12,                              # fWidth
        12,                              # fEndWidth
        0,                               # fFadeLength
        0,                               # fAmplitude
        iRed,                            # iRed
        0,                               # iGreen
        iBlue,                           # iBlue
        255,                             # iAlpha
        1,                               # iSpeed
    )

    gamethread.delayedname(hero['delay'], hero['delay_name'] % (player), TRPLoop, player)
