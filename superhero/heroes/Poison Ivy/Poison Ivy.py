import es
import playerlib
import gamethread
from collections import defaultdict
from random import randint
poison = defaultdict(int)
MAX_POISON = 1
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Poison Ivy successfully loaded")

def unload():
    gamethread.cancelDelayed(VenomCycle)

def es_map_start(ev):
    gamethread.cancelDelayed(VenomCycle)

def round_start(ev):
    poison.clear()

def round_end(ev):
    poison.clear()

def player_hurt(ev):
    userid = ev['userid']
    attacker = int(ev['attacker'])
    if attacker and superhero.hasHero(attacker, 'Poison Ivy') and poison[attacker] < MAX_POISON:
        dice = randint(1,8)
        if dice == 1 or ev['weapon'] == 'knife':
            venom = randint(10, 30)
            es.tell(attacker, '#multi', '#green[SH]#lightgreen You have poisoned %s' % ev['es_username'])
            VenomCycle(userid, venom, attacker)
            es.tell(userid, '#multi', '#green[SH]#lightgreen #green%s #lightgreenhas poisoned you' % ev['es_attackername'])
            poison[attacker] += 1
           
def VenomCycle(userid, venom, attacker):
    if not es.getuserid(userid) or not es.getuserid(attacker):
        return
    player = playerlib.getPlayer(userid)
    if player.isdead:
        return
    if venom == 0:
        return
    elif venom == 1:
        es.server.queuecmd('damage %s 1 1024 %s'%(userid,attacker))
        venom -= 1
        fade(userid, 0, 0.2, 0.2, 0, 255, 0, 50)
    elif venom == 2:
        es.server.queuecmd('damage %s 2 1024 %s'%(userid,attacker))
        venom -=  2
    elif venom == 3:
         es.server.queuecmd('damage %s 3 1024 %s'%(userid,attacker))
         venom -= 3
         fade(userid, 0, 0.2, 0.2, 0, 255, 0, 50)
    elif venom > 0:
        es.server.queuecmd('damage %s 4 1024 %s'%(userid,attacker))
        venom -= 4
        fade(userid, 0, 0.2, 0.2, 0, 255, 0, 50)
    gamethread.delayedname(1, VenomCycle, VenomCycle, (userid, venom, attacker))


def fade(users, type_, fadetime, totaltime, r, g, b, a):
    if type_ in (0, 1):
        type_ += 1
    else:
        type_ = 8 + 16
    es.usermsg("create", "fade", "Fade")
    es.usermsg("write", "short", "fade", fadetime * 1000)
    es.usermsg("write", "short", "fade", totaltime * 1000)
    es.usermsg("write", "short", "fade", type_)
    es.usermsg("write", "byte", "fade", r)
    es.usermsg("write", "byte", "fade", g)
    es.usermsg("write", "byte", "fade", b)
    es.usermsg("write", "byte", "fade", a)
    es.usermsg("send", "fade", users)
    es.usermsg("delete", "fade")