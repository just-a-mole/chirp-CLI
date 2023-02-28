import sqlite3

class App:
    def __init__(self):
        self.mConnection = sqlite3.connect("app.db")
        self.mCursor = self.mConnection.cursor()

    #create
    def createUser(self, email, password, first_name):
        data = [first_name]
        self.mCursor.execute("INSERT INTO users (name) VALUES (?)",data)
        self.mConnection.commit()
        user_id = self.getUserFromName(first_name)
        data = [user_id, password, email]
        self.mCursor.execute("INSERT INTO credentials (user_id, password, email) VALUES (?,?,?)",data)
        self.mConnection.commit()

    def createFriendPost(self, user_id, post, title):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO friend_first_posts (user_id, post, title) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createEnemyPost(self, user_id, post, title):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO enemy_first_posts (user_id, post, title) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def addFriend(self, user_id, friend_id,first):
        data = [user_id, friend_id, first]
        self.mCursor.execute("INSERT INTO friends (user_id, friend_id, name ) VALUES (?,?,?)",data)
        self.mConnection.commit()

    def addEnemy(self,user_id, enemy_id, first_name):
        data = [user_id, enemy_id, first_name]
        self.mCursor.execute("INSERT INTO enemies (user_id,enemy_id,name) VALUES (?,?,?)",data)
        self.mConnection.commit()

    #get
    def getUserFromEmail(self, email, password):
        data = [email, password]
        item = self.mCursor.execute("SELECT user_id FROM credentials WHERE email = ? AND password = ?",data)
        try:
            return item.fetchone()[0]
        except TypeError:
            return None

    def getUserFromName(self, first_name):
        data = [first_name]
        item = self.mCursor.execute("SELECT id FROM users WHERE name = ?",data)
        return item.fetchone()[0]

    def getFriends(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT u.name "+
                                "FROM friends AS f "+
                                "JOIN users AS u ON f.friend_id = u.id "+
                                "WHERE f.user_id = ? ")
        return self.mCursor.fetchall()

    def getEnemies(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT u.name "+
                                "FROM enemies AS e "+
                                "JOIN users AS u ON e.enemy_id= u.id "+
                                "WHERE e.user_id = ? ")
        return self.mCursor.fetchall()

