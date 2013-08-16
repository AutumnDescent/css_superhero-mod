import es
import random
import playerlib
import usermsg
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Dracula")

def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    damage = int(ev['dmg_health'])
    chance = 25
    dice = random.randint(1,100)
    if dice <= chance:
        if superhero.hasHero(attacker,'Dracula'):
            drain = 0.5
            health = int(damage*drain)
            player = playerlib.getPlayer(attacker)
            player.health = player.health + health
            es.centertell(attacker,'Drained',health,'Health')