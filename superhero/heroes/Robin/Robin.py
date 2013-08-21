import es
import gamethread
import playerlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Robin")

def player_spawn(ev):
    userid = ev['userid']
    if not es.exists('userid',userid):
        return
    player = playerlib.getPlayer(userid)
    if not playerlib.getPlayer(userid).isdead:
        if not superhero.hasHero(userid,'Robin'):
            return
        if player.he == 0:
	    gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s weapon_hegrenade'%userid)
	if player.fb == 0:
            gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s weapon_flashbang'%userid)
	    gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s weapon_flashbang'%userid)
	elif player.fb == 1:
	    gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s weapon_flashbang'%userid)
	if player.sg == 0:
	    gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s weapon_smokegrenade'%userid)
	if player.nightvision != 1:
	    gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s item_nvgs'%userid)
        playerteam = es.getplayerteam(userid)
        if playerteam == 3:
	    if player.defuser != 1:
		gamethread.delayed(0.01, es.server.queuecmd, 'es_xgive %s item_defuser'%userid)