import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()

    def createTables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS fights (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                campaign_id INTEGER)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                fight_id INTEGER, 
                name STRING, 
                player INTEGER,  
                current_hp INTEGER,
                max_hp INTEGER,
                state STRING, 
                position STRING,
                high_miss_ar INTEGER, 
                low_hit_ar INTEGER)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                fight_id INTEGER,
                source_id INTEGER,
                target_id INTEGER,
                attack_roll INTEGER,
                hit INTEGER,
                damage INTEGER)''')
        self.conn.commit()

    def addCampaign(self):
        self.c.execute("INSERT INTO campaigns (id) VALUES (NULL)")
        self.conn.commit()
        return self.c.lastrowid

    def addFight(self, campaign_id):
        self.c.execute("INSERT INTO fights (campaign_id) VALUES ({0})".\
                       format(campaign_id))
        self.conn.commit()
        return self.c.lastrowid

    def addCharacter(self, campaign_id, fight_id, name, player, current_hp, max_hp, count = 1):
        sqlString = '''INSERT INTO characters (campaign_id, fight_id, name, player, 
                       current_hp, max_hp, high_miss_ar, low_hit_ar)
                       VALUES ({0}, {1}, '{2}', {3}, {4}, {5}, 0, 0)'''
        if count > 1:
            for i in range(0, count):
                self.c.execute(sqlString.format(campaign_id, fight_id, name + ' ' + str(i), int(player),
                                                current_hp, max_hp))
        else:
            self.c.execute(sqlString.format(campaign_id, fight_id, name, int(player),
                                            current_hp, max_hp))
        self.conn.commit()

    def addAttack(self, campaign_id, fight_id, source_character_id, target_character_id,
                  attack_roll, hit, damage):
        self.c.execute('''INSERT INTO attacks (campaign_id, fight_id, source_id, 
                          target_id, attack_roll, hit, damage)
                          VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})'''. \
                       format(campaign_id, fight_id, source_character_id, target_character_id,
                              attack_roll, int(hit), damage))
        self.conn.commit()

    def getCharacter(self, name):
        return self.c.execute("SELECT id FROM characters WHERE name='{0}'".format(name)).fetchone()[0]

    def getCharacterDamageTaken(self, character_id):
        return self.c.execute('SELECT sum(damage) FROM attacks WHERE target_id={0}'.format(character_id)).fetchone()[0]

    def getCharacterDamageDone(self, character_id):
        return self.c.execute('SELECT sum(damage) FROM attacks WHERE source_id={0}'.format(character_id)).fetchone()[0]

    def countCharacterHits(self, character_id):
        return self.c.execute('SELECT count(*) FROM attacks WHERE source_id={0} AND hit=1'.format(character_id)).fetchone()[0]

    def countCharacterMisses(self, character_id):
        return self.c.execute('SELECT count(*) FROM attacks WHERE source_id={0} AND hit=0'.format(character_id)).fetchone()[0]

    def getFighters(self, fight_id):
        return self.c.execute('''SELECT id, name, player, current_hp, max_hp, state, position,
                              high_miss_ar, low_hit_ar
                              FROM characters WHERE fight_id={0} ORDER BY id ASC'''.\
                              format(fight_id)).fetchall()