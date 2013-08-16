##########################################
# Superhero Mod                          #
#                                        #
# By: NeoSan  & Hashed                   #
#                                        #
# Visit http://forums.eventscripts.com   #
# for the latest mod                     #
#                                        #
# Date created: 11.27.2012               #
# First release: 03.07.2012              #
# Latest Version: 0.3.4.8                #
##########################################
import os
import cmdlib
import keyvalues
import playerlib
import cfglib
import langlib
import random
import usermsg
import es, sys, os.path, time
import traceback as tb_module
import popuplib
from sqlite3 import connect
from path import path
from array import array
addonpath = path(__file__).dirname()
connection = connect(addonpath.joinpath('Userdata/xp.db')) # Connect to database
cursor = connection.cursor() # Cursor to execute commands
other_msg = langlib.Strings(addonpath.joinpath('languages', 'other_msg.ini'))
Users = {}
info = es.AddonInfo()
info['name'] = "Superhero" 
info['version'] = "0.3.4.8"
info['author'] = "NeoSan" 
info['url'] = "http://forums.eventscripts.com"
info['basename'] = "superhero"
info['description'] = "Superhero Source Mod"
es.set('sh_version',info['version'])
config = cfglib.AddonCFG(es.getAddonPath("superhero") + "/superhero.cfg")
config.text("******************************")
config.text("       Superhero Config")
config.text("******************************")
herolist         = config.cvar("herolist","Agent Zero,Batman,Blade,Chucky,Daredevil,Dazzler,Dracula,Flash,General,Goku,HobGoblin,Invisible Man,Iron Man,Jubilee,Morph,Mystique,Nightcrawler,Poison Ivy,Predator,Punisher,Robin,Superman,Windwalker,Wolverine,Zeus",  "Heroes to load. Case Sensitive.")
xp_kill_min      = config.cvar("xp_kill_min",  10, "XP a Player receives each Kill min")
xp_kill_max      = config.cvar("xp_kill_max",  35, "XP a Player receives each Kill max")
xp_next_level    = config.cvar("xp_next_level", 100, "XP need to get a Level up")
xp_multi         = config.cvar("xp_multi",  1.1, "Increases the required XP again")
max_level        = config.cvar("max_level",   15, "What is the Max Level players can reach?")
buyxp            = config.cvar("buyxp",  1, "Buyxp command enabled? (0->off)")
xp_dollar        = config.cvar("xp_dollar",  0.015, "How many XP each $1?")
buyxp_players    = config.cvar("buyxp_players",  2, "How many Players are required for buyxp to be enabled?")
start_level      = config.cvar("start_level",  1, "Do players get a New Player Bonus?")
drop_alive       = config.cvar("drop_alive", 0, "Should Players be able to drop Heroes while alive?")
popup_language   = config.cvar("popup_language",  "en", "popup language A N D for all other messages")
config.write() # Writes the .cfg to file
cursor.execute(
    'CREATE TABLE IF NOT EXISTS users '
    '(id TEXT PRIMARY KEY,'
    'level INTEGER DEFAULT "0",'
    'xp INTEGER DEFAULT "0",'
    'unspent INTEGER DEFAULT "0",'
    'lastplayed REAL DEFAULT "0",'
    "heroes TEXT DEFAULT '0',"
    "power1 TEXT DEFAULT '0',"
    "power2 TEXT DEFAULT '0',"
    "power3 TEXT DEFAULT '0',"
    'connected INTEGER DEFAULT "0")')

