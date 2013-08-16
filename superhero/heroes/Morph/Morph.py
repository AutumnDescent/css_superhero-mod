import es
import random
import playerlib
import time
superhero = es.import_addon('superhero')

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Morph")
    
def player_spawn(ev):
    userid = ev['userid']
    if es.exists('userid',userid):
        player = playerlib.getPlayer(userid)
        wcs_dead = player.isdead
        if wcs_dead != 1:
            if superhero.hasHero(userid,'Morph'):
                superhero.Users[userid]['morph_cool'] = int(time.time())
                superhero.Users[userid]['morph_model'] = ''
                superhero.Users[userid]['morph_box'] = 0 

def power():
    userid = str(es.getcmduserid())
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        powerx = str(superhero.Users[userid]['powerx'])
        if superhero.Users[userid][powerx] == 'Morph':
            if not 'morph_cool' in superhero.Users[userid]:
                superhero.Users[userid]['morph_cool'] = int(time.time()) + 3
            if not 'morph_model' in superhero.Users[userid]:
                superhero.Users[userid]['morph_model'] = ''
            if not 'morph_box' in superhero.Users[userid]:
                superhero.Users[userid]['morph_box'] = 0
            if int(time.time()) >= int(superhero.Users[userid]['morph_cool']):
                superhero.Users[userid]['morph_cool'] = int(time.time()) + 3
                dice = random.randint(1,4)
                if not bool(superhero.Users[userid]['morph_box']):
                    superhero.Users[userid]['morph_model'] = player.model
                    if dice == 1:
                        player.model = 'props/de_dust/stoneblock01a.mdl'
                        es.tell(userid,'#multi','#green[SH]#lightgreen Morph now looks like a #greenStoneblock')
                    elif dice == 2:
                        player.model = 'props/cs_office/sofa_chair.mdl'
                        es.tell(userid,'#multi','#green[SH]#lightgreen Morph now looks like a #greenSofa Chair')
                    elif dice == 3:
                        player.model = 'props/de_train/Barrel.mdl'
                        es.tell(userid,'#multi','#green[SH]#lightgreen Morph now looks like a #greenBarrel')
                    elif dice == 4:
                        player.model = 'props/cs_assault/BarrelWarning.mdl'
                        es.tell(userid,'#multi','#green[SH]#lightgreen Morph now looks like a #greenBarrel Warning')
                    superhero.Users[userid]['morph_box'] = 1
                elif bool(superhero.Users[userid]['morph_box']):
                    player.model = superhero.Users[userid]['morph_model']
                    es.tell(userid,'#multi','#green[SH]#lightgreen Morph now looks like a #greenHuman')
                    superhero.Users[userid]['morph_box'] = 0
            else:
                es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate Morph #green',int(superhero.Users[userid]['morph_cool'])-int(time.time()),'#lightgreenseconds left')