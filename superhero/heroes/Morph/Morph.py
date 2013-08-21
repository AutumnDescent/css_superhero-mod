import es
import random
import playerlib
import time
superhero = es.import_addon('superhero')
global gusers
gusers = {}

def load():
    es.dbgmsg(0, "[SH] Successfully loaded Morph")
    
def player_spawn(ev):
    userid = ev['userid']
    global gusers
    if superhero.hasHero(userid,'Morph'):
        gusers[userid] = {}
        gusers[userid]['morph_cool'] = int(time.time())
        gusers[userid]['morph_model'] = ''
        gusers[userid]['morph_box'] = 0 

def selected():
    global gusers
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    gusers[userid] = {}
    gusers[userid]['morph_cool'] = int(time.time())
    gusers[userid]['morph_model'] = ''
    gusers[userid]['morph_box'] = 0 

def power():
    global gusers
    userid = str(es.getcmduserid())
    if not es.exists('userid',userid):
        return
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        if not 'morph_cool' in gusers[userid]:
            gusers[userid]['morph_cool'] = int(time.time()) + 3
        if not 'morph_model' in gusers[userid]:
            gusers[userid]['morph_model'] = ''
        if not 'morph_box' in gusers[userid]:
            gusers[userid]['morph_box'] = 0
        if int(time.time()) >= int(gusers[userid]['morph_cool']):
            gusers[userid]['morph_cool'] = int(time.time()) + 3
            dice = random.randint(1,4)
            if not bool(gusers[userid]['morph_box']):
                gusers[userid]['morph_model'] = player.model
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
                gusers[userid]['morph_box'] = 1
            elif bool(gusers[userid]['morph_box']):
                player.model = gusers[userid]['morph_model']
                es.tell(userid,'#multi','#green[SH]#lightgreen Morph now looks like a #greenHuman')
                gusers[userid]['morph_box'] = 0
        else:
            es.tell(userid,'#multi','#green[SH]#lightgreen Cannot activate Morph #green',int(gusers[userid]['morph_cool'])-int(time.time()),'#lightgreenseconds left')