def load():
    es.dbgmsg(0, "[SH] Loading.....") 
    config.execute() # Executes the .cfg to register changes   
    global popup_language
    popup_language = es.ServerVar('popup_language')
    global rounds_played
    rounds_played = 0
    es.server.queuecmd('es_xload superhero/heroes')
    es.server.queuecmd('es_xload superhero/admins')   
    # Create a group
    global heroes
    heroes = []
    ### Get the Strings the popup
    cmdlist_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/cmdlist_popup.ini")
    # Create popups
    global commandlist
    commandlist = popuplib.easymenu('commandlist','choice',commandlist_selection)
    commandlist.settitle('All Commands')   
    commandlist.addoption('help',cmdlist_popup('cmd_help',lang=str(popup_language))) # Done
    commandlist.addoption('herolist',cmdlist_popup('cmd_herolist',lang=str(popup_language))) # Done
    commandlist.addoption('playerinfo',cmdlist_popup('cmd_playerinfo',lang=str(popup_language)))
    commandlist.addoption('myheroes',cmdlist_popup('cmd_myheroes',lang=str(popup_language))) # Done
    commandlist.addoption('clearpowers',cmdlist_popup('cmd_clearpowers',lang=str(popup_language))) # Done
    commandlist.addoption('showmenu',cmdlist_popup('cmd_showmenu',lang=str(popup_language))) # Done
    commandlist.addoption('showxp',cmdlist_popup('cmd_showxp',lang=str(popup_language))) # Done
    commandlist.addoption(None,cmdlist_popup('cmd_drop',lang=str(popup_language))) # Done
    commandlist.addoption(None,cmdlist_popup('cmd_buyxp',lang=str(popup_language)))
    commandlist.addoption(None,cmdlist_popup('cmd_binding',lang=str(popup_language)))
    helpbox_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/helpbox_popup.ini")
    global helpbox
    helpbox = popuplib.create('helpbox')
    helpbox.addline(helpbox_popup('helpbox_1',lang=str(popup_language)))
    helpbox.addline(helpbox_popup('helpbox_2',lang=str(popup_language)))
    helpbox.addline('\n\n')
    helpbox.addline(helpbox_popup('helpbox_3',lang=str(popup_language)))
    helpbox.addline(helpbox_popup('helpbox_4',lang=str(popup_language)))
    helpbox.addline(helpbox_popup('helpbox_5',lang=str(popup_language)))
    helpbox.addline(helpbox_popup('helpbox_6',lang=str(popup_language)))
    # Saycommands register etc.
    cmdlib.registerSayCommand('/commandlist', 'superhero/commandlist', 'COMMANDLIST')
    cmdlib.registerSayCommand('/shmenu', 'superhero/commandlist', 'SHMENU')
    cmdlib.registerSayCommand('/sh', 'superhero/commandlist', 'SH')
    cmdlib.registerSayCommand('/help', 'superhero/superherohelp', 'HELP')
    cmdlib.registerSayCommand('/showmenu', 'superhero/showmenu', 'SHOWMENU')
    cmdlib.registerSayCommand('/drop', drop, 'DROP')
    cmdlib.registerSayCommand('/showxp', showxp, 'SHOWXP')
    cmdlib.registerSayCommand('/myheroes', 'superhero/myheroes', 'MYHEROES')
    cmdlib.registerSayCommand('hashero', 'superhero/hashero', 'HASHERO')
    cmdlib.registerSayCommand('/buyxp', buyxp, 'BUYXP')
    cmdlib.registerSayCommand('/herolist', 'superhero/herolist', 'HEROLIST')
    cmdlib.registerSayCommand('/clearpowers', 'superhero/clearpowers', 'CLEARPOWERS')
    cmdlib.registerSayCommand('/playerinfo', 'superhero/playerinfo', 'PLAYERINFO')
    cmdlib.registerClientCommand('+power1', power, "+power1")
    cmdlib.registerClientCommand('-power1', poweroff, "-power1")
    cmdlib.registerClientCommand('+power2', power, "+power2")
    cmdlib.registerClientCommand('-power2', poweroff, "-power2")
    cmdlib.registerClientCommand('+power3', power, "+power3")
    cmdlib.registerClientCommand('-power3', poweroff, "-power3")
    es.doblock('corelib/noisy_on')      
    print "[SH] Loading done."
    
