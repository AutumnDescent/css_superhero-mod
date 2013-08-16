import es
import random
import playerlib
import gamethread
superhero = es.import_addon('superhero')
global gct
global gcct
    
def load():
    es.dbgmsg(0, "[SH] Successfully loaded General")

def unload():
    gamethread.cancelDelayed(GeneralHelp)
    
def round_end(ev):
    gamethread.cancelDelayed(GeneralHelp)

def round_start(ev):
    global gct #T General count
    global gcct #CT General count 
    gct = 0
    gcct = 0
    for userid in superhero.Users:
        superhero.Users[userid]['Gensupport'] = 0
        if superhero.hasHero(userid,'General'):
            if es.getplayerteam(userid) == 2:
                gct = gct + 1
            elif es.getplayerteam(userid) == 3:
                gcct = gcct + 1
                
def player_spawn(ev):
    global gct #T General count
    global gcct #CT General count 
    gct = 0
    gcct = 0
    userid = ev['userid']
    if superhero.hasHero(userid,'General'):
        player = playerlib.getPlayer(userid)
        if not playerlib.getPlayer(userid).isdead:
            gamethread.delayed(1, GeneralHelp, userid)
    
def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    damage = int(ev['dmg_health'])
    weapon = ev['weapon']
    if userid != attacker:
        if weapon != 'point_hurt':
            if weapon:
                if 'Gensupport' in superhero.Users[attacker]:
                    if superhero.Users[attacker]['Gensupport']:
                        rand = random.randint(1,3)*superhero.Users[attacker]['Gensupport']
                        es.server.queuecmd('damage %s %i 1024 %s' % (userid,rand,attacker))
            
def GeneralHelp(userid):
    team = es.getplayerteam(userid)
    global gct #T General count
    global gcct #CT General count 
    if team == 2:
        if gct:
            if gct == 1:
                superhero.Users[userid]['Gensupport'] = 1
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGeneral in your team'%gct)
            elif gct == 2:
                superhero.Users[userid]['Gensupport'] = 2
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gct)
            elif gct == 3:
                superhero.Users[userid]['Gensupport'] = 4
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gct)
            elif gct > 3:
                superhero.Users[userid]['Gensupport'] = 3
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gct)                    
    elif team == 3:
        if gcct:
            if gcct == 1:
                superhero.Users[userid]['Gensupport'] = 1
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGeneral in your team'%gcct)
            elif gcct == 2:
                superhero.Users[userid]['Gensupport'] = 2
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gcct)
            elif gcct == 3:
                superhero.Users[userid]['Gensupport'] = 4
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gcct)
            elif gcct > 3:
                superhero.Users[userid]['Gensupport'] = 3
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gcct)