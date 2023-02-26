import sqlite3

class App:
    def __init__(self):
        self.mConnection = sqlite3.connect("app.db")
        self.mCursor = self.mConnection.cursor()

    #create
    def createUser(self, email, password, first_name, last_name):
        data = [email, password, first_name, last_name]
        self.mCursor.execute("INSERT INTO users (email, password, first_name, last_name) VALUES (?,?,?,?)",data)
        self.mConnection.commit()

    def createFirstFriendlyPost(self, title, caption, person_id):
        data = [title, caption, person_id]
        self.mCursor.execute("INSERT INTO first_friendly_posts (title, caption, person_id) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createFirstNotFriendlyPost(self, title, caption, person_id):
        data = [title, caption, person_id]
        self.mCursor.execute("INSERT INTO first_not_friendly_posts (title, caption, person_id) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createLastFriendlyPost(self, title, caption, person_id):
        data = [title, caption, person_id]
        self.mCursor.execute("INSERT INTO last_friendly_posts (title, caption, person_id) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def createLastNotFriendlyPost(self, title, caption, person_id):
        data = [title, caption, person_id]
        self.mCursor.execute("INSERT INTO last_not_friendly_posts (title, caption, person_id) VALUES(?,?,?)",data)
        self.mConnection.commit()

    def addFirstFriends(self, last_name, person_id):
        data = [last_name, person_id]
        #add friends that have the same first name as you
        self.mCursor.execute("INSERT INTO first_friends (last_name, person_id) VALUES (?,?)",data)
        self.mConnection.commit()

    def addLastFriends(self, first_name, person_id):
        data = [first_name, person_id]
        #add friends that have the same last name as you
        self.mCursor.execute("INSERT INTO last_friends (first_name, person_id) VALUES (?,?)",data)
        self.mConnection.commit()
    
    def addLastEnemies(self, last_name, person_id):
        data = [last_name, person_id]
        self.mCursor.execute("INSERT INTO last_enemies (last_name, person_id) VALUES (?,?)",data)
        self.mConnection.commit()

    def addFirstEnemies(self,first_name, person_id):
        data = [first_name, person_id]
        self.mCursor.execute("INSERT INTO first_enemies (first_name, person_id) VALUES (?,?)",data)
        self.mConnection.commit()

    #find/select
    def findUser(self, email, password):
        data = [email, password]
        self.mCursor.execute("SELECT * FROM users WHERE email = ? AND password = ?",data)
        return self.mCursor.fetchone()
