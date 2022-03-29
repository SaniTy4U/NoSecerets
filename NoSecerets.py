import mmap
import hashlib
import os
import time
import multiprocessing
from datetime import datetime

hash_selection = hashlib.md5
hash_type = "md5"
printstart = True
path_to_wordlist = "NOT CONFIGURED"
hashtable_name = "NOT CONFIGURED"
path_to_hashes = "NOT CONFIGURED"
path_to_hashtable = "NOT CONFIGURED"

titlescreen = """
 _,  _,____, ____,____,____,____,____, ____,____,____, 
(-|\ |(-/  \(-(__(-|_,(-/  (-|_,(-|__)(-|_,(-|  (-(__  
 _| \|,_\__/,____)_|__,_\__,_|__,_|  \,_|__,_|,  ____) 
(     (     (    (    (    (    (     (    (    (    
By MntlPrblm, https://github.com/MntlPrblm


[1] Create hashtable
[2] Change hashtype
[3] Run attack
"""

def configure_hashtable():
    #globalizes variables
    global path_to_wordlist
    global hashtable_name
    clear()
    print("[1] Wordlist: "+path_to_wordlist)
    print("[2] hashtable name: "+hashtable_name)
    print("[3] Generate hashtable")
    hashtable_option = input("Input: ")
    if hashtable_option == "1":
        path_to_wordlist = input("Path to wordlist: ")
        if os.path.exists(path_to_wordlist) == False:
            print("Wordlist not found")
            path_to_wordlist = "NOT CONFIGURED"
            time.sleep(2)
            configure_hashtable()
        configure_hashtable()
    if hashtable_option == "2":
        hashtable_name = input("Hashtable name: ")
        configure_hashtable()
    if hashtable_option == "3":
        hashtable_process = multiprocessing.Process(target=create_hashtable, args=(path_to_wordlist, hashtable_name))
        hashtable_process.start()
        hashtable_process.join()
    print("Invalid option")
    time.sleep(2)
    configure_hashtable()

#function to help count the file quickly
def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

def clear():
    if os.name == "posix":
        _ = os.system('clear')
    else:
        _ = os.system('cls')

