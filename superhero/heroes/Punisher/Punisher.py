import es
import weaponlib
import playerlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Punisher")
    
def weapon_fire(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Punisher'):
        player = playerlib.getPlayer(userid)
        weapon = weaponlib.getWeapon(ev['weapon'])
        ammo = int(player.getClip(ev['weapon']))
        clip = weapon['clip']
        if ammo == 0:
            player.setClip(ev['weapon'],clip)
