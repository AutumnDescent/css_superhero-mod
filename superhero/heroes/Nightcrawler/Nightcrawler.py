import es
import playerlib
import usermsg
import time
import weaponlib
import gamethread
superhero = es.import_addon('superhero')
round_ended = 0
global gusers
gusers = {}
import psyco
psyco.full()

def load():
    es.set('sv_noclipspeed',1.0)
    es.dbgmsg(0, "[SH] Successfully loaded Nightcrawler")

def unload():
    gamethread.cancelDelayed("undo")

def round_end(ev):
    global round_ended
    round_ended = 1
    if not superhero.hasHero(ev['userid'],'Nightcrawler'):
        return
    gusers[userid] = {}
    gusers[ev['userid']]['on_ground'] = 0

def player_spawn(ev):
    userid = ev['userid']
    if not superhero.hasHero(ev['userid'],'Nightcrawler'):
        return
    gusers[userid] = {}
    gusers[userid]['crawl'] = 0
    gusers[ev['userid']]['nc_cooldown'] = int(time.time())

def selected():
    userid = es.getcmduserid()
    if not superhero.hasHero(userid,'Nightcrawler'):
        return
    gusers[userid] = {}
    gusers[userid]['crawl'] = 0
    gusers[userid]['nc_cooldown'] = int(time.time())

    
def power():
    userid = str(es.getcmduserid())
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        if int(time.time()) >= int(gusers[userid]['nc_cooldown']):
            es.server.queuecmd('es_xsetplayerprop %s "CBaseEntity.movetype" 8' % userid)
            if not 'speed' in gusers[userid]: 
                gusers[userid]['speed'] = 1.0
            player.set("speed", 1.0)
            gusers[userid]['nc_cooldown'] = int(time.time()) + 10
            es.centertell(userid,'Noclip activated, do not get Stuck!')
            es.tell(userid,'#multi','#green[SH]#lightgreen Nightcrawler is partially blinded. You now are aswell.')
            gusers[userid]['crawl'] = 1
            fade(userid, 1, 0.5, 2.8, 0, 0, 0, 254)
            speed_set(userid)
            #es.server.cmd('ezrestrict %s #all' % userid)
            #es.server.cmd('ezrestrict_removeidle #all')
            #es.server.cmd('ezunrestrict %s knife' % userid)
            gamethread.delayed(0.1, es.server.queuecmd, 'es_xgive %s weapon_knife' % userid)
            es.delayed(1,'es_centertell %s 6 seconds left...' % userid)
            es.delayed(2,'es_centertell %s 5 seconds left...' % userid)
            es.delayed(3,'es_centertell %s 4 seconds left...' % userid)
            es.delayed(4,'es_centertell %s 3 seconds left...' % userid)
            es.delayed(5,'es_centertell %s 2 seconds left...' % userid)
            es.delayed(6,'es_centertell %s 1 seconds left...' % userid)
            gamethread.delayed(7,undo,(player))
        else:
            es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate Nightcrawler #green',int(gusers[userid]['nc_cooldown'])-int(time.time()),'#lightgreenseconds left')

def speed_set(userid):
    userid = str(userid)
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        if gusers[userid]['crawl'] != 0:
            player.set("speed", 1.0)
            gamethread.delayed(0.2,speed_set,userid)
              
                    
def undo(player):
    userid = str(es.getcmduserid())
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        es.centertell(player.userid,'Noclip deactivated')
        gusers[str(player.userid)]['crawl'] = 0
        if not 'speed' in gusers[str(player.userid)]: 
            gusers[str(player.userid)]['speed'] = 1.0
        player.set("speed", float(gusers[str(player.userid)]['speed']))
        es.server.queuecmd('es_xsetplayerprop %s "CBaseEntity.movetype" 1' % player.userid)
        gusers[str(player.userid)]['nc_cooldown'] = int(time.time()) + 10
        gusers[str(player.userid)]['on_ground'] = 0
        #es.server.cmd('ezunrestrict %s #all' % player.userid)
        gamethread.delayed(0.5,check_stuck,(player))
    
def check_stuck(player):
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    global gusers
    on_ground = int(gusers[str(player.userid)]['on_ground'])
    if on_ground != 8:
        if player.onground != 1:
            es.centertell(player.userid,'You are not on the ground, probably stuck, will slay you soon!')
            gusers[str(player.userid)]['on_ground'] = on_ground + 1
            gamethread.delayed(0.5,check_stuck,(player))
        else:
            return
    else:
        es.server.queuecmd('damage %s 999 1024' % player.userid)
            
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