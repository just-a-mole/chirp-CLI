import sqlite3

class App:
    def __init__(self):
        self.mConnection = sqlite3.connect("app.db")
        self.mCursor = self.mConnection.cursor()

    #create
    def updateFriends(self,user_id):
        data = [user_id, user_id, user_id]
        friends = self.mCursor.execute("SELECT u.id "+
                            "FROM users AS u "+
                            "WHERE u.name = (SELECT name FROM users WHERE id = ? "+
                            "AND u.id <> ? "+
                            "AND u.id NOT IN ( "+
                            "SELECT friend_id FROM friends WHERE user_id = ?) "+
                            ")",data)
        try:
            friends = friends.fetchall()
            for i in range(len(friends)):
                print(friends)
                self.addFriend(user_id,friends[i][0])
            return True
        except TypeError:
            return False


    def createUser(self, email, password, first_name):
        try:
            x = self.mCursor.execute("SELECT MAX(id) FROM users")
            user_id = x.fetchone()[0]
            user_id += 1
        except:
            user_id = 1
        data = [user_id,email]
        self.mCursor.execute("INSERT INTO users (id, name) VALUES (?,?)",data)
        self.mConnection.commit()
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

    def addFriend(self, user_id, friend_id):
        data = [user_id, friend_id]
        self.mCursor.execute("INSERT INTO friends (user_id, friend_id ) VALUES (?,?)",data)
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

    def getUserFromName(self, email):
        data = [email]
        item = self.mCursor.execute("SELECT email FROM credentials WHERE email = ?",data)
        return item.fetchone()[0]

    def getFriends(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT c.email "+
                                "FROM friends AS f "+
                                "JOIN credentials AS c ON f.friend_id = c.user_id "+
                                "WHERE f.user_id = ? ",data)
        return self.mCursor.fetchall()

    def getEnemies(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT u.name "+
                                "FROM enemies AS e "+
                                "JOIN users AS u ON e.enemy_id= u.id "+
                                "WHERE e.user_id = ? ",data)
        return self.mCursor.fetchall()

    # def viewEnemies(self):
    #     self.mCursor.execute("SELECT u.name")
