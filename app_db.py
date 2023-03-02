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
                self.addFriend(user_id,friends[i][0])
            return True
        except TypeError:
            return False


    def createUser(self, email, password, name):
        try:
            x = self.mCursor.execute("SELECT MAX(id) FROM users")
            user_id = x.fetchone()[0]
            user_id += 1
        except:
            user_id = 1
        data = [user_id,name]
        self.mCursor.execute("INSERT INTO users (id, name) VALUES (?,?)",data)
        self.mConnection.commit()
        data = [user_id, password, email]
        self.mCursor.execute("INSERT INTO credentials (user_id, password, email) VALUES (?,?,?)",data)
        self.mConnection.commit()

    def createFriendPost(self, user_id, post, title):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO friend_posts (user_id, post, title, time) VALUES(?,?,?,TIME('now'))",data)
        self.mConnection.commit()
        return True

    def createEnemyPost(self, user_id, post, title):
        data = [user_id,post,title]
        self.mCursor.execute("INSERT INTO enemy_posts (user_id, post, title,time) VALUES(?,?,?,TIME('now'))",data)
        self.mConnection.commit()

    def addFriend(self, user_id, friend_id):
        data = [user_id, friend_id]
        self.mCursor.execute("INSERT INTO friends (user_id, friend_id ) VALUES (?,?)",data)
        self.mConnection.commit()

    def makeEnemy(self, name, ID):
        data = [ID]
        self.mCursor.execute(""" SELECT users.id
                                FROM users 
                                WHERE users.name IN(
                                    SELECT users.name
                                    FROM users
                                    WHERE users.id = ?
                                )""", data)
        friends = self.mCursor.fetchall()
        try:
            for i in range(len(friends)):
                data = [name, friends[i][0]]
                self.mCursor.execute("""SELECT users.id 
                                        FROM users 
                                        WHERE users.name = ? AND users.name NOT IN (
                                            SELECT name 
                                            FROM users 
                                            WHERE users.id = ? 
                                            LIMIT 1
                                            )""", data)
                users = self.mCursor.fetchall()
                try:
                    for j in range(len(users)):
                        print(users[j][0])
                        self.addEnemy(ID, users[j][0])
                except TypeError:
                    return None
        except TypeError:
            return None


    def addEnemy(self,user_id, enemy_id):
        data = [user_id, enemy_id]
        self.mCursor.execute("INSERT INTO enemies (user_id,enemy_id) VALUES (?,?)",data)
        self.mConnection.commit()

    #get
    def getUserFromEmail(self, email, password):
        data = [email, password]
        item = self.mCursor.execute("SELECT user_id FROM credentials WHERE email = ? AND password = ?",data)
        try:
            return item.fetchone()[0]
        except TypeError:
            return None

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

    def getFriendsFeed(self, user_id):
        data = [user_id]
        self.mCursor.execute("""SELECT friend_posts.post, friend_posts.title, friend_posts.time, credentials.email
                            FROM friends
                            JOIN friend_posts ON friends.friend_id = friend_posts.user_id
                            JOIN users ON users.id = friend_posts.user_id
                            JOIN credentials ON users.id = credentials.user_id
                            WHERE users.name IN (
                                SELECT users.name
                                FROM users
                                WHERE id = ?
                                LIMIT 1
                            )
                            GROUP BY friend_posts.post, friend_posts.title, friend_posts.time, credentials.email
                            ORDER BY friend_posts.time DESC""",data)
        return self.mCursor.fetchall()

    def getEnemiesFeed(self, user_id):
        self.mCursor.execute("SELECT * FROM enemy_posts ORDER BY enemy_posts.time DESC")
        return self.mCursor.fetchall()

