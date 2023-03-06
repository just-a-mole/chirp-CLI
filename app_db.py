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

    def updateEnemies(self,user_id):
        data = [user_id, user_id]
        new_enemies = self.mCursor.execute("""
            SELECT DISTINCT e.enemy_id as friends_enemies_ids
            FROM friends f
            JOIN enemies e ON f.friend_id = e.user_id
            WHERE f.user_id = ?  
            AND e.enemy_id IS NOT NULL
            AND e.enemy_id NOT IN (SELECT enemy_id FROM enemies WHERE user_id = ?);
            """,data)
        try:
            new_enemies = new_enemies.fetchall()
            for i in range(len(new_enemies)):
                self.addEnemy(user_id,new_enemies[i][0])
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
        try:
            data = [user_id, password, email]
            self.mCursor.execute("INSERT INTO credentials (user_id, password, email) VALUES (?,?,?)",data)
            self.mConnection.commit()

            data = [user_id,name]
            self.mCursor.execute("INSERT INTO users (id, name) VALUES (?,?)",data)
            self.mConnection.commit()
            return True
        except:
            return False

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
        self.mCursor.execute("""SELECT u.id
                             FROM users AS u
                             WHERE u.name IN (SELECT name FROM users WHERE id = ? LIMIT 1)
                                """,data)
        users = self.mCursor.fetchall() 
        data = [name]
        self.mCursor.execute("""SELECT u.id
                             FROM users AS u
                             WHERE u.name = ?
                                """,data)
        enemies = self.mCursor.fetchall()
        ##Check if your enemy has an enemy already
        self.mCursor.execute("""
                                SELECT e.enemy_id
                                FROM enemies AS e
                                JOIN(
                                    SELECT u.id AS id
                                    FROM enemies AS e
                                    JOIN users AS u
                                    WHERE u.name = ?
                                    LIMIT 1
                                ) AS other_guy
                                ON e.user_id = other_guy.id
                                LIMIT 1
                                """,data)
        guy_id = self.mCursor.fetchone()

        ##
        try:
            if guy_id:
                print(guy_id, data) 
                e = guy_id[0]
                other_guy = self.getName(e)[0]
                print(name, "already has an enemy",other_guy,"try someone else")
                return True
            #check if you put your own name in lol
            friend = users[0][0]
            for i in range(len(enemies)):
                if friend in enemies[i]:
                    return False
            for i in range(len(users)):
                for j in range(len(enemies)):
                    self.addEnemy(users[i][0],enemies[j][0])
        except TypeError:
            print("Failed find ids")
            return True
        return True


        # data = [ID]
        # self.mCursor.execute(""" SELECT users.id
        #                         FROM users 
        #                         WHERE users.name IN(
        #                             SELECT users.name
        #                             FROM users
        #                             WHERE users.id = ?
        #                         )""", data)
        # friends = self.mCursor.fetchall()
        # try:
        #     for i in range(len(friends)):
        #         data = [name, friends[i][0]]
        #         self.mCursor.execute("""SELECT users.id 
        #                                 FROM users 
        #                                 WHERE users.name = ? AND users.name NOT IN (
        #                                     SELECT name 
        #                                     FROM users 
        #                                     WHERE users.id = ? 
        #                                     LIMIT 1
        #                                     )""", data)
        #         users = self.mCursor.fetchall()
        #         try:
        #             for j in range(len(users)):
        #                 print(users[j][0])
        #                 self.addEnemy(ID, users[j][0])
        #         except TypeError:
        #             return None
        # except TypeError:
        #     return None


    def addEnemy(self,user_id, enemy_id):
        data = [user_id, enemy_id]
        self.mCursor.execute("INSERT INTO enemies (user_id,enemy_id) VALUES (?,?)",data)
        self.mConnection.commit()
        data = [enemy_id, user_id]
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
        self.mCursor.execute("SELECT c.email "+
                                "FROM enemies AS e "+
                                "JOIN credentials AS c ON e.enemy_id= c.user_id "+
                                "WHERE e.user_id = ? ",data)
        return self.mCursor.fetchall()

    def getEnemy(self, user_id):
        data = [user_id]
        self.mCursor.execute(""" SELECT
                                    u.name
                                    FROM enemies AS e
                                    JOIN users AS u ON u.id = e.enemy_id
                                    WHERE e.user_id = ?
                                    LIMIT 1
                                    """,data)
        return self.mCursor.fetchone()

    def getName(self, user_id):
        data = [user_id]
        self.mCursor.execute("SELECT name FROM users WHERE id = ? LIMIT 1",data)
        return self.mCursor.fetchone()

    def getFriendsFeed(self, user_id):
        data = [user_id]
        self.mCursor.execute("""
            SELECT fp.post, fp.title, fp.time, c.email
            FROM friend_posts AS fp
            JOIN users AS u ON fp.user_id = u.id
            JOIN credentials AS c ON fp.user_id = c.user_id
            WHERE u.name IN (SELECT name FROM users WHERE id = ?);
            ORDER BY fp.time
                             """,data)
        #Chat failed us again!
        # self.mCursor.execute("""SELECT friend_posts.post, friend_posts.title, friend_posts.time, credentials.email
        #                     FROM friends
        #                     JOIN friend_posts ON friends.friend_id = friend_posts.user_id
        #                     JOIN users ON users.id = friend_posts.user_id
        #                     JOIN credentials ON users.id = credentials.user_id
        #                     WHERE users.name IN (
        #                         SELECT users.name
        #                         FROM users
        #                         WHERE id = ?
        #                         LIMIT 1
        #                     )
        #                     GROUP BY friend_posts.post, friend_posts.title, friend_posts.time, credentials.email
        #                     ORDER BY friend_posts.time DESC""",data)
        return self.mCursor.fetchall()

    def getEnemiesFeed(self, user_id):
        data = [user_id,user_id]
        self.mCursor.execute("""SELECT 
                                ep.post, 
                                ep.title, 
                                ep.time, 
                                c.email
                            FROM(
                               SELECT
                               u.id AS id
                               FROM users u
                               WHERE u.name IN(
                               SELECT u.name
                               from users u 
                               JOIN enemies e ON u.id = e.user_id
                               JOIN users enemy ON e.enemy_id = enemy.id 
                               WHERE u.name IN (Select u.name From users where id =?)
                               )
                               OR u.name IN(
                               SELECT enemy.name
                               from users u 
                               JOIN enemies e ON u.id = e.user_id
                               JOIN users enemy ON e.enemy_id = enemy.id 
                               WHERE u.name IN (Select u.name From users where id =?)
                               )
                               )as feed
                               JOIN credentials c ON c.user_id = feed.id
                               JOIN enemy_posts ep ON ep.user_id = feed.id
                                ORDER BY ep.time DESC""",data)
        return self.mCursor.fetchall()

#delete

    def removeAccounts(self, name):
        data = [name]
# cascade is not working
        self.mCursor.execute("""
                            DELETE FROM credentials WHERE user_id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()
        self.mCursor.execute("""
                            DELETE FROM friends WHERE user_id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()
        self.mCursor.execute("""
                            DELETE FROM enemy_posts WHERE user_id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()
        self.mCursor.execute("""
                            DELETE FROM enemies WHERE user_id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()
        self.mCursor.execute("""
                            DELETE FROM enemies WHERE enemy_id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()
        self.mCursor.execute("""
                            DELETE FROM friend_posts WHERE user_id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()
        self.mCursor.execute("""
                            DELETE FROM users WHERE id IN(
                                SELECT id FROM users
                                WHERE name = ?)""",data)
        self.mConnection.commit()

