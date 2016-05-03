#!/usr/bin/python3
"""
Usage: transfer ( -l | -p | -u <file> | -d | -h)

Options:
  -h              Help.
  -d              Download file into your local folder
  -l              List files that have been uploaded to transfer.sh
  -p              Purge the files from list that have Expired
  -u <file>       Upload a file from a local folder to transfer.sh
                  This command requires to be followed by the full path of the
                  local file

Examples:
    transfer -l
    transfer -d
    transfer -p
    transfer -u ~/test.txt

"""
import os
import json
import datetime
import subprocess
from copy import deepcopy
try:
    from docopt import docopt
except ImportError:
    print("docopt library missing..\nPlease install by executing the following command:")
    print("pip3 install docopt")


VERSION = "0.1.0"
HOME = ""
UPLOAD_COMMAND = "curl --upload-file "
DWNLOAD_COMMAND = "curl "
SITE = "https://transfer.sh/"
LOCAL_DB = "files_stored_in_transfer.json"
LOCAL_DB_FULL = ""
FILE_LIST = {}
NO_DAYS_TO_KEEP = 14


def purge_deleted_files_from_Db():
    global HOME
    global FILE_LIST

    #print(FILE_LIST)

    #print(LOCAL_DB_FULL)
    temp_file_list = deepcopy(FILE_LIST)
    for item, fn in temp_file_list.items():
        if fn[2] == 'Expired':
            print(" {}\t{}\t{} -> has been deleted\n".format(
                    item, fn[0], fn[1]))
            del(FILE_LIST[item])
    write_to_file_db(FILE_LIST, LOCAL_DB_FULL)


def read_from_files_db(list=False):
    global FILE_LIST
    global HOME
    global LOCAL_DB_FULL
    if os.name == 'posix':
        HOME = os.environ['HOME']
        LOCAL_DB_FULL = HOME + "/" + LOCAL_DB
    else:
        #HOME = "C:" + os.environ['HOMEPATH']
        #LOCAL_DB_FULL = HOME + "\\" + LOCAL_DB
        exit("Only to be used in Unix like machines (Linux, UX, OSX)")

    #print(LOCAL_DB_FULL)
    if os.path.isfile(LOCAL_DB_FULL):
        with open(LOCAL_DB_FULL, 'r') as f:
            text = f.read()
            if text != "":
                FILE_LIST = json.loads(text)
                if list:
                    temp_file_list = deepcopy(FILE_LIST)
                    print(" ID\tURL\t\t\t\t\t\t\tDate\tStatus")
                    print("~"*90)
                    for item, fn in temp_file_list.items():
                        update_file_status(FILE_LIST, item)

                    write_to_file_db(FILE_LIST, LOCAL_DB_FULL)

                    for item, fn in FILE_LIST.items():
                        print(" {}\t{}\t{}\t{}\n".format(
                            item, fn[0], fn[1], fn[2]))

            else:
                print("======================")
                print("Files DB is Empty, no files in Transfer.sh")
                print("======================")

    else:
        if list:
            print("======================")
            print("DB File {} not found".format(LOCAL_DB_FULL))
            print("======================")
        print("Creating new DB file...")
        command = "touch {}".format(LOCAL_DB_FULL)
        res = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        if res.stdout.readline().decode() == '':
            print("File {} created successfuly.".format(LOCAL_DB_FULL))
        else:
            print("Something happened: {}".format(res.stdout.readline().decode()))


def write_to_file_db(myDb, f_name):
    today = datetime.date.today()
    myDb = json.dumps(myDb, indent=1)
    #print("Writing to {}".format(f_name))
    #print(myDb)
    with open(f_name, 'w') as f:
        f.write(myDb)


def add_resultURL(URL):
    global FILE_LIST
    #print(URL)
    if FILE_LIST == {}:
        idx = 1
    else:
        idx = max(FILE_LIST.keys())
        idx = int(idx) + 1
    #print("Next Index: {}".format(idx))
    FILE_LIST["{}".format(idx)] = [URL, str(datetime.date.today()), "Available"]
    #print(FILE_LIST)


def upload_file(f_name):
    global FILE_LIST
    #print(f_name)
    if os.path.isfile(f_name):
        f_basename = os.path.basename(f_name)
        command = "{}{} {}{}".format(UPLOAD_COMMAND, f_name, SITE, f_basename)
        #command = "ls /home/jose/files_stored_in_transfer.json"
        print("\nSending Command: " + command)
        res = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        for i in range(4):
            res_URL = res.stdout.readline().decode()

        res_URL = res_URL.strip()

        print(res_URL)
        add_resultURL(res_URL)

    else:
        print("Check path, file do not exists")

    try:
        write_to_file_db(FILE_LIST, LOCAL_DB_FULL)
    except Exception as e:
        print(e)


def update_file_status(myDb, item):
    #print("\nupdate DB file status")
    today = datetime.date.today()
    delta = datetime.timedelta(days=NO_DAYS_TO_KEEP)
    expire_date = today - delta
    y, m, d = myDb[item][1].split('-')
    f_day = datetime.date(int(y), int(m), int(d))
    #print("{} < {} ?".format(f_day, expire_date))
    if f_day < expire_date:
        #print(" Item {}\t Status Changed to Expired\n".format(item))
        myDb[item][2] = "Expired"
        #print(myDb)



def download_file():
    read_from_files_db(list=True)
    user_in = 0
    try:
        user_in = input("Please enter the ID number from the above list: ")
    except ValueError as e:
        print("Value needs to be an Integer from the ID list Above.")
    except KeyboardInterrupt:
        print("\nAction Interrupted, Goodbye!")

    if user_in != 0:
        selected = FILE_LIST[str(user_in)]
        url_name = selected[0]
        f_basename = url_name.split("/")
        f_basename = str(f_basename[-1:])
        print(str(f_basename[-1:]))
        command = "{}{} -o {}".format(DWNLOAD_COMMAND, url_name, \
                                f_basename.strip("]['"))
        #command = "ls /home/jose/files_stored_in_transfer.json"
        print("\nSending Command: " + command)
        res = subprocess.Popen(command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        for i in range(4):
            result = res.stdout.readline().decode()

        if result != '':
            print("Not sure what happend : {}".format(result))

def main():
    # Collects the arguments passed to the script from command line
    arguments = docopt(__doc__, version=VERSION)

    # Start by reading the information already existing in the files DB
    read_from_files_db()
    # add_resultURL('https://transfer.sh/fsdjifhu/test.json')

    # Act upon the arguments passed
    if arguments.get('-u') != None:
        # Uploads file to transfer.sh and if successful adds the file to the DB
        upload_file(arguments.get('-u'))
    elif arguments.get("-l"):
        # Lists the existing files in transfer.sh based on what is saved in DB
        read_from_files_db(list=True)
    elif arguments.get("-p"):
        purge_deleted_files_from_Db()
    elif arguments.get("-d"):
        download_file()
    else:
        print("Something Wrong, we should not be here...")


if __name__ == '__main__':
    main()
    
