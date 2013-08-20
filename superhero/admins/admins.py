import es
import playerlib
import popuplib
import psyco
import langlib
import random
psyco.full()
from collections import defaultdict
from sqlite3 import connect
from path import path
addonpath = path(__file__).dirname()
connection = connect(addonpath.joinpath('../Userdata/xp.db')) # Connect to database
cursor = connection.cursor() # Cursor to execute commands
superhero = es.import_addon('superhero')
sh_admins = []
popup_language = str(es.ServerVar('popup_language'))
admin_msg = langlib.Strings(es.getAddonPath("superhero") + "/languages/admin_msg.ini")
admin_popup = langlib.Strings(es.getAddonPath("superhero") + "/languages/admin_popup.ini")
tokens = {}
manage_user = defaultdict(int)

def load():
    print "[SH] Admins loading..."
    path = es.getAddonPath("superhero/admins/adminlist.txt")
    for line in open(path):
        line = str(line).rstrip()
        if line != '0':
            if line != "":
                if not '//' in line:
                    sh_admins.append(line)
                    print "[SH] %s is now a Superhero Admin" % line 
    es.dbgmsg(0, "[SH] Admins Loaded")   
    if not es.exists('saycommand', '/sh_admin'):
        es.regsaycmd('/sh_admin', 'superhero/admins/sh_admin')
       

def sh_admin():
    userid = str(es.getcmduserid())
    steamid = str(es.getplayersteamid(userid))
    if steamid in sh_admins:
        ##### Build Admin Menu ####
        player_list = popuplib.easymenu('player_list',None,player_list_selection)
        player_list.settitle(admin_popup('admin_player_list_title',lang=popup_language))
        PlayerList = playerlib.getPlayerList('#all,#all')
        counter = 0
        
        for player in PlayerList:
            player_list.addoption(player,(str(player.name)))
            
        popuplib.send('player_list',userid)
        
    else:
        es.tell(userid,'#multi',admin_msg('admin_not',lang=popup_language))

def player_list_selection(userid,player,popup):
    if es.exists('userid',player.userid):
        manage_user[str(userid)] = player.userid
        pid, plevel, pxp = cursor.execute('SELECT id, level, xp FROM users WHERE id=?', (superhero.getID(manage_user[str(userid)]),)).fetchone()
        player_manage = popuplib.easymenu('player_manage','choice',player_manage_selection)
        player_manage.settitle(player.name)
        player_manage.setdescription('LvL '+str(plevel)+' - XP '+str(pxp))
        player_manage.addoption('clear',admin_popup('admin_clear',lang=popup_language))
        player_manage.addoption('give_level',admin_popup('admin_givelevel',lang=popup_language))
        player_manage.addoption('remove_level',admin_popup('admin_remove',lang=popup_language))
        player_manage.addoption('give_50xp',admin_popup('admin_give50',lang=popup_language))
        player_manage.addoption('give_200xp',admin_popup('admin_give200',lang=popup_language))
        popuplib.send('player_manage',userid)
    else:
        es.tell(userid,'#multi',admin_msg('admin_notexist',lang=popup_language))

def player_manage_selection(userid,choice,popup):
    choice = str(choice)
    player = playerlib.getPlayer(manage_user[str(userid)])
    uid = str(player.userid)
    if es.exists('userid',player.userid):
        if choice == 'clear':
            cursor.execute('UPDATE users SET unspent=\'0\', level=\'0\', xp=\'0\', heroes=\'0\', power1=\'0\', power2=\'0\', power3=\'0\' WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
            es.playsound(uid, 'items/gift_drop.wav', 1.0)
            es.tell(uid,'#multi',admin_msg('admin_cleared',lang=popup_language))
            es.server.queuecmd('es_xsexec %s say /showxp' % uid)
            connection.commit()
            
        if choice == 'give_level':
            cursor.execute('UPDATE users SET level=(level + 1), unspent=(unspent + 1) WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
            es.playsound(uid, 'ambient/tones/elev1.wav', 1.0)
            es.tell(uid,'#multi',admin_msg('admin_granted',lang=popup_language))
            es.server.queuecmd('es_xsexec %s say /showxp' % uid)
            connection.commit()
            
        if choice == 'remove_level':
            pid, plevel, pxp, punspent, pheroes, ppower1, ppower2, ppower3 = cursor.execute('SELECT id, level, xp, unspent, heroes, power1, power2, power3 FROM users WHERE id=?', (superhero.getID(manage_user[str(uid)]),)).fetchone()
            if int(plevel) > 0:
                cursor.execute('UPDATE users SET level=(level - 1) WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
                connection.commit()
                es.playsound(uid, 'buttons/weapon_cant_buy.wav', 1.0)
                if int(punspent) > 0:
                    cursor.execute('UPDATE users SET unspent=(unspent - 1) WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
                else:
                    heroes = str(pheroes).split(',')
                    leng = int(len(heroes))
     
                    try:
                        rand = int(random.randint(0,leng-1))
                        hero = str(heroes[rand])
                        if hero != '0':
                            heroes.remove(hero)
                            if str(ppower1) == hero:
                                cursor.execute('UPDATE users SET power1=\'0\' WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
                                connection.commit()
                            if str(ppower2) == hero:
                                cursor.execute('UPDATE users SET power2=\'0\' WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
                                connection.commit()
                            if str(ppower3) == hero:
                                cursor.execute('UPDATE users SET power3=\'0\' WHERE id=?', (superhero.getID(manage_user[str(uid)]),))
                                connection.commit()
                            
                    except:
                        None
                            
                    string = heroes[0]
                    for hero in heroes:
                        if not hero in string:
                            string = string+','+str(hero)
                    cursor.execute('UPDATE users SET heroes=? WHERE id=?', (string,superhero.getID(manage_user[str(uid)])))
                    connection.commit()
                es.tell(uid,'#multi',admin_msg('admin_removed',lang=popup_language))
                es.server.queuecmd('es_xsexec %s say /showxp' % uid)
            else:
                es.tell(userid,'#multi',admin_msg('admin_already',lang=popup_language))
                
        if choice == 'give_50xp':
            superhero.sh_givexp(uid,50,admin_msg('admin_givexp',lang=popup_language))
            es.playsound(uid, 'items/itempickup.wav', 1.0)
            connection.commit()
        if choice == 'give_200xp':
            superhero.sh_givexp(uid,200,admin_msg('admin_givexp',lang=popup_language))
            es.playsound(uid, 'items/itempickup.wav', 1.0)
            connection.commit() # Commit changes to table
    es.server.queuecmd('es_xsexec %s say /sh_admin' % userid)
