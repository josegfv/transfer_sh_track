# transfer.py
## Python script for transfer.sh

Transfer.sh (https://transfer.sh) is a website that provides easy file sharing from command line.

Transfer.sh requires that we take advantage of curl command functionality to allow upload and download of files,
while transfer.sh will store the files you need to move around for a short time (14 days)

I found out about transfer.sh website and really like the simplicity of using command line and be able 
to upload files temporarily in order to move them around easily. 
I wrote this python script to be able to track the files that I have uploaded while they are still 
available in transfer.sh.

## Pre-Requisites
There are of course a few items that are required in your system in oder to be able to 
run transfer.py.
- As of now the script only support posix operating systems(Linux, Unix, OSX, etc)
- The script was written for Python3 (so make sure you have it in your system)
- I requires the docopt and json libraries to be install for python 3
- The script will create a local file (files_stored_in_transfer.json) in the users home directory
  whereit keeps the information on the files you have uploaded form that computer to transfer.sh

## Usage
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

## Features
Keep a list of the files you have uploaded to transfer.sh and whether the file are Available or Expired
Allows you to upload files (one at a time on this version)
Download files from transfer.sh that have not yet expired and are still Available
Files that have expired can be purged from the local tracking file 
