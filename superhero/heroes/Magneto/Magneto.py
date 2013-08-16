import es
import random
import playerlib
import gamethread
import weaponlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Magneto")

def player_hurt(ev):
	userid = str(ev['userid'])
	if superhero.hasHero(userid,'Magneto'):
		attacker = str(ev['attacker'])
		weapon = str(ev['weapon'])
		weapon = 'weapon_%s'%weapon
		dice = random.randint(1,4)
		if dice == 1:
			if not weapon in ['weapon_glock','weapon_usp','weapon_p228','weapon_fiveseven','weapon_deagle','weapon_elite','weapon_knife','weapon_flashbang','weapon_hegrenade','weapon_smokegrenade']:
				wep_remove(attacker)
				for wep in ['weapon_glock','weapon_usp','weapon_p228','weapon_fiveseven','weapon_deagle','weapon_elite']:
					es.sexec(attacker, 'use %s'%wep)
				if ev['health'] > 0:
					if ev['es_userweapon'] in ['weapon_glock','weapon_usp','weapon_p228','weapon_fiveseven','weapon_deagle','weapon_elite','weapon_knife','weapon_flashbang','weapon_hegrenade','weapon_smokegrenade']:
						es.give(userid, weapon)
						es.tell(userid, '#multi', '#green[SH]#lightgreen You have taken#green',ev['es_attackername'],'#lightgreenprimary weapon')
				es.tell(attacker, '#multi', '#green[SH]#lightgreen Magneto has taken your primary weapon')

def player_death(ev):
	userid = str(ev['userid'])
	if superhero.hasHero(userid,'Magneto'):
		gamethread.delayed(0.1, es.give, (userid, 'player_weaponstrip'))
		gamethread.delayed(0.1, es.server.es_fire, (userid, "player_weaponstrip", "Strip"))
        gamethread.delayed(0.1, es.server.es_fire, (userid, "player_weaponstrip", "Kill"))

def wep_remove(userid):
    if userid != '0':
        player = playerlib.getPlayer(userid)
        primary = player.getPrimary()
        if primary != 0:
            handle = es.getplayerhandle(userid)
            weapon = weaponlib.getWeapon(primary)
            for index in weapon.indexlist:
                if es.getindexprop(index, 'CBaseEntity.m_hOwnerEntity') == handle:
                    es.server.cmd('es_xremove %s' % index)