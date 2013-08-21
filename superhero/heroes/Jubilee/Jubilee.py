import es
import playerlib
import gamethread
import time
superhero = es.import_addon('superhero')
from collections import defaultdict
MAX_POW = 1
jub = defaultdict(int)

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Jubilee")

def unload():
    gamethread.cancelDelayed("Unblind")
            
def power():
    userid = str(es.getcmduserid())
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        if jub[userid] < MAX_POW:
            es.tell(userid, '#multi', '#green[SH]#lightgreen Jubilee pink shades now protect you from flashbangs')
            fade(userid, 0, 5, 5, 64, 0, 64, 130)
            gamethread.delayed(12, Unblind, userid)
            jub[userid] += 1
            
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
    if not superhero.hasHero(userid,'Jubilee'):
        return
    if jub[userid] == 1:
        es.setplayerprop(userid,'CCSPlayer.m_flFlashMaxAlpha',0)
	es.setplayerprop(userid,'CCSPlayer.m_flFlashDuration',0)
        
def Unblind(userid):
    userid = str(userid)
    jub[userid] = 0
    es.tell(userid, '#multi', '#green[SH]#lightgreen Jubilee protection has ended, now you are vulnerable to flashes')