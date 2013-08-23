import es
import playerlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Chucky")

def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    weapon = ev['weapon']
    if weapon == 'knife':
        if not superhero.hasHero(attacker,'Chucky'):
            return
        if userid != attacker:
            es.server.queuecmd('damage %s 40 1024 %s' % (userid,attacker))
            es.tell(attacker,'#multi','#green[SH]#lightgreen Chucky did extra Damage to#green',ev['es_username'])

def player_activeweapon(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid,'Chucky'):
        return
    weapon = ev['weapon']
    getspeed = playerlib.getPlayer(userid).speed
    if weapon == 'knife':
        player.set("speed", 1.5)
    else:
        player.set("speed", getspeed)

