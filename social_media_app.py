import app_db

def homePage():
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
        print("That is not a valid option! Try again.")
        print("OPTIONS: ",valid)
        INPUT = input()
        getValidInput(INPUT, valid)

def signUp(db):
    print("by signing up understand we will store your password as plain text.")
    print()
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    db.createUser(email, password, first_name.lower(),last_name.lower())
    return True

def login(db):
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    db.findUser(email, password)
    return True

def options(first_name, last_name):
    print("Welcome,",first_name,last_name)
    print("View feed [v]")
    print("Post feed [p]")
    print("View friends [f]")
    print("View enemies [e]")
    print("Add enemies [a]")
    print("Logout [l]")
    