def unload():
    print "[SH] Unloading..."
    es.unload('superhero/heroes')
    es.unload('superhero/admins')
    es.doblock('corelib/noisy_off')
    print "[SH] Unloading done."
    helpbox.delete()
    commandlist.delete()
    cmdlib.unregisterSayCommand('/myheroes')
    cmdlib.unregisterSayCommand('/showmenu')
    cmdlib.unregisterSayCommand('/showxp')
    cmdlib.unregisterSayCommand('/drop')
    cmdlib.unregisterSayCommand('/commandlist')
    cmdlib.unregisterSayCommand('/help')
    cmdlib.unregisterSayCommand('/buyxp')
    cmdlib.unregisterSayCommand('/clearpowers')
    cmdlib.unregisterSayCommand('/herolist')
    cmdlib.unregisterSayCommand('/playerinfo')
    cmdlib.unregisterSayCommand('/sh')
    cmdlib.unregisterSayCommand('/shmenu')
    cmdlib.unregisterClientCommand('+power1')
    cmdlib.unregisterClientCommand('+power2')
    cmdlib.unregisterClientCommand('+power3')
    cmdlib.unregisterClientCommand('-power1')
    cmdlib.unregisterClientCommand('-power2')
    cmdlib.unregisterClientCommand('-power3')
    connection.commit() # Commit changes to table
    connection.close() # Close our connection

def es_map_start(ev):
    es.ServerVar('sh_version', info['version'], 'Superhero Mod').makepublic()
    es.delayed(1,'es_xdoblock superhero/setVersion')
    es.server.cmd('es_xset sh_version %s' % info['version'])

def setVersion():
    es.ServerVar('sh_version', info['version'], 'Superhero Mod').makepublic()
    es.server.cmd('es_xset sh_version %s' % info['version'])
    es.delayed(5,'es_xdoblock superhero/setVersion')

def getID(userid):
    steamid = es.getplayersteamid(userid)
    return es.getplayername(userid) if steamid == 'BOT' else steamid

def player_activate(ev):
    steamid = getID(ev['userid'])
    cursor.execute('INSERT OR IGNORE INTO users (id) VALUES (?)', (steamid,))
    cursor.execute('UPDATE users SET connected=(connected + 1), lastplayed=? WHERE id=?', (time.time(), steamid))
    connection.commit() # Commit changes to table

def player_spawn(ev):
    userid = ev['userid']
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT':
        return
    player = playerlib.getPlayer(userid)
    if int(player.isdead) != 1:
        spawn_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/spawn_msg.ini')
        global popup_language
        pid, plevel = cursor.execute('SELECT id, level FROM users WHERE id=?', (steamid,)).fetchone()
        if pid != steamid:
            return
        es.tell(userid,'#multi',spawn_msg('spawn_cmdlist',lang=str(popup_language)))
        showxp(userid, None)
        es.tell(userid,'#multi',spawn_msg('spawn_latest',lang=str(popup_language)))
        if int(es.ServerVar('start_level')) > 0:
            if pid != steamid:
                return
            if int(plevel) == 0:
                es.tell(userid,'#multi',spawn_msg('spawn_startlevel',lang=str(popup_language)))
                sh_levelup(userid,int(es.ServerVar('start_level')))

def bomb_planted(ev):
    userid = ev['userid']
    xp = random.randint(5,35)
    xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
    global popup_language
    sh_givexp(userid, xp,xp_msg('xp_bombplanted',lang=str(popup_language)))
   
def bomb_exploded(ev):
    userid = ev['userid']
    xp = random.randint(5,35)
    xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
    global popup_language
    sh_givexp(userid, xp,xp_msg('xp_bombexploded',lang=str(popup_language)))

def bomb_defused(ev):
    userid = ev['userid']
    xp = random.randint(10,70)
    xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
    global popup_language
    sh_givexp(userid, xp,xp_msg('xp_bombdefused',lang=str(popup_language)))
    
def hostage_rescued(ev):
    userid = ev['userid']
    xp = random.randint(1,10)
    xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
    global popup_language
    sh_givexp(userid, xp,xp_msg('xp_hostage',lang=str(popup_language)))
    
