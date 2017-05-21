import sqlite3

class Database():
    def __init__(self, logging):
        self.logging = logging
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.createTables()

    def log(self, msg):
        if self.logging:
            print "log: " + msg

    def createTables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name STRING)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS fights (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                campaign_id INTEGER)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                fight_id INTEGER, 
                name STRING, 
                is_player INTEGER,  
                current_hp INTEGER,
                max_hp INTEGER,
                state STRING, 
                position STRING)''')
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
        self.log("create tables...")
    
    def getLastTableRowId(self, table):
        return self.c.execute("SELECT id FROM {0} ORDER BY id DESC LIMIT 1".format(table)).fetchone()[0]

    def addCampaign(self, name=''):
        self.c.execute("INSERT INTO campaigns (name) VALUES ('{0}')".format(name))
        self.conn.commit()
        self.log("add campaign -- id: {0}, name: {1}".format(self.c.lastrowid, name))
        return self.c.lastrowid

    def getCampaign(self, name):
        return self.c.execute("SELECT id FROM campaigns WHERE name='{0}'".format(name)).fetchone()[0]

    def addFight(self, campaign_id):
        self.c.execute("INSERT INTO fights (campaign_id) VALUES ({0})".\
                       format(campaign_id))
        self.conn.commit()
        self.log("add fight -- id: {0}".format(self.c.lastrowid))
        return self.c.lastrowid

    def addCharacter(self, campaign_id, fight_id, name, is_player, current_hp, max_hp, count = 1):
        sqlString = '''INSERT INTO characters (campaign_id, fight_id, name, is_player, 
                       current_hp, max_hp, state, position)
                       VALUES ({0}, {1}, '{2}', {3}, {4}, {5}, '', '')'''
        if count > 1:
            for i in range(0, count):
                self.c.execute(sqlString.format(campaign_id, fight_id, name + ' ' + str(i), is_player,
                                                current_hp, max_hp))
        else:
            self.c.execute(sqlString.format(campaign_id, fight_id, name, is_player,
                                            current_hp, max_hp))
        self.conn.commit()
        self.log("add character")

    def getCharacter(self, fight_id, name):
        return self.c.execute("SELECT id FROM characters WHERE fight_id={0} AND name='{1}'".format(fight_id, name)).fetchone()[0]
        self.conn.commit()

    def addAttack(self, campaign_id, fight_id, source_character_id, target_character_id,
                  attack_roll, hit, damage):
        self.c.execute('''INSERT INTO attacks (campaign_id, fight_id, source_id, 
                          target_id, attack_roll, hit, damage)
                          VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6})'''. \
                       format(campaign_id, fight_id, source_character_id, target_character_id,
                              attack_roll, int(hit), damage))
        self.conn.commit()
        self.log("add attack")

    def getCharacterDamageTaken(self, character_id):
        result = self.c.execute('SELECT sum(damage) FROM attacks WHERE target_id={0}'.format(character_id)).fetchone()[0]
        if result:
            return result
        else:
            return 0

    def getCharacterDamageDone(self, character_id):
        result = self.c.execute('SELECT sum(damage) FROM attacks WHERE source_id={0}'.format(character_id)).fetchone()[0]
        if result:
            return result
        else:
            return 0

    def countCharacterHits(self, character_id):
        return self.c.execute('SELECT count(*) FROM attacks WHERE source_id={0} AND hit=1'.format(character_id)).fetchone()[0]

    def countCharacterMisses(self, character_id):
        return self.c.execute('SELECT count(*) FROM attacks WHERE source_id={0} AND hit=0'.format(character_id)).fetchone()[0]

    def getHighestMissAttackRoll(self, character_id):
        result = self.c.execute('''SELECT attack_roll FROM attacks WHERE hit=0 AND target_id={0} ORDER BY attack_roll DESC LIMIT 1'''.\
                                format(character_id)).fetchall()
        if len(result) > 0:
            return result[0][0]
        else:
            return 0

    def getLowestHitAttackRoll(self, character_id):
        result = self.c.execute('''SELECT attack_roll FROM attacks WHERE hit=1 AND target_id={0} ORDER BY attack_roll ASC LIMIT 1'''.\
                                format(character_id)).fetchall()
        if len(result) > 0:
            return result[0][0]
        else:
            return 0

    def getFighters(self, fight_id):
        return self.c.execute('''SELECT id, name, is_player, current_hp, max_hp, state, position
                              FROM characters WHERE fight_id={0} ORDER BY id ASC'''.\
                              format(fight_id)).fetchall()