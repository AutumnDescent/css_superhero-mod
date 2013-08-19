import es
import random
import playerlib
import gamethread
import random
from playerlib import getPlayer, UseridError
superhero = es.import_addon('superhero')
global gusers
gusers = {}

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Goku")

def unload():
    gamethread.cancelDelayed(KI_regen)

def es_map_start(ev):
    gamethread.cancelDelayed(KI_regen)

def player_spawn(ev):
    global gusers
    userid = ev['userid']
    if superhero.hasHero(userid,'Goku'):
        gamethread.cancelDelayed(KI_regen)
        player = playerlib.getPlayer(userid)
        gusers[userid] = {}
        gusers[userid]['LVL'] = 0
        gusers[userid]['RegenKI'] = 1
        gusers[userid]['GokuJump'] = 1.0
        player.armor = 100
        KI_regen(userid)
        
def player_death(ev):
    global gusers
    userid = ev['userid']
    if superhero.hasHero(userid,'Goku'):
        gusers[userid]['RegenKI'] = 0

def round_end(ev):
    global gusers
    userid = ev['userid']
    if superhero.hasHero(userid,'Goku'):
        gamethread.cancelDelayed(KI_regen)
        gusers[userid]['RegenKI'] = 0
        
def power():
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        if 'LVL' in gusers[userid]:
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
    for userid in es.getUseridList():
        if not es.exists('userid',userid):
            return
        global gusers
        if superhero.hasHero(userid, 'Goku'): 
            player = playerlib.getPlayer(userid)
            if int(player.isdead) != 1:
                gusers[userid] = {}            
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
                if 'RegenKI' in gusers[userid]:
                    if gusers[userid]['RegenKI'] == 1:
                        gamethread.delayedname(1, KI_regen, KI_regen)
                else: gusers[userid]['RegenKI'] = 0
                                                
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
    es.tell(userid, '#multi', '#green[SH]#lightgreen You are back to normal')
    
def player_jump(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Goku'):
        es.server.cmd('es_xfire %s %s addoutput "Gravity %s"' % (userid,'!self', gusers[userid]['GokuJump']))
