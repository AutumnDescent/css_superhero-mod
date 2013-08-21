import es
import random
import playerlib
import gamethread
superhero = es.import_addon('superhero')
global gct
global gcct
global gusers
    
def load():
    es.dbgmsg(0, "[SH] Successfully loaded General")

def unload():
    gamethread.cancelDelayed(GeneralHelp)
    
def round_end(ev):
    gamethread.cancelDelayed(GeneralHelp)

def round_start(ev):
    steamid = ev['es_steamid']
    if steamid == 'BOT':
        return
    global gct #T General count
    global gcct #CT General count 
    global gusers #General users
    gct = 0
    gcct = 0
    gusers = {}
    playerList = playerlib.getPlayerList('#alive')
    for ply in playerList:
        userid = ply.userid
        gusers[userid] = {}
        gusers[userid]['Gensupport'] = 0
        if not superhero.hasHero(userid,'General'):
            return
        if es.getplayerteam(userid) == 2:
            gct = gct + 1
        elif es.getplayerteam(userid) == 3:
            gcct = gcct + 1
                
def player_spawn(ev):
    global gct #T General count
    global gcct #CT General count 
    global gusers #General users
    gct = 0
    gcct = 0
    userid = ev['userid']
    if not superhero.hasHero(userid,'General'):
        return
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        gamethread.delayed(1, GeneralHelp, userid)
    
def player_hurt(ev):
    global gusers #General users
    userid = ev['userid']
    attacker = ev['attacker']
    steamid = ev['es_steamid']
    if steamid == 'BOT':
        return
    damage = int(ev['dmg_health'])
    weapon = ev['weapon']
    if userid != attacker:
        if not superhero.hasHero(attacker,'General'):
            return
        if weapon != 'point_hurt':
            if weapon:
                if 'Gensupport' in gusers[attacker]:
                    if gusers[attacker]['Gensupport']:
                        rand = random.randint(1,3)*gusers[attacker]['Gensupport']
                        es.server.queuecmd('damage %s %i 1024 %s' % (userid,rand,attacker))
            
def GeneralHelp(userid):
    team = es.getplayerteam(userid)
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT':
        return
    global gct #T General count
    global gcct #CT General count 
    global gusers #General users
    gusers[userid] = {}
    if team == 2:
        if gct:
            if gct == 1:
                gusers[userid]['Gensupport'] = 1
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGeneral in your team'%gct)
            elif gct == 2:
                gusers[userid]['Gensupport'] = 2
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gct)
            elif gct == 3:
                gusers[userid]['Gensupport'] = 4
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gct)
            elif gct > 3:
                gusers[userid]['Gensupport'] = 3
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gct)                    
    elif team == 3:
        if gcct:
            if gcct == 1:
                gusers[userid]['Gensupport'] = 1
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGeneral in your team'%gcct)
            elif gcct == 2:
                gusers[userid]['Gensupport'] = 2
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gcct)
            elif gcct == 3:
                gusers[userid]['Gensupport'] = 4
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gcct)
            elif gcct > 3:
                gusers[userid]['Gensupport'] = 3
                es.tell(userid, '#multi', '#green[SH]#lightgreen You feel stronger because you have #green%s #lightgreenGenerals in your team'%gcct)