def player_death(ev):
    userid = ev['userid']
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT': steamid = es.getplayername(userid)
    attacker = ev['attacker']
    weapon = ev['weapon']
    if weapon != 'world':
        if weapon != 'worldspawn':
            if userid != attacker:
                if ev['es_userteam'] != ev['es_attackerteam']: 
                    # Normal Player kill
                    xp_kill_min = es.ServerVar('xp_kill_min')
                    xp_kill_max = es.ServerVar('xp_kill_max')
                    xp = random.randint(xp_kill_min,xp_kill_max)
                    if attacker != '0':
                        if userid != '0':
                            pid, plevel = cursor.execute('SELECT id, level FROM users WHERE id=?', (steamid,)).fetchone()
                            if es.getplayersteamid(attacker) == 'BOT':
                                aid = getID(attacker)
                                alevel = '1'
                            else:
                                aid, alevel = cursor.execute('SELECT id, level FROM users WHERE id=?', (getID(attacker),)).fetchone()
                            level_dif = int(plevel) - int(alevel)
                            if alevel < 1:
                                xp = xp * float(es.ServerVar('xp_multi'))
                            if level_dif > 1:
                                xp = xp * level_dif * level_dif
                            elif level_dif == 1:
                                xp = xp * 2
                            if steamid == 'BOT':
                                return
                            xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
                            global popup_language
                            sh_givexp(attacker,xp,xp_msg('xp_kill',lang=str(popup_language)))
                   
def showxp(userid, args): # Cmdlib syntax
    # Get the player's level and XP
    plevel, pxp = cursor.execute('SELECT level, xp FROM users WHERE id=?', (getID(userid),)).fetchone()
    # XP required for next level
    xp_next_level = int(es.ServerVar('xp_next_level'))
    xp_multi = float(es.ServerVar('xp_multi'))
    next_level_xp = int((plevel*plevel)*xp_next_level*xp_multi)
    # Send text
    es.tell(userid, '#multi', '#green[SH] Level #lightgreen%s - %s / %s XP' % (plevel, int(pxp), int(next_level_xp)))

def sh_givexp(userid,amount,reason):
    userid = str(userid)
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT':
        return
    reason = str(reason)
    amount = int(amount)
    pid, plevel, pxp = cursor.execute('SELECT id, level, xp FROM users WHERE id=?', (steamid,)).fetchone()
    if plevel < int(es.ServerVar('max_level')):
        xp_next_level = int(es.ServerVar('xp_next_level'))
        xp_multi = float(es.ServerVar('xp_multi'))
        #xp_grenze = ((plevel + 1)*xp_next_level)*xp_multi
        xp_grenze = int((plevel*plevel)*xp_next_level*xp_multi)
        xp = amount + int(pxp)
        if int(xp) >= int(xp_grenze):
            # The player is above max xp
            cursor.execute('UPDATE users SET xp=? WHERE id=?', ((xp - xp_grenze), getID(userid)))
            sh_levelup(userid,1)
        else:
            cursor.execute('UPDATE users SET xp=? WHERE id=?', ((xp), getID(userid)))
        # Show the player's current level XP
        xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
        global popup_language
        tokens = {}
        tokens['amount'] = amount
        es.tell(userid,'#multi',xp_msg('xp_gain',tokens,lang=str(popup_language)),reason)
        showxp(userid, None)
        
def sh_levelup(userid,amount):
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT':
        return
    amount = int(amount)
    cursor.execute('UPDATE users SET level=(level + ?), unspent=(unspent + ?) WHERE id=?', (amount, amount, getID(userid)))
    es.playsound(userid, 'ambient/tones/elev1.wav', 1.0)
    #es.playsound(userid, 'plats/elevbell1.wav', 1.0)
    xp_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/xp_msg.ini')
    global popup_language
    es.tell(userid,'#multi',xp_msg('xp_levelup',lang=str(popup_language)))
    showxp(userid, None)

def map_end(ev):
    print "Map End...Saving Players..."
    connection.commit() # Commit changes to table
        
def round_end(ev):
    connection.commit()
    
def commandlist():
    userid = es.getcmduserid()
    #close_popups(userid)
    popuplib.send('commandlist',userid)
    
