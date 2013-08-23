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
    if superhero.hasHero(userid,'Invisible Man'):
        gamethread.cancelDelayed(check_moving)
        es.delayed(1,'es_xdoblock superhero/heroes/Invisible Man/check_moving')

def selected():
    global gusers
    userid = es.getcmduserid()
    if superhero.hasHero(userid,'Invisible Man'):
        gusers[userid] = {}
        es.delayed(1,'es_xdoblock superhero/heroes/Invisible Man/check_moving')

def round_end(ev):
    gamethread.cancelDelayed(check_moving)
 
def player_footstep(ev):
    global gusers
    userid = ev['userid']
    if superhero.hasHero(userid,'Invisible Man'):
        player = playerlib.getPlayer(userid)
        r,g,b,a = player.getColor() 
        player.set("color", [r, g, b, 255])
        gusers[userid]['oldpos'] = es.getplayerlocation(userid)
        if a != 255:
            es.centertell(userid,"You are not cloaked anymore!")
            
def player_hurt(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Invisible Man'):
        player = playerlib.getPlayer(userid)
        r,g,b,a = player.getColor() 
        player.set("color", [r, g, b, 255])
        gusers[userid]['oldpos'] = es.getplayerlocation(userid)
        if a != 255:
            es.centertell(userid,"You are not cloaked anymore!")
            
def weapon_fire(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Invisible Man'):
        player = playerlib.getPlayer(userid)
        r,g,b,a = player.getColor() 
        player.set("color", [r, g, b, 255])
        gusers[userid]['oldpos'] = es.getplayerlocation(userid)
        if a != 255:
            es.centertell(userid,"You are not cloaked anymore!")
    
def check_moving():
    global gusers
    for userid in gusers:
        if superhero.hasHero(userid,'Invisible Man'):   
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
    es.delayed(0.4,'es_xdoblock superhero/heroes/Invisible Man/check_moving')