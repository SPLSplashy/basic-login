####IMPORT####
import os, sys, time
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import zlib, json, getpass
####SET YOURE VARIABLES####
RECOVERY_PASSWORD = "myPassword"
YOUREFOLDER = "YOUREPATH"
YOUREDATA = "YOUREDATA"
SUCESS_MESSAGE = "Sucess"
WELCOME_USER_TEXT = "Welcome User"
DURATION = 6
DATA_IN_JSON = True
####MAIN FUNCTION####
def login(): #maybe add some else or elif statements forgot to do them
    try: #if error occurs we jump to except
        os.chdir(YOUREFOLDER) #going in folder
        with open(f"{YOUREDATA}.json", "r") as f: #opening file in read mode
            data = f.read() #reading file
            data = json.loads(data) #reading file with json
        input_username = input(str("Username: ")) #username input
        time.sleep(DURATION)
        input_passwd = getpass.getpass("Password: ") #getpass hides youre input
        time.sleep(DURATION)
        user = data["data"][0]["user"] #calling the username from the json file
        if input_username == user: 
            passwd = data["data"][0]["passwd"] #same thing
            passwd = str(passwd).encode() #encoding in bytes
            passwd = unobscure(passwd) #decrypting the bytes in string
            passwd = str(passwd).split("'")
            passwd = passwd[1] # selecting the second string in the list
            if input_passwd == passwd:
                welcoming_user(WELCOME_USER_TEXT)
                print("\n\n")

    except Exception: #happens if error in try: occurs
        recovery_pwd = input(str("Recovery Password: "))
        if recovery_pwd == RECOVERY_PASSWORD:
            if os.path.isdir(YOUREFOLDER) == True: #if youre folder exists
                os.chdir(YOUREFOLDER) # go in the folder
            elif os.path.isdir(YOUREFOLDER) == False: #if it does not exist
                os.mkdir(YOUREFOLDER) #make the folder
                time.sleep(1) #chill for one second
                os.chdir(YOUREFOLDER) #go in the folder
            time.sleep(1)
            username = input(str("New Username: "))
            pwd = getpass.getpass("New password: ") #again getpass is like normal input
            pwd_repeat = getpass.getpass("Repeat new password: ")
            pwd = checking_new_password(str(pwd), str(pwd_repeat)) #jumping to the function and getting the return
            reading_dump = json_data_dump(username, pwd) #same thing
            with open(f"{YOUREDATA}.json", "w+") as f: #creating the file with write more lines than one
                dump = json.dumps(reading_dump) 
                f.write(dump)
            print(SUCESS_MESSAGE + username)
####ENCRYPTION####
def obscure(data: bytes):
    return b64e(zlib.compress(data, 9)) 
####DECRYPTION####
def unobscure(obscured: bytes):
    return zlib.decompress(b64d(obscured))

def checking_new_password(passwd1, passwd2):
        if passwd1 == passwd2: 
            passwd = passwd1.encode()
            passwd = obscure(passwd)
            passwd = str(passwd).split("'")
            passwd = passwd[1]
            return passwd
          
def json_data_dump(user, pwd):
    json_dump_data = {
    "data" : [
         {
             "DONT_CHANGE_THIS":"CHANGING THIS FILE IS GOING TO CORRUPT YOUR PROGRAM",
             "user":f"{user}",
             "passwd":f"{pwd}"
        }
    ]
 }
    return json_dump_data #just some basic json

def welcoming_user(text): #only purpose to look a little bit more fancy
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(0.1)
