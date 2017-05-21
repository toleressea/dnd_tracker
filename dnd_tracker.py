import os
from database import Database

def printStatus():
    print "campaign_id: {0}, fight_id: {1}".format(cc, cf)

    s = ''
    for header in ["id", "name", "is_player", "current_hp", "max_hp", "state", "position",
                   "high_miss_ar", "low_hit_ar", "damage_done", "damage_taken",
                   "hits/misses", "hit_percent"]:
        s += header.ljust(15)
    print (s)

    s = ''
    fighters = d.getFighters(cf)
    for ft in fighters:
        for i in range(0, 7):
            s += str(ft[i]).ljust(15)
        s += str(d.getHighestMissAttackRoll(ft[0])).ljust(15)
        s += str(d.getLowestHitAttackRoll(ft[0])).ljust(15)
        s += str(d.getCharacterDamageDone(ft[0])).ljust(15)
        s += str(d.getCharacterDamageTaken(ft[0])).ljust(15)
        hits = d.countCharacterHits(ft[0])
        misses = d.countCharacterMisses(ft[0])
        s += '{0}/{1}'.format(hits, misses).ljust(15)
        try:
            s += '{0}'.format(format(hits/float(hits + misses), '.2f')).ljust(15)
        except:
            s += '0'.ljust(15)
        s += '\n'
    print s

d = Database(False);
try:
    cc = d.getLastTableRowId('campaigns')
    cf = d.getLastTableRowId('fights')
except:
    cc, cf = None, None

while True:
    printStatus()
    cmd = raw_input("> ").split(' ')

    if cmd[0] == 'add':
        if cmd[1] == 'campaign':
            if len(cmd) > 2:
                cc = d.addCampaign(cmd[2])
            else:
                cc = d.addCampaign()
        elif cmd[1] == 'fight':
            cf = d.addFight(cc)
        elif cmd[1] == 'char':
            d.addCharacter(cc,              # campaign_id
                           cf,              # fight_id
                           cmd[2],          # name
                           cmd[3],          # is_player
                           cmd[4],          # current_hp
                           cmd[5])          # max_hp
    elif cmd[0] == 'atk':
        d.addAttack(cc,                     # campaign_id
                    cf,                     # fight_id
                    d.getCharacter(cf, cmd[1]), # source_id
                    d.getCharacter(cf, cmd[2]), # target_id
                    cmd[3],                 # attack_roll
                    cmd[4],                 # hit
                    cmd[5])                 # damage
    elif cmd[0] == 'set':
        if cmd[1] == 'campaign':
            cc = d.getCampaign(cmd[2])
    elif cmd[0] == 'status':
        printStatus()

    elif cmd[0] == 'exit':
        break