def commandlist_selection(userid,choice,name):
    userid = str(userid)
    cmdlist_msg = langlib.Strings(es.getAddonPath('superhero') + '/languages/cmdlist_msg.ini')
    global popup_language
    if choice != None:
        if str(choice) == 'disable':
            Users[userid]['cmdlist'] = 0
            es.tell(userid,'#multi',cmdlist_msg('cmdlist_disable',lang=str(popup_language)))
        elif str(choice) == 'enable':
            Users[userid]['cmdlist'] = 1
            es.tell(userid,'#multi',cmdlist_msg('cmdlist_enable',lang=str(popup_language)))
        else:
            popupname = '/'+str(choice)
            es.sexec(userid,'say',popupname)
    
def superherohelp():
    userid = es.getcmduserid()
    #close_popups(userid)
    popuplib.send('helpbox',userid)

def showmenu():
    userid = es.getcmduserid()
    userid = str(userid)
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT':
        return
    steamid = es.getplayersteamid(userid)
    global menuname
    menuname = "showmenu"+"_"+userid
    menuname = popuplib.easymenu(menuname, 'choice', showmenu_selection)
    showmenu_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/showmenu_popup.ini")
    global popup_language
    menuname.settitle(showmenu_popup('showmenu_title',lang=str(popup_language)))
    pid, plevel, punspent, pheroes, ppower1, ppower2, ppower3 = cursor.execute('SELECT id, level, unspent, heroes, power1, power2, power3 FROM users WHERE id=?', (steamid,)).fetchone()
    tokens = {}
    tokens['unspent'] = punspent
    menuname.setdescription(showmenu_popup('showmenu_desc',tokens,lang=str(popup_language)))
    herolist = str(es.ServerVar('herolist')).split(',')
    for hero in herolist:
        userheroes = pheroes.split(',')
        if not hero in userheroes:
            text = langlib.Strings(es.getAddonPath("superhero/heroes/"+hero+ "/strings.ini"))
            if int(text("req_level")) <= int(plevel):
                string = str(text("heroname"))+'    -   '+str(text("description",lang=str(popup_language)))
                menuname.addoption(hero,string)
    menuname = "showmenu"+"_"+userid
    #close_popups(userid)
    popuplib.send(menuname,userid)
    
def showmenu_selection(userid,choice,popupname):
    userid = str(userid)
    steamid = es.getplayersteamid(userid)
    showmenu_msg = langlib.Strings(es.getAddonPath("superhero/languages/showmenu_msg.ini"))
    global popup_language
    pid, plevel, punspent, pheroes, ppower1, ppower2, ppower3 = cursor.execute('SELECT id, level, unspent, heroes, power1, power2, power3 FROM users WHERE id=?', (steamid,)).fetchone()
    if int(punspent) != 0:
        text = langlib.Strings(es.getAddonPath("superhero/heroes/"+choice+ "/strings.ini"))
        req_level = int(text('req_level'))
        level = int(plevel)
        powerx = '0'
        powers = 0
        if int(text('power')) == 1:
            if str(ppower3) != '0':
                powers += 1
            else:
                powerx = 'power3'
            if str(ppower2) != '0':
                powers += 1
            else:
                powerx = 'power2'
            if str(ppower1) != '0':
                powers += 1
            else:
                powerx = 'power1'
            if powers == 3:
                es.tell(userid,'#multi',showmenu_msg('showmenu_allpowers',lang=str(popup_language)))
                return
        if req_level <= level:
            heroes = pheroes
            heroes = heroes.split(',')
            heroes.append(choice)
            string = heroes[0]
            for hero in heroes:
                if not hero in string:
                    string = string+','+str(hero)
            cursor.execute('UPDATE users SET heroes=?, unspent=(unspent - 1) WHERE id=?', (string, getID(userid)))
            pid, punspent, pheroes = cursor.execute('SELECT id, unspent, heroes FROM users WHERE id=?', (steamid,)).fetchone()
            #Users[userid][powerx] = choice # Might have to add powerx to DB
            tokens = {}
            tokens['choice'] = choice
            es.tell(userid,'#multi',showmenu_msg('showmenu_picked',tokens,lang=str(popup_language)))
            if powerx != '0':
                tokens = {}
                tokens['powerx'] = '+'+powerx
                es.tell(userid,showmenu_msg('showmenu_bind',tokens,lang=str(popup_language)))
            if int(punspent) > 0:
                showmenu()
            connection.commit() # Commit changes to table
    else:
        es.tell(userid,'#multi',showmenu_msg('showmenu_nopoints',lang=str(popup_language)))

