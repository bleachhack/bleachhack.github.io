import os
import sys
import time
import uuid
import zipfile
import requests
import shutil
from colorama import Fore, init
from clint.textui import progress


def _exit():
    print(Fore.RESET)

    if os.name == 'nt':
        os.system("pause")
    else:
        os.system('read -s -n 1 -p "Press any key to continue..."')

    sys.exit()
    
init()

if len(sys.argv) != 3:
    print(Fore.RED + "Invalid argument size")
    print(Fore.RED + "Syntax: installer.py [old-mod] [new-mod-url]")
    _exit()

oldmodfile = sys.argv[1]
url = sys.argv[2]
tempfile = "bh-" + str(uuid.uuid4())

print("Downloading latest build..")

r = requests.get(url, stream=True)
with open(tempfile, "wb") as f:
    header = r.headers.get("content-length")

    try:
        total_length = int(header)
    except:
        total_length = 2_600_000

    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        if chunk:
            f.write(chunk)
            f.flush()

if url.endswith(".zip"):
    print("Extracting jar..")
    with zipfile.ZipFile(tempfile, 'r') as zp:
        files = zipfile.ZipFile.infolist(zp)
        if len(files) > 0:
            unzippedfile = "bh-" + str(uuid.uuid4())

            with open(unzippedfile, 'wb') as f:
                f.write(zp.read(files[0].filename))
        else:
            print("No files in zipfile, Aborting!")
            _exit()

    os.remove(tempfile)
    tempfile = unzippedfile

print("Replacing jar..")

firstLine = False
while True:
    try:
        os.remove(oldmodfile)

        if firstLine:
            print();

        break;
    except Exception as e:
        if not os.path.exists(oldmodfile):
            print(Fore.YELLOW + "- File already deleted??")
            break;

        if firstLine:
            print(".", end="")
        else:
            print("- Waiting for Minecraft to close.", end="")
            firstLine = True

        time.sleep(1)

try:
    shutil.move(tempfile, oldmodfile)
except Exception as e:
    print(Fore.RED + "Unable to move jar to mod directory, Aborting!")
    _exit()

print(Fore.GREEN + "\nInstalled Successfully!")
print(Fore.GREEN + "Restart Minecraft to apply the new version")

_exit()
