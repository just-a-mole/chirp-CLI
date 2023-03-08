import app_db
import random

def loginPage():
    print("Welcome to Chirp CLI!")
    print()
    print("Login [l]") 
    print("or")
    print("Sign-up [s]")
    answer = input()
    answer = getValidInput(answer, ["l", "s"])
    return answer

def getValidInput(INPUT,valid):
    if INPUT in valid:
        return INPUT
    else:
        while True:
            print("That is not a valid option! Try again.")
            print("OPTIONS: ",valid)
            INPUT = input()
            if INPUT in valid:
                return INPUT

def signUp(db):
    print("by signing up understand we will store your password as plain text.")
    print()
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    if db.createUser(email, password, name.lower().strip()):
        return db.getUserFromEmail(email,password)
    return

def login(db):
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    if db.getUserFromEmail(email, password):
        return db.getUserFromEmail(email,password) 
    else:
        print("Your account died in war or doesnt exist.")
        return 

def mainPage(db, ID):
    name = db.getName(ID)[0]
    print("Welcome,",name)
    print("View friends [f]")
    print("View enemies [e]")
    print("Logout [l]")
    answer = input()
    answer = getValidInput(answer, ["f","e","l"])
    return answer

def friendsPage():
    print("FRIENDS")
    print("View feed [vf]")
    print("Post feed [pf]")
    print("List friends [lf]")
    print("Back [b]")
    answer = input()
    answer = getValidInput(answer, ["vf","pf","lf","b"])
    return answer

def enemiesPage():
    print("ENEMIES")
    print("View feed [ve]")
    print("Post feed [pe]")
    print("List enemies [le]")
    print("Add enemies [ae]")
    print("WAR!!! [w]")
    print("Back [b]")
    answer = input()
    answer = getValidInput(answer, ["ve","pe","le","ae","w","b"])
    return answer
    
def listFriends(db,ID):
    friends = db.getFriends(ID)
    if friends:
        for i in range(len(friends)):
            print(friends[i][0])
    else:
        print("you have no friends :(")
    return friends

def postFriends(db, ID):
    print("POST TO FRIENDS")
    title = input("Title: ")
    post = input("Content: ")
    db.createFriendPost(ID,post,title)
    print("SUCCESS!")
    print()

def viewFriendsFeed(db,ID):
    print("FRIENDS FREED")
    feed = db.getFriendsFeed(ID)
    try:
# 0 content
# 1 title
# 2 00:02:30
# 3 chaz1@mail
        for post in feed:
            email = post[3]
            title = post[1]
            content = post[0]
            time = post[2]
            print(email, "POSTED: ")
            print("*"+title+"*")
            print(content)
            print("--"+time)
    except TypeError:
        print("no posts")

def listEnemies(db, ID):
    enemies = db.getEnemies(ID)
    if enemies:
        for i in range(len(enemies)):
            print(enemies[i][0])
    else:
        print("you dont have any enemies go add some!")
    return enemies

def postEnemies(db, ID):
    print("POST TO ENEMIES")
    title = input("Title: ")
    post = input("Content: ")
    db.createEnemyPost(ID,post,title)
    print("SUCCESS!")
    print()

def viewEnemiesFeed(db,ID):
    print("ENEMIES FREED")
    feed = db.getEnemiesFeed(ID)
    try:
# 0 content
# 1 title
# 2 23:58:07
# 3 chaz1@mail 
        for post in feed:
            email = post[3]
            title = post[1]
            content = post[0]
            time = post[2]
            print(email, "POSTED: ")
            print("*"+title+"*")
            print(content)
            print("--"+time)
    except TypeError:
        print("no posts")

def makeEnemy(db, ID):
    enemy = db.getEnemy(ID)
    if enemy:
        print("You are aleady enemies with", enemy[0])
        return
    print("Who would you like to add")
    name = input()
    made = db.makeEnemy(name.lower(), ID)
    if not made:
        print("You cant go to war with yourself / friends " )

def war(db, ID):
    enemies = db.getEnemies(ID)
    if not enemies:
        print("you have no enemies, add enemies to go to war.")
        return
    print("WAR!!!")
    print("by declaring war you have a chance of loosing")
    print("and having your account deleted")
    print("do you wish to continue?")
    print("YES, LETS DO THIS!!! [y]")
    print("no im scared [n]")
    INPUT = input()
    getValidInput(INPUT , ["y","n"])
    if INPUT == "n":
        print("backing out ...")
        print()
        return
    print("Welcome to the battle field: ")
    print("you")
    f = [True] * (len(listFriends(db, ID))+1) # plus you
    print("vs")
    e = [False] * len(listEnemies(db, ID))
    war = f+e
    youWin = random.choice(war)
    if youWin:
        print("YOU WIN!")
        en = db.getEnemy(ID)[0]
        db.removeAccounts(en)
        return False
    else:
        print("YOU LOSE!")
        yall = db.getName(ID)[0]
        db.removeAccounts(yall)
        return True


def main():
    running = True
    while running:
        answer = loginPage()
        db = app_db.App()
        if answer == 'l':
            ID = login(db)
        elif answer == 's':
            ID = signUp(db)
        #######
        if ID:
            db.updateFriends(ID)
            db.updateEnemies(ID)
            while True:
                answer = mainPage(db,ID)
                if answer == 'f':
                    key = friendsPage()
                    if key == 'vf':
                        viewFriendsFeed(db,ID)
                        print()
                    elif key == 'pf':
                        postFriends(db,ID)
                        print()
                    elif key == 'lf':
                        listFriends(db,ID)
                        print()
                elif answer == 'e':
                    key = enemiesPage()
                    if key == 've':
                        viewEnemiesFeed(db,ID)
                        print()
                    elif key == 'pe':
                        postEnemies(db,ID)
                        print()
                    elif key == 'le':
                        listEnemies(db, ID)
                        print()
                    elif key == 'ae':
                        makeEnemy(db, ID)
                        print()
                    elif key == 'w':
                        x = war(db,ID)
                        if x:
                            break
                else:
                    break
            
        else:
            print("login failed or user already exists")
            

main()

