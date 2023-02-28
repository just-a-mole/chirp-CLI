import app_db

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
    first_name = input("Enter First Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    db.createUser(email, password, first_name.lower().strip())
    return db.getUserFromEmail(email,password) 

def login(db):
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    if db.getUserFromEmail(email, password):
        return db.getUserFromEmail(email,password) 
    else:
        print("Your account died in war or doesnt exist.")
        return 

def mainPage():
    print("Welcome,")
    print("View friends [f]")
    print("View enemies [e]")
    print("Logout [l]")
    answer = input()
    answer = getValidInput(answer, ["f","e","l"])
    return answer

def friendsPage():
    print("View first name feed [vf]")
    print("Post first name feed [pf]")
    print("List first name friends [lf]")
    print("Back [b]")
    answer = input()
    answer = getValidInput(answer, ["vf","pf","lf","b"])
    return answer

def enemiesPage():
    print("View first name feed [ve]")
    print("Post first name feed [pe]")
    print("List first name enemies [le]")
    print("Add first name enemies [ae]")
    print("Back [b]")
    answer = input()
    answer = getValidInput(answer, ["ve","pe","le","ae","b"])
    return answer
    

#note I think you can be eneies with a freind if war of last name friends are against someone that
#has your first name ... thats probly fine

#this is a way to do a switch statment in python, very useful in this case

def viewEnemies(db, id):
    print(db.getEnemies(id))

def main():
    running = True
    while running:
        answer = loginPage()
        db = app_db.App()
        if answer == 'l':
            id = login(db)
        elif answer == 's':
            id = signUp(db)
        #######
        if id:
            while True:
                answer = mainPage()
                if answer == 'f':
                    key = friendsPage()
                    if key == 'vf':
                        # viewFriends(db)
                        print()
                    elif key == 'pf':
                        # postFriends(db)
                        print()
                    elif key == 'lf':
                        # listFriends(db)
                        print()
                elif answer == 'e':
                    key = enemiesPage()
                    if key == 've':
                        viewEnemies(db, id)
                        print(id)
                    elif key == 'pe':
                        # postEnemies(db)
                        print()
                    elif key == 'le':
                        # listEnemies(db)
                        print()
                    elif key == 'ae':
                        # addEnemies(db)
                        print()
                else:
                    break
            
        else:
            print("login failed")
            

main()


