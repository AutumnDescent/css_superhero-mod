import es
import random
import playerlib
from playerlib import getPlayer, UseridError
import gamethread
import random
superhero = es.import_addon('superhero')
global gusers
gusers = {}
import psyco
psyco.full()
delayname = 'sh_goku_%s'
KI_REGEN_DELAY = 1.0

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Goku")

def unload():
    gamethread.cancelDelayed(KI_regen)

def es_map_start(ev):
    gamethread.cancelDelayed(KI_regen)

def player_spawn(ev):
    global gusers
    userid = int(ev['userid'])
    if not superhero.hasHero(userid,'Goku'):
        return
    gamethread.cancelDelayed(delayname % ev['userid'])
    player = playerlib.getPlayer(userid)
    player.armor = 100
    KI_regen(userid)

def player_death(ev):
    global gusers
    userid = ev['userid']
    if not superhero.hasHero(userid,'Goku'):
        return
    gamethread.cancelDelayed(delayname % ev['userid'])

def round_end(ev):
    gamethread.cancelDelayed(KI_regen)

def player_disconnect(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])
        
def selected():
    global gusers
    userid = es.getcmduserid()
    for player in playerlib.getPlayerList('#alive'):
        if not superhero.hasHero(player,'Goku'):
            return
        gusers[userid] = {}
        gusers[userid]['LVL'] = 0
        player.armor = 100
        KI_regen(userid)

def power():
    global gusers
    userid = str(es.getcmduserid())
    for player in playerlib.getPlayerList('#alive'):
        if gusers[userid]['LVL'] == 0:
            es.tell(userid, '#multi', '#green[SH]#lightgreen Cant release KI, you have to be at least 1 lvl')
        elif gusers[userid]['LVL'] == 1:
            speed(userid, 1.5)
            setgravity(userid, 0.75)
            player.armor = 0
            es.tell(userid, '#multi', '#green[SH]#lightgreen You have released KI on 1 LVL')
            gamethread.delayed(10, speed, (userid, 1))
            gamethread.delayed(10, setgravity,(userid, 1))
            gamethread.delayed(10, endmessage, userid)
        elif gusers[userid]['LVL'] == 2:
            speed(userid, 2)
            setgravity(userid, 0.65)
            player.armor = 0
            es.tell(userid, '#multi', '#green[SH]#lightgreen You have released KI on 2 LVL')
            gamethread.delayed(10, speed, (userid, 1))
            gamethread.delayed(10, setgravity,(userid, 1))
            gamethread.delayed(10, endmessage, userid)
        elif gusers[userid]['LVL'] == 3:
            speed(userid, 2.30)
            setgravity(userid, 0.55)
            player.armor = 0
            es.tell(userid, '#multi', '#green[SH]#lightgreen You have released KI on 3 LVL')
            gamethread.delayed(10, speed, (userid, 1))
            gamethread.delayed(10, setgravity,(userid, 1))
            gamethread.delayed(10, endmessage, userid)
        elif gusers[userid]['LVL'] == 4:
            speed(userid, 2.60)
            setgravity(userid, 0.45)
            player.armor = 0
            es.tell(userid, '#multi', '#green[SH]#lightgreen You have released KI on 4 LVL! Destroy them all!')
            gamethread.delayed(10, speed, (userid, 1))
            gamethread.delayed(10, setgravity,(userid, 1))
            gamethread.delayed(10, endmessage, userid)
    else: gusers[userid]['LVL'] = 0

def KI_regen(userid):
    global gusers
    userid = str(userid)
    if not superhero.hasHero(userid, 'Goku'):
        return
    for player in playerlib.getPlayerList('#alive'):
        gusers[userid] = {}
        gusers[userid]['GokuJump'] = 1.0
        if player.armor < 450:
            player.armor = player.armor + 5
        if player.armor < 150:
            hsay(userid, 'Your LVL is 0!\nKI = %i'%player.armor)
            gusers[userid]['LVL'] = 0
        if player.armor in range(150, 226):
            hsay(userid, 'Your LVL is 1!\nKI = %i'%player.armor)
            gusers[userid]['LVL'] = 1
        elif player.armor in range(227, 301):
            hsay(userid, 'Your LVL is 2!\nKI = %i'%player.armor)
            gusers[userid]['LVL'] = 2
        elif player.armor in range(302, 376):
            hsay(userid, 'Your LVL is 3!\nKI = %i'%player.armor)
            gusers[userid]['LVL'] = 3
        elif player.armor > 375:
            hsay(userid, 'Your LVL is 4!\nKI = %i'%player.armor)
            gusers[userid]['LVL'] = 4
        gamethread.delayedname(KI_REGEN_DELAY, delayname % player, KI_regen, player)
                                                
def hsay(userid, text):
    es.usermsg("create", "hudhint", "HintText")
    es.usermsg("write", "string", "hudhint", unicode(text))
    es.usermsg("send", "hudhint", userid)
    es.usermsg("delete", "hudhint")
    
def speed(userid, value):
    es.setplayerprop(userid, "CBasePlayer.localdata.m_flLaggedMovementValue", value)
        
def setgravity(userid, ratio):
    global gusers
    gusers[userid] = {}
    if not 'GokuJump' in gusers[userid]:
        gusers[userid]['GokuJump'] = 1.0
    else: gusers[userid]['GokuJump'] = ratio
        
        
def endmessage(userid):
    userid = str(userid)
    if not es.exists('userid',userid):
        return
    es.tell(userid, '#multi', '#green[SH]#lightgreen You are back to normal')
    player = playerlib.getPlayer(userid)
    if superhero.hasHero(userid,'Flash'):
        player.set("speed", 1.5)
    else:
        return
    
#def player_jump(ev):
    #userid = ev['userid']
    #if not superhero.hasHero(userid,'Goku'):
        #return
    #es.server.cmd('es_xfire %s %s addoutput "Gravity %s"' % (userid,'!self', gusers[userid]['GokuJump']))