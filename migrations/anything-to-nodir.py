#!/usr/bin/env python3
#
# Copyright 2017 Silvio Ankermann <silvio@booq.org>
#

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os.path
import argparse

class FileNotFoundException(Exception):
    pass
class FolderNotEmptyException(Exception):
    pass
class AmbiguousFoldernameException(Exception):
    pass
class InputError (Exception):
    pass
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Recursively moves all files to root
def traverse(current_folder, current_path):
    global moved_count, deleted_count
    for file_list in drive.ListFile({'q': f"'{current_folder['id']}' in parents and trashed=false", 'maxResults': 100}):
        for file_ in file_list:
            if file_['mimeType'] == 'application/vnd.google-apps.folder':
                traverse(file_, current_path+"/"+file_['title'])
            elif (current_folder != root):
                print ( f"Moving {current_path}/{file_['title']}")
                file_['parents'] = [{'kind': 'drive#parentReference', 'id': root['id']}]
                file_.Upload()
                moved_count += 1
    if (current_folder != root):
        delete_empty (current_folder, current_path)
        deleted_count += 1

# Checks if folder is empty, then deletes it
def delete_empty (folder, path):
    file_list = drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false"}).GetList()
    if (len(file_list) == 0):
        print (f"Deleting empty {path}")
        folder.Delete()
    else:
        raise FolderNotEmptyException (path)

# Returns the file object of the repository's root
def getfolder(path):
    path_list = path.split('/')
    current_folder = drive.CreateFile({'id': 'root'})
    current_path = ""
    for folder in path_list:
        current_path = "/".join([current_path, folder])
        file_list = drive.ListFile({'q': f"'{current_folder['id']}' in parents and title='{folder}' and trashed=false"}).GetList()
        if (len(file_list) == 1):
            print (f"Found {folder}")
            current_folder = file_list[0]
        elif (len(file_list) == 0):
            raise FileNotFoundException (current_path)
        else:
            raise AmbiguousFoldernameException (current_path)
    return current_folder



parser = argparse.ArgumentParser()
parser.add_argument("root", help="The ID of the root folder. ")
parser.add_argument("--token", help="If defined, access token will be stored in and loaded from this file. By default, no credentials are stored.")
args = parser.parse_args()

# Authentication
gauth = GoogleAuth()
if args.token:
    gauth.LoadCredentialsFile(args.token)

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

if args.token:
    gauth.SaveCredentialsFile(args.token)

# Counter for statistics
moved_count = 0
deleted_count = 0

drive = GoogleDrive(gauth)
root = getfolder(args.root)
if (root == drive.CreateFile({'id': 'root'})):
    raise InputError("Root is not an allowed prefix")

answer= input (f"{bcolors.WARNING}This will move all files from subdirectories in /{args.root} directly to /{args.root} and delete all empty subfolders on the way. OK (y/n)?{bcolors.ENDC} ")
if answer.lower() != "y":
    raise SystemExit

try:
    traverse(root, args.root)
except (KeyboardInterrupt, SystemExit):
    print (f"\n{bcolors.WARNING}Exiting.")
    print ("The remote is in an undefined state now. Re-run this script before using git-annex on it.")
else:
    print (f"\n{bcolors.OKGREEN}Finished.")
    print (f"The remote has now 'nodir' structure. Remember to change the layout via 'git annex enableremote' and consider checking consistency with 'git annex fsck --from=<remotename> --fast'")

print ( f"Processed {deleted_count} subfolders" )
print ( f"Moved {moved_count} files{bcolors.ENDC}")



