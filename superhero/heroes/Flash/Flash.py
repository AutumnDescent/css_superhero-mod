import es
import playerlib
import langlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Flash")
    
def player_spawn(ev):
    userid = ev['userid']
    player = playerlib.getPlayer(userid)
    if superhero.hasHero(userid,'Flash'):
        player.set("speed", 1.5)
    else:
        return

def selected():
    userid = es.getcmduserid()
    player = playerlib.getPlayer(userid)
    if superhero.hasHero(userid,'Flash'):
        player.set("speed", 1.5)
    else:
        return
