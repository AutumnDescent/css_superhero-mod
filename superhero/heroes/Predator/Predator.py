import es
import gamethread
import playerlib
import weaponlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Predator")

def player_spawn(ev):
    userid = int(ev['userid'])
    if not superhero.hasHero(userid, 'Predator'):
        return
    giveDeagle(userid)

def giveDeagle(userid):
   for x in xrange(7): # CSS players can have up to 7 weapons
      handle = es.getplayerprop(userid, 'CBaseCombatCharacter.m_hMyWeapons.%03d' % x)
      if handle > 0: # Is this a valid handle?
         index = es.getindexfromhandle(handle)
         weapon = weaponlib.getWeapon(es.entitygetvalue(index, 'classname'))
         # Is this a secondary weapon?
         if weapon is not None and 'secondary' in weapon.tags:
            # Do we already have the correct weapon?
            if weapon != 'weapon_deagle':
               # We'll use this name to remove the weapon
               es.entitysetvalue(index, 'targetname', 'kill_me')
               es.server.insertcmd('es_xfire %(userid)s kill_me Kill;' # Remove the weapon
                                   'es_xgive %(userid)s weapon_deagle' % # Give a deagle
                                   {'userid': userid})
            break # We found the player's secondary weapon so we're done
  
def player_hurt(ev):
    userid = ev['userid']
    attacker = ev['attacker']
    if not superhero.hasHero(attacker,'Predator'):
        return
    weapon = ev['weapon']
    if weapon == 'deagle':
        if userid != attacker:
            if ev['es_userteam'] != ev['es_attackerteam']: 
                es.server.queuecmd('damage %s 45 1024 %s' % (userid,attacker))
