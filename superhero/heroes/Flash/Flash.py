import es
import playerlib
import langlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Flash")
    
def player_spawn(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid,'Flash'):
        return
    else:
        player = playerlib.getPlayer(userid)
        player.set("speed", 1.5)

def selected():
    userid = es.getcmduserid()
    if not superhero.hasHero(userid,'Flash'):
        return
    else:
        player = playerlib.getPlayer(userid)
        player.set("speed", 1.5)