from database import Database

d = Database();
d.createTables()
c = d.addCampaign()
f = d.addFight(c)
ct = d.addCharacter(f, 'testName', False, 5)