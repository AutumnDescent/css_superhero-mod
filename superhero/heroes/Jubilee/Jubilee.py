import es
import playerlib
import gamethread
import time
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Jubilee")

def unload():
    gamethread.cancelDelayed("Unblind")
    
def player_spawn(ev):
    userid = ev['userid']
    if es.exists('userid',userid):
        if superhero.hasHero(userid,'Jubilee'):
            player = playerlib.getPlayer(userid)
            if not playerlib.getPlayer(userid).isdead:
                superhero.Users[userid]['jub_cooldown'] = int(time.time()) + 5
                superhero.Users[userid]['jub_protect'] = 0
            
def power():
    userid = str(es.getcmduserid())
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        powerx = str(superhero.Users[userid]['powerx'])
        if superhero.Users[userid][powerx] == 'Jubilee':
            if not 'jub_cooldown' in superhero.Users[userid]:
                superhero.Users[userid]['jub_cooldown'] = int(time.time()) + 5
            if int(time.time()) >= int(superhero.Users[userid]['jub_cooldown']):
                es.tell(userid, '#multi', '#green[SH]#lightgreen Jubilee pink shades now protect you from flashbangs')
                fade(userid, 0, 5, 5, 64, 0, 64, 130)
                superhero.Users[userid]['jub_protect'] = 1
                superhero.Users[userid]['jub_cooldown'] = int(time.time()) + 30
                gamethread.delayed(10, Unblind, userid)
            else:
                es.tell(userid, '#multi', '#green[SH]#lightgreen Cannot activate Jubilee #green',int(superhero.Users[userid]['jub_cooldown'])-int(time.time()),'#lightgreenseconds left')
            
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
        if not 'jub_protect' in superhero.Users[userid]:
            superhero.Users[userid]['jub_protect'] = 0
        elif superhero.Users[userid]['jub_protect'] == 1:
            playerBlinded(userid)

def playerBlinded(userid):
		es.setplayerprop(userid, 'CCSPlayer.m_flFlashMaxAlpha', 0)
		es.setplayerprop(userid, 'CCSPlayer.m_flFlashDuration', 0)
        
def Unblind(userid):
    superhero.Users[userid]['jub_protect'] = 0
    es.tell(userid, '#multi', '#green[SH]#lightgreen Jubilee protection has ended, now you are vulnerable to flashes')