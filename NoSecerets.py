import mmap
import hashlib
import os
import time
import multiprocessing
from datetime import datetime

printstart = True
path_to_wordlist = "NOT CONFIGURED"
hashtable_name = "NOT CONFIGURED"

titlescreen = """
 _,  _,____, ____,____,____,____,____, ____,____,____, 
(-|\ |(-/  \(-(__(-|_,(-/  (-|_,(-|__)(-|_,(-|  (-(__  
 _| \|,_\__/,____)_|__,_\__,_|__,_|  \,_|__,_|,  ____) 
(     (     (    (    (    (    (     (    (    (    
By MntlPrblm, https://github.com/MntlPrblm


[1] Create hashtable
[2] Attack options
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
                hash = hashlib.md5().hexdigest()
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


def start():
    clear()
    print(titlescreen)
    option = input("Input: ")
    if option == "1":
        configure_hashtable()


if __name__ == '__main__':
    start()
