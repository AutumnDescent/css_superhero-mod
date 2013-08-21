import es

import playerlib

import gamethread

import popuplib

import weaponlib

import psyco

psyco.full()

superhero = es.import_addon('superhero')


def load():

    global bat_menu

    bat_menu = popuplib.easymenu('bat_menu', 'choice', bat_menu_selection)

    bat_menu.settitle('Pick a Weapon Category:') 
    bat_menu.addoption('rifles','Rifles')

    bat_menu.addoption('smg','SMG')

    global bat_menu_rifles

    bat_menu_rifles = popuplib.easymenu('bat_menu_rifles', 'choice', weapon_give)

    bat_menu_rifles.settitle('Pick a Weapon Category:')
    bat_menu_rifles.addoption('m4a1','M4A1')

    bat_menu_rifles.addoption('ak47','Ak47')

    bat_menu_rifles.addoption('sg552','Krieg')
    global bat_menu_smg

    bat_menu_smg = popuplib.easymenu('bat_menu_smg', 'choice', weapon_give)

    bat_menu_smg.settitle('Pick a Weapon Category:') 

    bat_menu_smg.addoption('tmp','Tmp')

    bat_menu_smg.addoption('mp5navy','MP5')

    bat_menu_smg.addoption('p90','P90')

    if not es.exists('saycommand', 'batmenu'):

        es.regsaycmd('batmenu', 'superhero/heroes/Batman/batmenu')

    print "[SH] Batman successfully loaded"

    

def unload():

    es.unregsaycmd('batmenu')

    bat_menu.delete()

    bat_menu_pistols.delete()

    bat_menu_smg.delete()

    bat_menu_rifles.delete()


def selected():

    userid = es.getcmduserid()

    if not superhero.hasHero(userid,'Batman'):

        return

    popuplib.send('bat_menu',userid)

    es.tell(userid,'#multi','#green[SH]#lightgreen Batman activated. Type #greenbatmenu #lightgreento pick Weapons')
    

def batmenu():

    userid = str(es.getcmduserid())

    if not superhero.hasHero(userid,'Batman'):

        return

    if popuplib.isqueued('bat_menu',userid):

        popuplib.close('bat_menu',userid)

    popuplib.send('bat_menu',userid)

    

def bat_menu_selection(userid,choice,popupname):

    userid = str(userid)

    choice = str(choice)

    menuname = 'bat_menu_'+choice

    popuplib.send(menuname,userid)

    

def bat_menu_pistols(userid,choice,popupname):

    userid = str(userid)

    choice = str(choice)

    weapon_give

    

def bat_menu_smg(userid,choice,popupname):

    userid = str(userid)

    choice = str(choice)

    

def bat_menu_rifles(userid,choice,popupname):

    userid = str(userid)

    choice = str(choice)

    

def weapon_give(userid,weapon,popupname):

    userid = str(userid)

    weapon = str(weapon)
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        batlist = 'tmp,mp5navy,p90,ak47,m4a1,sg552'

        if weapon in batlist:

            weapon_give = 'weapon_'+weapon

            primary = player.getPrimary()

            for x in xrange(7):

                handle = es.getplayerprop(userid, 'CBaseCombatCharacter.m_hMyWeapons.%03d' % x)

                if handle > 0:

                    index = es.getindexfromhandle(handle)

                    weapon = weaponlib.getWeapon(es.entitygetvalue(index, 'classname'))

                    # Loop through all usps to find the one belonging to the player

                    if weapon is not None and 'primary' in weapon.tags:

                        es.entitysetvalue(index, 'targetname', 'kill_me')

                        es.server.queuecmd('es_xfire %s kill_me kill'%userid)

            es.server.queuecmd('es_xgive %s %s'%(userid, weapon_give))

            if popuplib.isqueued('bat_menu', userid):

                popuplib.close('bat_menu', userid)

        else:

            es.tell(userid,'#multi','#green[SH] #lightgreenWeapon has already been picked once this round')

    

def player_spawn(ev):
    userid = ev['userid']

    if  not superhero.hasHero(userid,'Batman'):

        return

    player = playerlib.getPlayer(userid)

    if int(player.isdead) != 1:
        primary = player.getPrimary()

        es.tell(userid,'#multi','#green[SH]#lightgreen Batman activated. Type #greenbatmenu #lightgreento pick Weapons')

        if popuplib.isqueued('bat_menu',userid):

            popuplib.close('bat_menu',userid)
        if not primary:

            popuplib.send('bat_menu',userid)