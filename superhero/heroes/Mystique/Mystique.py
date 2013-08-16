import es
import playerlib
import time
import random
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Mystique")
 
def player_spawn(ev):
    userid = ev['userid']
    if es.exists('userid',userid):
        if superhero.hasHero(userid,'Mystique'):
            if not playerlib.getPlayer(userid).isdead:
                superhero.Users[userid]['my_cooldown'] = int(time.time())

def power():
	userid = str(es.getcmduserid())
	player = playerlib.getPlayer(userid)
	if int(player.isdead) != 1:
		powerx = str(superhero.Users[userid]['powerx'])
		if superhero.Users[userid][powerx] == 'Mystique':
			if not 'my_cooldown' in superhero.Users[userid]:
				superhero.Users[userid]['my_cooldown'] = int(time.time()) + 3
			if int(time.time()) >= int(superhero.Users[userid]['my_cooldown']):
				superhero.Users[userid]['my_cooldown'] = int(time.time()) + 3
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
				es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate Mystique #green',int(superhero.Users[userid]['my_cooldown'])-int(time.time()),'#lightgreenseconds left')