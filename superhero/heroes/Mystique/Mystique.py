import es
import playerlib
import time
import random
superhero = es.import_addon('superhero')
global gusers
gusers = {}

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Mystique")
 
def player_spawn(ev):
    userid = ev['userid']
    global gusers
    if not superhero.hasHero(userid,'Mystique'):
        return
    gusers[userid] = {}
    gusers[userid]['my_cooldown'] = int(time.time())

def selected():
    global gusers
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    gusers[userid] = {}
    gusers[userid]['my_cooldown'] = int(time.time())

def power():
    global gusers
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    for player in playerlib.getPlayerList('#alive'):
	if int(time.time()) >= int(gusers[userid]['my_cooldown']):
		gusers[userid]['my_cooldown'] = int(time.time()) + 3
		RandSkin = random.randint(1, 4)
		if es.getplayerteam(userid) == 2:
			if RandSkin == 1:
				player.model = 'player/ct_urban'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenCT Urban')
			elif RandSkin == 2:
				player.model = 'player/ct_gsg9'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenCT Gsg 9')
			elif RandSkin == 3:
				player.model = 'player/ct_sas'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenCT Sas')
			elif RandSkin == 4:
				player.model = 'player/ct_gign'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenCT Gign')
		elif es.getplayerteam(userid) == 3:
			if RandSkin == 1:
				player.model = 'player/t_phoenix'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenT Phoenix')
			elif RandSkin == 2:
				player.model = 'player/t_leet'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenT Leet')
			elif RandSkin == 3:
				player.model = 'player/t_arctic'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenT Arctic')
			elif RandSkin == 4:
				player.model = 'player/t_guerilla'
				es.tell(userid,'#multi','#green[SH]#lightgreen Mystique changes skin, now you look like #greenT Guerilla')
	else:
		es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate Mystique #green',int(gusers[userid]['my_cooldown'])-int(time.time()),'#lightgreenseconds left')