def hasHero(userid,hero):
    if not es.exists('userid', userid):
        return
    steamid = es.getplayersteamid(userid)
    if steamid == 'BOT':
        return
    pheroes = cursor.execute('SELECT heroes FROM users WHERE id=?', (steamid,)).fetchone()
    if not pheroes:
        return
    hero = str(hero)
    heroes = []
    heroes = list(pheroes)
    heroes = heroes[0].split(',')
    if str(hero) in str(heroes):
        return True
    else:
        return

def drop(userid, args):
    userid = str(userid)
    steamid = es.getplayersteamid(userid)
    heroname = str(es.getargs())
    global popup_language
    drop_msg = langlib.Strings(es.getAddonPath("superhero/languages/drop_msg.ini"))
    if int(es.ServerVar('drop_alive')) == 0:
        if int(playerlib.getPlayer(userid).isdead) == 0:
            es.tell(userid,'#multi',drop_msg('drop_alive',lang=str(popup_language)))
            return
    pid, plevel, punspent, pheroes, ppower1, ppower2, ppower3 = cursor.execute('SELECT id, level, unspent, heroes, power1, power2, power3 FROM users WHERE id=?', (steamid,)).fetchone()
    heroes = pheroes
    heroes = heroes.split(',')
    text = langlib.Strings(es.getAddonPath("superhero/heroes/"+heroname+ "/strings.ini"))
    tokens = {}
    tokens['heroname'] = heroname
    if heroname in heroes:
        heroes.remove(heroname)
        string = heroes[0]
        for hero in heroes:
            if not hero in string:
                string = string+','+str(hero)
        cursor.execute('UPDATE users SET heroes=? WHERE id=?', (string,steamid))
        cursor.execute('UPDATE users SET unspent=(unspent + 1) WHERE id=?', (steamid,))
        if int(text('power')) == 1:
            if ppower1 == heroname:
                cursor.execute('UPDATE users SET power1=\'0\' WHERE id=?', (steamid,))
            if ppower2 == heroname:
                cursor.execute('UPDATE users SET power2=\'0\' WHERE id=?', (steamid,))
            if ppower3 == heroname:
                cursor.execute('UPDATE users SET power3=\'0\' WHERE id=?', (steamid,))
                
        es.tell(userid,'#multi',drop_msg('drop_suc',tokens,lang=str(popup_language)))
    else:
        es.tell(userid,'#multi',drop_msg('drop_not',tokens,lang=str(popup_language)))      
        
def myheroes():
    userid = str(es.getcmduserid())
    steamid = es.getplayersteamid(userid)
    pid, pheroes, ppower1, ppower2, ppower3 = cursor.execute('SELECT id, heroes, power1, power2, power3 FROM users WHERE id=?', (steamid,)).fetchone()
    heroes = pheroes
    heroes = heroes.split(',')
    menuname = "myheroes"+"_"+userid
    menuname = popuplib.easymenu(menuname,None, myheroes_selection)
    myheroes_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/myheroes_popup.ini")
    global popup_language
    menuname.settitle(myheroes_popup('myheroes_title',lang=str(popup_language)))
    menuname.setdescription(myheroes_popup('myheroes_desc',lang=str(popup_language)))
    for hero in heroes:
        if hero != '0':
            if str(ppower1) == hero:
                menuname.addoption(str(hero),str(hero)+' [+power1]')
            elif str(ppower2) == hero:
                menuname.addoption(str(hero),str(hero)+' [+power2]')
            elif str(ppower3) == hero:
                menuname.addoption(str(hero),str(hero)+' [+power3]')
            else:
                menuname.addoption(str(hero),hero)
    menuname = "myheroes"+"_"+userid
    #close_popups(userid)
    popuplib.send(menuname,userid)
    
