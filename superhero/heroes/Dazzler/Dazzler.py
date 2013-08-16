import es
import playerlib
import usermsg
import time
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Dazzler")

def player_spawn(ev):
    userid = ev['userid']
    if superhero.hasHero(ev['userid'],'Dazzler'):
        player = playerlib.getPlayer(userid)
        if not playerlib.getPlayer(userid).isdead:
            superhero.Users[str(ev['userid'])]['dazzle'] = int(time.time())
    
def power():
    userid = str(es.getcmduserid())
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        powerx = str(superhero.Users[userid]['powerx'])
        if superhero.Users[userid][powerx] == 'Dazzler':
            if not 'dazzle' in superhero.Users[userid]:
                superhero.Users[userid]['dazzle'] = int(time.time()) + 15
            if int(time.time()) >= int(superhero.Users[userid]['dazzle']):
                nearPlayers = player.getNearPlayers(750)
                counter = 0
                for dude in nearPlayers:
                        if playerlib.getPlayer(dude).teamid != player.teamid:
                            fade(dude, 1, 1, 2.5, 255, 255, 255, 255)
                            es.tell(dude,'#multi','#green[SH]#lightgreen You have been Dazzled by#green',es.getplayername(userid))
                            counter += 1
                fade(userid, 1, 1, 2.5, 255, 255, 255, 255)
                es.tell(userid,'#multi','#green[SH]#lightgreenYou dazzled #green',counter,'#lightgreenPlayers')
                superhero.Users[userid]['dazzle'] = int(time.time()) + 15
            else:
                es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate #greenDazzler#lightgreen, you have to wait#green',int(superhero.Users[userid]['dazzle'])-int(time.time()),'#lightgreenmore seconds')
        
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