import es
import playerlib
import langlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Flash")
    
def player_spawn(ev):
    userid = ev['userid']
    if not es.exists('userid',userid):
        return
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        if superhero.hasHero(userid,'Flash'):
            player.set("speed", 1.5)
            superhero.Users[userid]['speed'] = 1.5
        else:
            if userid in superhero.Users:
                superhero.Users[userid]['speed'] = 1.0