def myheroes_selection(userid,heroname,popupname):
    userid = str(userid)
    es.server.cmd('es_sexec %s say /drop %s' % (userid,heroname))
    
def herolist():
    userid = str(es.getcmduserid())
    heroes = str(es.ServerVar('herolist'))
    heroes = heroes.split(',')
    herolist = popuplib.easymenu('herolist',None,None)
    herolist_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/herolist_popup.ini")
    global popup_language
    herolist.settitle(herolist_popup("herolist_title",lang=str(popup_language)))
    for hero in heroes:
        text = langlib.Strings(es.getAddonPath("superhero/heroes/"+hero+ "/strings.ini"))
        string = str(text("heroname"))+'    -   '+str(text("description",lang=str(popup_language)))
        herolist.addoption(None,string)
    #close_popups(userid)
    popuplib.send('herolist',userid)
    
def clearpowers():
    userid = str(es.getcmduserid())
    steamid = es.getplayersteamid(userid)
    global popup_language
    drop_msg = langlib.Strings(es.getAddonPath("superhero/languages/drop_msg.ini"))
    if int(es.ServerVar('drop_alive')) == 0:
        if int(playerlib.getPlayer(userid).isdead) == 0:
            es.tell(userid,'#multi',drop_msg('drop_alive',lang=str(popup_language)))
            return
    pid, punspent, pheroes, ppower1, ppower2, ppower3 = cursor.execute('SELECT id, unspent, heroes, power1, power2, power3 FROM users WHERE id=?', (steamid,)).fetchone()
    heroes = pheroes
    heroes = heroes.split(',')
    counter = 0
    for hero in heroes:
        if hero != '0':
            cursor.execute('UPDATE users SET unspent=(unspent + 1) WHERE id=?', (steamid,))
            if ppower1 == hero:
                cursor.execute('UPDATE users SET power1=\'0\' WHERE id=?', (steamid,))
            if ppower2 == hero:
                cursor.execute('UPDATE users SET power2=\'0\' WHERE id=?', (steamid,))
            if ppower3 == hero:
                cursor.execute('UPDATE users SET power3=\'0\' WHERE id=?', (steamid,))
            counter += 1
    cursor.execute('UPDATE users SET heroes=\'0\' WHERE id=?', (steamid,))
    other_msg = langlib.Strings(es.getAddonPath("superhero") + "/languages/other_msg.ini")
    tokens = {}
    tokens['counter'] = counter
    es.tell(userid,'#multi',other_msg('other_cleared',tokens,lang=str(popup_language)))
 
def power(userid, args):
    powerx = str(es.getargv(0))
    powerx = powerx.split('+')
    powerx = str(powerx[1])
    userid = str(es.getcmduserid())
    if userid in users:
        users[userid]['powerx'] = powerx
        if str(users[userid][powerx]) != '0':
            es.server.queuecmd('es_xdoblock superhero/heroes/'+str(users[userid][powerx])+'/power')

def poweroff(userid, args):
    powerx = str(es.getargv(0))
    powerx = powerx.split('-')
    powerx = str(powerx[1])
    userid = str(es.getcmduserid())
    if userid in users:
        users[userid]['powerx'] = powerx
        if str(users[userid][powerx]) != '0':
            es.server.queuecmd('es_xdoblock superhero/heroes/'+str(users[userid][powerx])+'/poweroff')
                                     
def round_start(ev):
    global roundend
    roundend = 0
    playerinfo_list_build()
    connection.commit() # Commit changes to table
    
