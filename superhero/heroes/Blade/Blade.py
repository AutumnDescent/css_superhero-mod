import es
import random
import playerlib
import gamethread
import random
import usermsg
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Blade")

def unload():
    gamethread.cancelDelayed("unburn")

def es_map_start(ev):
    gamethread.cancelDelayed("unburn")
        
def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    if superhero.hasHero(attacker,'Blade'):
        if userid != attacker:
            if superhero.hasHero(userid,'Dracula'):
                chance = 60
            else: chance = 20
            if random.randint(1, 100) <= chance:
                player = playerlib.getPlayer(userid)
                player.burn()
                gamethread.delayed(1, unburn, userid)
            
def unburn(userid):
    es.fire(userid, "!self", "IgniteLifetime", 0)