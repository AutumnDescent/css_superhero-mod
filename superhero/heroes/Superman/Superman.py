import es
import playerlib
import gamethread
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Superman")
    es.addons.registerClientCommandFilter(shfilter)

def unload():
    es.addons.unregisterClientCommandFilter(shfilter)

def player_spawn(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Superman'):
        player = playerlib.getPlayer(userid)
        if not playerlib.getPlayer(userid).isdead:
            health = player.health
            player.health = health + 75
            armor = player.armor
            player.set("armor", "120")
    
def shfilter(userid, args):
    userid = str(userid) 
    if args[0].lower() == 'buy':
        if args[1].lower() == 'vesthelm':
            if superhero.hasHero(userid,'Superman'):
                es.tell(userid,'#multi','#green You already have armor!')
                return False 
    return True  
  
def player_jump(ev):
    userid = ev['userid']
    superhero = es.import_addon('superhero')
    if superhero.hasHero(userid,'Superman'): 
        es.server.queuecmd('es_xfire %s !self addoutput "gravity 0.6"' % ev['userid'])
    else:
        es.server.queuecmd('es_xfire %s !self addoutput "gravity 1"' % ev['userid'])
