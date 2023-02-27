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
    db.createUser(email, password, first_name.lower().strip(),last_name.lower().strip())
    return True

def login(db):
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    db.findUser(email, password)
    return True

def mainPage(first_name, last_name):
    print("Welcome,",first_name,last_name)
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
    print("View last name feed [vl]")
    print("Post last name feed [pl]")
    print("List last name friends [ll]")
    print("Back [b]")
    answer = input()
    answer = getValidInput(answer, ["vf","pf","lf","vl","pl","ll","b"])
    return answer

def enemiesPage():
    print("View first name feed [vf]")
    print("Post first name feed [pf]")
    print("List first name enemies [lf]")
    print("Add first name enemies [af]")
    print("View last name feed [vl]")
    print("Post last name feed [pl]")
    print("List last name enemies [ll]")
    print("Add last name enemies [al]")
    print("Back [b]")
    answer = input()
    answer = getValidInput(answer, ["vf","pf","lf","af","vl","pl","ll","al","b"])
    return answer
    

#note I think you can be eneies with a freind if war of last name friends are against someone that
#has your first name ... thats probly fine

#this is a way to do a switch statment in python, very useful in this case
match answer:
    case "vf":
        #view first name feed
        return
    case "pf":
        #post om first name feed
        return
    case "lf":
        #list all first name frinends