#creates hashtable with given arguments
def create_hashtable(wordlist, hashtable):
    #makes it so the start dosent print twice
    global printstart
    global hash_selection

    #counts lines in file
    with open(wordlist, "r",encoding="utf-8") as f:
        linecount = sum(bl.count("\n") for bl in blocks(f)) + 1

    #gets current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start_time = time.time()

    #encodes wordlist
    amount_hashed = 0
    if printstart == True:
        print("Creating hashtable from "+str(linecount)+" lines. Time started: "+str(current_time))
        printstart = False
    with open(wordlist, mode="r+", encoding="utf-8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            text = mmap_obj.read().splitlines()
            for word in text:
                amount_hashed += 1
                #gets record of how long it took to encode 1000 hashes to estiamte eta
                if amount_hashed == 1000:
                    thousand_finished = time.time()
                    eta_1000 = thousand_finished - start_time
                #shows eta every 5000 hashes
                if amount_hashed%5000 == 0:
                    amount_remaining = linecount - amount_hashed
                    eta = (amount_remaining / 1000) * eta_1000
                    converted_eta = time.strftime("%H:%M:%S", time.gmtime(eta))
                    print("ETA: "+str(converted_eta)+", Lines hashed: "+str(amount_hashed))
                #adds hashes to specified file
                hash = hash_selection(word).hexdigest()
                with open(hashtable, 'a', encoding="utf-8") as f:
                    f.write(hash+":"+str(word.decode()))
                    f.write('\n')

    #shows ending information
    end_time = time.time()
    how_long = end_time - start_time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Finished! at "+str(current_time))
    finish_time = time.strftime("%H:%M:%S", time.gmtime(how_long))
    print("Time taken: "+finish_time)

def compare_hashes():
    global path_to_hashes
    global path_to_hashtable
    clear()
    print("[1] Hashtable: "+path_to_hashtable)
    print("[2] Hashes: "+path_to_hashes)
    print("[3] Run attack")
    option = input("Input: ")
    if option == "1":
        path_to_hashtable = input("Path to hashtable: ")
        if os.path.exists(path_to_hashtable) == False:
            print("Hashtable not found")
            time.sleep(2)
            path_to_hashtable = "NOT CONFIGURED"
            compare_hashes()
        else:
            compare_hashes()
    if option == "2":
        path_to_hashes = input("Path to hashes: ")
        if os.path.exists(path_to_hashes) == False:
            print("Hashes not found")
            time.sleep(2)
            path_to_hashes = "NOT CONFIGURED"
            compare_hashes()
        else:
            compare_hashes()
    if option == "3":
        if path_to_hashes == "NOT CONFIGURED":
            print("Please configure all options")
            time.sleep(2)
            compare_hashes()
        if path_to_hashtable == "NOT CONFIGURED":
            print("Please configure all options")
            time.sleep(2)
            compare_hashes()
        print("Starting attack...")
        attack_process = multiprocessing.Process(target=attack, args=(path_to_hashtable, path_to_hashes))
        attack_process.start()
        attack_process.join()
    print("Invalid option")
    time.sleep(2)
    compare_hashes()

def attack(path_to_hashtable, path_to_hashes):
    amount_hashed = 0
    #counts lines in hashtable
    with open(path_to_hashtable, "r",encoding="utf-8") as f:
        hashtable_count = sum(bl.count("\n") for bl in blocks(f)) + 1
    
    #counts how many hashes there are
    with open(path_to_hashes, "r",encoding="utf-8") as f:
        hashes_count = sum(bl.count("\n") for bl in blocks(f)) + 1

    #gets current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start_time = time.time()
    with open(path_to_hashes, "r",encoding="utf-8") as f:
        hashes = f.read().splitlines()
        for hash in hashes:
            with open(path_to_hashtable, mode="r+", encoding="utf-8") as file_obj:
                with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
                    hashcombos = mmap_obj.read().splitlines()
                    for w in hashcombos:
                        #print("Trying "+str(w.decode('utf-8')).split(':')[0])
                        if hash.lower() == str(w.decode('utf-8')).split(':')[0]:
                            print("Cracked! "+str(hash)+":"+str(w.decode('utf-8')).split(':')[1])
                            with open("cracked.txt", "a",encoding="utf-8") as f:
                                f.write(str(hash)+":"+str(w.decode('utf-8')).split(':')[1])
                                f.write('\n')
                                f.close
    #deletes duplicates in file at the end of every script
    lines_seen = set()
    with open("cracked.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i not in lines_seen:
                f.write(i)
                lines_seen.add(i)
        f.truncate()
    print("finished")
    quit()

def change_hashtype():
    global hash_type
    print("Current: "+str(hash_type))
    hash_type = input("New hash type: ")
    if hash_type == "md5":
        hash_selection = hashlib.md5
    elif hash_type == "sha1":
        hash_selection = hashlib.sha1
    elif hash_type == "sha224":
        hash_selection = hashlib.sha224
    elif hash_type == "sha256":
        hash_selection = hashlib.sha256
    elif hash_type == "sha384":
        hash_selection = hashlib.sha384
    elif hash_type == "sha512":
        hash_selection = hashlib.sha512
    elif hash_type == "blake2b":
        hash_selection = hashlib.blake2b
    elif hash_type == "blake2s":
        hash_selection = hashlib.blake2s
    elif hash_type == "sha3_224":
        hash_selection = hashlib.sha3_224
    elif hash_type == "sha3_256":
        hash_selection = hashlib.sha3_256
    elif hash_type == "sha3_384":
        hash_selection = hashlib.sha3_384
    elif hash_type == "sha3_512":
        hash_selection = hashlib.sha3_512
    elif hash_type == "shake_128":
        hash_selection = hashlib.shake_128
    elif hash_type == "shake_256":
        hash_selection = hashlib.shake_256
    else:
        clear()
        print("Please only enter hashes that are: sha1, sha224, sha256, sha384, sha512, blake2b, blake2s, md5, sha3_224, sha3_256, sha3_384, sha3_512, shake_128, or shake_256")
        time.sleep(3)
        change_hashtype()
    start()

def start():
    clear()
    print(titlescreen)
    option = input("Input: ")
    if option == "1":
        configure_hashtable()
    if option == "2":
        change_hashtype()
    if option == "3":
        compare_hashes()
    print("Invalid option")
    time.sleep(1)
    start()

if __name__ == '__main__':
    start()
