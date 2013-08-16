import es
import playerlib
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Agent Zero")
 
def weapon_fire(ev):
    userid = ev['userid']
    if superhero.hasHero(userid,'Agent Zero'):
        player = playerlib.getPlayer(userid)
        es.setplayerprop(userid, 'CCSPlayer.cslocaldata.m_iShotsFired', 0)
        es.setplayerprop(userid, 'CCSPlayer.baseclass.localdata.m_Local.m_vecPunchAngle', '0.000000,0.000000,0.000000')
