#!/usr/bin/env python3
#
# Copyright 2017 Silvio Ankermann <silvio@booq.org>
#

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError
from googleapiclient.errors import HttpError
import os.path
import argparse
import tenacity

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
@tenacity.retry(wait=tenacity.wait_fixed(2), retry=(tenacity.retry_if_exception_type(ApiRequestError) | tenacity.retry_if_exception_type(HttpError) | tenacity.retry_if_exception_type(ConnectionResetError)))
def traverse(current_folder, current_path):
    global moved_count, deleted_count
    if (current_folder == root):
        for file_list in drive.ListFile({'q': f"'{current_folder['id']}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false", 'maxResults': 100, 'orderBy': 'title'}):
            for file_ in file_list:
                traverse(file_, current_path+"/"+file_['title'])
    else:
        for file_list in drive.ListFile({'q': f"'{current_folder['id']}' in parents and trashed=false", 'maxResults': 100, 'orderBy': 'title'}):
            for file_ in file_list:
                if file_['mimeType'] == 'application/vnd.google-apps.folder':
                    traverse(file_, current_path+"/"+file_['title'])
                else:
                    print ( f"Moving {current_path}/{file_['title']}")
                    file_['parents'] = [{'kind': 'drive#parentReference', 'id': root['id']}]
                    file_.Upload()
                    moved_count += 1
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
            raise FileNotFoundException (f"{current_path} not found")
        else:
            raise AmbiguousFoldernameException (f"There are two or more folders named {current_path}")
    return current_folder



parser = argparse.ArgumentParser()
parser.add_argument("root", help="The root folder of the repository. Enter exactly what's specified as 'prefix', by default that's 'git-annex'.")
parser.add_argument("--token", help="If defined, access token will be stored in and loaded from this file. By default, no credentials are stored.")
args = parser.parse_args()

# Authentication
gauth = GoogleAuth()
gauth.settings['client_config_backend'] = 'settings'
gauth.settings['client_config'] = {'client_id': '914459249505-ji3d9v92ealsmc4a63ns66uoj9t6mdf0.apps.googleusercontent.com', 'client_secret': 'ivD4Ms4eROu10sHc43ojgX05', 'auth_uri':'https://accounts.google.com/o/oauth2/auth', 'token_uri':'https://accounts.google.com/o/oauth2/token', 'revoke_uri': None, 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'}

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
try:
    root = getfolder(args.root)
except (FileNotFoundException, AmbiguousFoldernameException) as e:
    print(str(e))
    raise SystemExit

if (root == drive.CreateFile({'id': 'root'})):
    print("Root is not an allowed prefix")
    raise SystemExit

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



