import es
import os.path

def load():
    herolist = str(es.ServerVar('herolist')).split(',')
    counter = 0
    global heroes
    heroes = {}
    for hero in herolist:
        es.load('superhero/heroes/'+str(hero))
        counter += 1
    print "[SH] Loaded",counter,"Heroes"
        
def unload():
    herolist = str(es.ServerVar('herolist')).split(',')
    for hero in herolist:
        es.unload('superhero/heroes/'+str(hero))