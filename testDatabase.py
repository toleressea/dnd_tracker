import os
from database import Database

try:
    os.remove('data.db')
except:
    pass

d = Database();
d.createTables()
c = d.addCampaign()
f = d.addFight(c)
d.addCharacter(c, f, 'Tol Eressea', True, 10, 10, 1)
ct = d.getCharacter('Tol Eressea')
d.addCharacter(c, f, 'Bad Guy', False, 0, 0, 5)
ctt = d.getCharacter('Bad Guy 2')
for i in range(0, 3):
    d.addAttack(c, f, ct, ctt, 20, True, 15)
for i in range(0, 7):
    d.addAttack(c, f, ct, ctt, 10, False, 0)
print d.getCharacterDamageTaken(ctt)
print d.getCharacterDamageDone(ct)
print d.countCharacterHits(ct)
print d.countCharacterMisses(ct)
fighters = d.getFighters(f)
s = ''
for ft in fighters:
    for i in range(0, 8):
        s += str(ft[i]).ljust(15)
    s += str(d.getCharacterDamageDone(ft[0])).ljust(15)
    s += str(d.getCharacterDamageTaken(ft[0])).ljust(15)
    hits = d.countCharacterHits(ft[0])
    misses = d.countCharacterMisses(ft[0])
    s += '{0}/{1}'.format(hits, misses).ljust(15)
    s += '\n'
print s