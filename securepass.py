"""

    Display series of numbers in infinite loop
    Listen to key "s" to stop
    Only works on Windows because listening to keys
    is platform dependent

"""
import hashlib,uuid
def GetKeys(mask='*'):
    from os import name
    
    if name != 'nt':
        print("[!] Unable to mask input, not Windows")
        return 
        
    else:
        from sys import stdout 
        import msvcrt            
        x = msvcrt.kbhit()
        if x:
            #getch acquires the character encoded in binary ASCII
            ret = msvcrt.getch()
            print(mask,end="")
            stdout.flush()
        else:
            ret = False
        return ret

def MaskInput(mask):
    raw_chars = ""
    while True:
        #acquire the keyboard hit if exists
        key = GetKeys(mask) 
        
        #if we got a keyboard hit
        if key != False:
            char = key.decode()
            #print("KEY PRESSED: ", char)
            raw_chars = raw_chars + char                
            
        if key != False and key.decode() == '\r':
            string = raw_chars.strip("\r")
            #print("YOUR STRING IS: " + string)
            print()
            return string

def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
#    print("hash: ",hashed)
    return hashed

def check_password(hashed_password, user_password):
#    print("recalled hash: ",hashed_password)
#    print("user pass: ",user_password)
    password, salt = hashed_password.split(':')
    hashed = hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
#    print("Check: ",hashed)
    return password == hashed            
