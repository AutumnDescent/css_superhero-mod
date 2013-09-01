import es
import playerlib
import usermsg
import time
superhero = es.import_addon('superhero')
global gusers
gusers = {}

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Dazzler")

def player_spawn(ev):
    global gusers
    userid = ev['userid']
    if not superhero.hasHero(ev['userid'],'Dazzler'):
        return
    gusers[userid] = {}
    gusers[ev['userid']]['dazzle'] = int(time.time())

def selected():
    global gusers
    userid = es.getcmduserid()
    userid = str(userid)
    if not superhero.hasHero(userid,'Dazzler'):
        return
    gusers[userid] = {}
    gusers[userid]['dazzle'] = int(time.time())
    
def power():
    global gusers
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    for player in playerlib.getPlayerList('#alive'):
        if int(time.time()) >= int(gusers[userid]['dazzle']):
            nearPlayers = player.getNearPlayers(750)
            counter = 0
            for dude in nearPlayers:
                if playerlib.getPlayer(dude).teamid != player.teamid:
                    fade(dude, 1, 1, 2.5, 255, 255, 255, 255)
                    es.tell(dude,'#multi','#green[SH]#lightgreen You have been Dazzled by#green',es.getplayername(userid))
                    counter += 1
            fade(userid, 1, 0.1, 0.1, 255, 255, 255, 255)
            es.tell(userid,'#multi','#green[SH]#lightgreenYou dazzled #green',counter,'#lightgreenPlayers')
            gusers[userid]['dazzle'] = int(time.time()) + 30
        else:
            es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate #greenDazzler#lightgreen, you have to wait#green',int(gusers[userid]['dazzle'])-int(time.time()),'#lightgreenmore seconds')
        
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
