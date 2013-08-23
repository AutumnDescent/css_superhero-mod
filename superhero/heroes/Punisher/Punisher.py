import es
import weaponlib
import playerlib
superhero = es.import_addon('superhero')
from playerlib import getPlayer
from weaponlib import getWeapon

def weapon_fire(ev):
   userid = ev['userid']
   if not superhero.hasHero(userid, 'Punisher'):
      return
   weapon = getWeapon(ev['weapon'])
   if weapon is not None and weapon.slot in (1, 2):
      player = getPlayer(ev['userid'])
      if not player.getClip(weapon):
         player.setClip(weapon, weapon.clip)
