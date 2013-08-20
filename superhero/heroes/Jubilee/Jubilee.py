import es
import playerlib
import gamethread
import time
superhero = es.import_addon('superhero')
from collections import defaultdict
MAX_POW = 1
jub = defaultdict(int)
global gusers
gusers = {}

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Jubilee")

def unload():
    gamethread.cancelDelayed("Unblind")
            
def power():
    global gusers
    userid = str(es.getcmduserid())
    gusers[userid] = {}
    gusers[userid]['jub_cooldown'] = int(time.time())
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
            if not 'jub_cooldown' in gusers[userid]:
                gusers[userid]['jub_cooldown'] = int(time.time()) + 5
            if int(time.time()) >= int(gusers[userid]['jub_cooldown']):
                if jub[userid] < MAX_POW:
                    es.tell(userid, '#multi', '#green[SH]#lightgreen Jubilee pink shades now protect you from flashbangs')
                    fade(userid, 0, 5, 5, 64, 0, 64, 130)
                    gusers[userid]['jub_cooldown'] = int(time.time()) + 25
                    gamethread.delayed(12, Unblind, userid)
                    jub[userid] += 1
            else:
                es.tell(userid, '#multi', '#green[SH]#lightgreen Cannot activate Jubilee #green',int(gusers[userid]['jub_cooldown'])-int(time.time()),'#lightgreenseconds left')
            
def fade(users, type, fadetime, totaltime, r, g, b, a):
    t = int(type)
    if t == 1:
        type = 2
    elif t == 0:
        type = 1
    else:
        type = 8 + 16
    es.usermsg("create", "fade", "Fade")
    es.usermsg("write", "short", "fade", float(fadetime) * 1000)
    es.usermsg("write", "short", "fade", float(totaltime) * 1000)
    es.usermsg("write", "short", "fade", int(type))
    es.usermsg("write", "byte", "fade", int(r))
    es.usermsg("write", "byte", "fade", int(g))
    es.usermsg("write", "byte", "fade", int(b))
    es.usermsg("write", "byte", "fade", int(a))
    es.usermsg("send", "fade", users)
    es.usermsg("delete", "fade")
    
def player_blind(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Jubilee'):
        global gusers
        if jub[userid] == 1:
            es.setplayerprop(userid,'CCSPlayer.m_flFlashMaxAlpha',0)
	    es.setplayerprop(userid,'CCSPlayer.m_flFlashDuration',0)
        
def Unblind(userid):
    global gusers
    userid = str(userid)
    jub[userid] = 0
    es.tell(userid, '#multi', '#green[SH]#lightgreen Jubilee protection has ended, now you are vulnerable to flashes')
