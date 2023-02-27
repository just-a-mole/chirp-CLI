import sqlite3

class App:
    def __init__(self):
        self.mConnection = sqlite3.connect("app.db")
        self.mCursor = self.mConnection.cursor()

    #create
    def createUser(self, email, password, first_name, last_name):
        data = [first_name, last_name]
        self.mCursor.execute("INSERT INTO users (first_name, last_name) VALUES (?,?)",data)
        self.mConnection.commit()
        user_id = self.getUserFromName(first_name, last_name)
        data = [user_id, first_name, last_name]
        self.mCursor.execute("INSERT INTO credentials (user_id, password, email) VALUES (?,?,?)",data)
        self.mConnection.commit()

    def createFirstFriendPost(self, user_id, post, title):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO friend_first_posts (user_id, post, title) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createFirstEnemyPost(self, user_id, post, title):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO enemy_first_posts (user_id, post, title) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createLastFriendPost(self,user_id, post, title ):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO last_friendly_posts (user_id, post, title) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createLastNotFriendlyPost(self,user_id, post, title ):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO last_not_friendly_posts (user_id, post, title) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def addFriend(self, user_id, friend_id,first, last):
        data = [user_id, friend_id, first, last]
        self.mCursor.execute("INSERT INTO friends (user_id, friend_id, first_name, last_name) VALUES (?,?,?,?)",data)
        self.mConnection.commit()

    def addEnemy(self,user_id, enemy_id, first_name, last_name):
        #lol copy and paste error, that I probs wont fix in schema
        #or fix later
        data = [user_id, enemy_id, first_name, last_name]
        self.mCursor.execute("INSERT INTO enemies (user_id,friend_id,first_name,last_name) VALUES (?,?,?,?)",data)
        self.mConnection.commit()

    #get
    def getUserFromEmail(self, email, password):
        data = [email, password]
        self.mCursor.execute("SELECT user_id FROM credentials WHERE email = ? AND password = ?",data)
        return self.mCursor.fetchone()[0]

    def getUserFromName(self, first_name, last_name):
        data = [first_name, last_name]
        self.mCursor.execute("SELECT id FROM users WHERE first_name = ? AND last_name=?",data)
        return self.mCursor.fetchone()[0]

    def getFirstFriends(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT u.first_name, u.last_name "+
                                "FROM friends AS f "+
                                "JOIN users AS u ON f.friend_id = u.id "+
                                "WHERE f.user_id = ? "+
                                "AND f.first = TRUE",data)
        return self.mCursor.fetchall()

    def getLastFriends(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT u.first_name, u.last_name "+
                                "FROM friends AS f "+
                                "JOIN users AS u ON f.friend_id = u.id "+
                                "WHERE f.user_id = ? "+
                                "AND f.last = TRUE",data)
        return self.mCursor.fetchall()

    def getFirstEnemies(self, user_id):
        data = [user_id]
        #IF YOU END UP CHANGING IT UPDATE IT HERE TOO
        self.mCursor.execute("SELECT u.first_name, u.last_name "+
                                "FROM enemies AS e "+
                                "JOIN users AS u ON e.friend_id = u.id "+
                                "WHERE e.user_id = ? "+
                                "AND e.first = TRUE",data)
        return self.mCursor.fetchall()

    def getLastEnemies(self, user_id):
        data = [user_id]
        #IF YOU END UP CHANGING IT UPDATE IT HERE TOO
        self.mCursor.execute("SELECT u.first_name, u.last_name "+
                                "FROM enemies AS e "+
                                "JOIN users AS u ON e.friend_id = u.id "+
                                "WHERE e.user_id = ? "+
                                "AND e.last = TRUE",data)
        return self.mCursor.fetchall()
