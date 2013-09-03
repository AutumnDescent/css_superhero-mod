import es
import playerlib
import effectlib
import gamethread
import random
import psyco
psyco.full()
superhero = es.import_addon('superhero')
global gusers
gusers = {}
delayname = 'sh_invman_%s'
INVIS_DELAY = 0.3

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Invisible Man")

def unload():
    gamethread.cancelDelayed(check_moving)

def es_map_start(ev):
    gamethread.cancelDelayed(check_moving)

def player_spawn(ev):
    global gusers
    userid = ev['userid']
    gusers[userid] = {}
    if not superhero.hasHero(userid,'Invisible Man'):
        return
    gamethread.cancelDelayed(delayname % ev['userid'])
    check_moving(userid)

def player_disconnect(ev):
    userid = ev['userid']
    gamethread.cancelDelayed(delayname % ev['userid'])

def selected():
    global gusers
    userid = es.getcmduserid()
    if not superhero.hasHero(userid,'Invisible Man'):
        return
    gusers[userid] = {}
    check_moving(userid)

def round_end(ev):
    gamethread.cancelDelayed(check_moving)
 
def player_footstep(ev):
    global gusers
    userid = ev['userid']
    if not superhero.hasHero(userid,'Invisible Man'):
        return
    player = playerlib.getPlayer(userid)
    r,g,b,a = player.getColor() 
    player.set("color", [r, g, b, 255])
    gusers[userid]['oldpos'] = es.getplayerlocation(userid)
    if a != 255:
        es.centertell(userid,"You are not cloaked anymore!")
            
def player_hurt(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid,'Invisible Man'):
        return
    player = playerlib.getPlayer(userid)
    r,g,b,a = player.getColor() 
    player.set("color", [r, g, b, 255])
    if a != 255:
        es.centertell(userid,"You are not cloaked anymore!")
            
def weapon_fire(ev):
    userid = ev['userid']
    if not superhero.hasHero(userid,'Invisible Man'):
        return
    player = playerlib.getPlayer(userid)
    r,g,b,a = player.getColor() 
    player.set("color", [r, g, b, 255])
    if a != 255:
        es.centertell(userid,"You are not cloaked anymore!")
    
def check_moving(userid):
    userid = str(userid)
    if not superhero.hasHero(userid,'Invisible Man'):
        return
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        if not 'oldpos' in gusers[userid]: gusers[userid]['oldpos'] = 0
        newpos = es.getplayerlocation(userid)
        oldpos = gusers[userid]['oldpos']
        if str(newpos) == str(oldpos):
            r,g,b,a = player.getColor() 
            if a >= 15:
                a -= 15
            invis = a
            invis = invis * 100 / 255
            invis = 100-invis
            es.centertell(userid,invis,'% Cloaked')
            player.set("color", [r, g, b, a])                       
        gusers[userid]['oldpos'] = newpos   
        gamethread.delayedname(INVIS_DELAY, delayname % player, check_moving, player)