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
                fight_id INTEGER, 
                name STRING, 
                player INTEGER,  
                hp INTEGER, 
                damage_taken INTEGER, 
                state STRING, 
                position STRING, 
                high_miss_ar INTEGER, 
                low_hit_ar INTEGER)''')
        self.conn.commit()

    def addCampaign(self):
        self.c.execute("INSERT INTO campaigns (id) VALUES (NULL)")
        self.conn.commit()
        return self.c.execute("SELECT (id) FROM campaigns ORDER BY id DESC LIMIT 1").fetchone()[0]

    def addFight(self, campaign_id):
        self.c.execute("INSERT INTO fights (campaign_id) VALUES ({0})".\
                       format(campaign_id))
        self.conn.commit()
        return self.c.execute("SELECT (id) FROM fights ORDER BY id DESC LIMIT 1").fetchone()[0]

    def addCharacter(self, fight_id, name, player, count = 1, hp = 0):
        for i in range(0, count):
            self.c.execute('''INSERT INTO characters (fight_id, name, player, hp, damage_done, damage_taken)
                              VALUES ({0}, '{1}', {2}, {3}, 0, 0)'''.\
                           format(fight_id, name + str(i), int(player), hp))
        self.conn.commit()