def playerinfo_list_build():
    # Create and update player info
    playerinfo_list = popuplib.easymenu('playerinfo_list',None,playerinfo_list_selection)
    playerinfo_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/playerinfo_popup.ini")
    global popup_language
    playerinfo_list.settitle(playerinfo_popup('playerinfo_title',lang=str(popup_language)))
    PlayerList = playerlib.getPlayerList('#all,#all')
    counter = 0 
    for player in PlayerList:
        steamid = getID(player.userid)
        plevel = cursor.execute('SELECT level FROM users WHERE id=?', (steamid,)).fetchone()
        if plevel:
            playerinfo_list.addoption(player,(str(player.name)+' [Lvl '+str(plevel[0])+']'))
            counter += 1     
    if counter == 0:
        playerinfo_list.addoption(None,playerinfo_popup('playerinfo_update',lang=str(popup_language)))
          
def playerinfo():
    userid = es.getcmduserid()
    #close_popups(userid)
    popuplib.send('playerinfo_list',userid)
    
def playerinfo_list_selection(userid,choice,popup):
    steamid = getID(choice.userid)
    pheroes = cursor.execute('SELECT heroes FROM users WHERE id=?', (steamid,)).fetchone()
    if pheroes:
        id = choice.userid
        playerinfo = popuplib.create('playerinfo')
        playerinfo.addline('-> 1.'+str(es.getplayername(id)))
        playerinfo.addline('---------')
        heroes = []
        heroes = list(pheroes)
        heroes = heroes[0].split(',')
        counter = 0
        for hero in heroes:
            hero = str(hero)
            if hero != '0':
                counter += 1
                playerinfo.addline(str(counter)+' - '+hero)
        if counter == 0:
            playerinfo_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/playerinfo_popup.ini")
            global popup_language
            playerinfo.addline(playerinfo_popup('playerinfo_noheroes',lang=str(popup_language)))
        playerinfo.addline('---------')
        playerinfo.addline('-> 2.Back')
        playerinfo.menuselect = playerinfo_selection
        #close_popups(userid)
        popuplib.send('playerinfo',userid)

def playerinfo_selection(userid, choice, popupid):
    if str(choice) != '10':
        #close_popups(userid)
        popuplib.send('playerinfo_list',userid)
   
def buyxp(userid, args):
    userid = str(es.getcmduserid())
    buyxp_msg = langlib.Strings(es.getAddonPath("superhero") + "/languages/buyxp_msg.ini")
    global popup_language
    tokens = {}
    if int(es.ServerVar('buyxp')) != 0:
        playerList = playerlib.getPlayerList('#human,#all')
        if len(playerList) >= int(es.ServerVar('buyxp_players')):
            amount = es.getargs()
            if amount != None:
                player = playerlib.getPlayer(userid)
                cash = int(player.getCash())
                if str(amount) == 'all':
                    xp = cash * float(es.ServerVar('xp_dollar'))
                    string = 'Used '+str(amount)+'$'
                    sh_givexp(userid,int(xp),string)
                    player.setCash(0)
                    return                  
                elif str(amount) == '#all':
                    xp = cash * float(es.ServerVar('xp_dollar'))
                    string = 'Used '+str(amount)+'$'
                    sh_givexp(userid,int(xp),string)
                    player.setCash(0)
                    return         
                amount = int(amount)
                if amount >= 100:
                    if amount <= cash:
                        xp = amount * float(es.ServerVar('xp_dollar'))
                        string = 'Used '+str(amount)+'$'
                        sh_givexp(userid,int(xp),string)
                        player.setCash(cash-amount)
                    else:
                        tokens['amount'] = amount
                        es.tell(userid,'#multi',buyxp_msg('buyxp_notamount',tokens,lang=str(popup_language)))
                else:
                    es.tell(userid,'#multi',buyxp_msg('buyxp_notenough',lang=str(popup_language)))
            else:
                es.tell(userid,'#multi',buyxp_msg('buyxp_none',lang=str(popup_language)))
        else:
            tokens['players'] = es.ServerVar('buyxp_players')
            es.tell(userid,'#multi',buyxp_msg('buyxp_players',tokens,lang=str(popup_language)))
    else:
        es.tell(userid,'#multi',buyxp_msg('buyxp_disabled',lang=str(popup_language)))
