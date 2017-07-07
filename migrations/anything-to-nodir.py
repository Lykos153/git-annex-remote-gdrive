#!/usr/bin/env python3
#
# Copyright 2017 Silvio Ankermann <silvio@booq.org>
#

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os.path
import argparse

# for debugging
from pprint import pprint

class FileNotFoundException(Exception):
    pass
class FolderNotEmptyException(Exception):
    pass
class AmbigiousFoldernameException(Exception):
    pass
class InputError (Exception):
    pass

gauth = GoogleAuth()
gauth.LoadCredentialsFile("token.json")
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("token.json")

drive = GoogleDrive(gauth)

parser = argparse.ArgumentParser()
parser.add_argument("root", help="The ID of the root folder. ")
args = parser.parse_args()


def traverse(current_folder, current_path):
    print (f"In {current_path}")
    for file_list in drive.ListFile({'q': f"'{current_folder['id']}' in parents and trashed=false", 'maxResults': 100}):
        for file_ in file_list:
            if file_['mimeType'] == 'application/vnd.google-apps.folder':
                traverse(file_, current_path+"/"+file_['title'])
            elif (current_folder != root):
                print ( f"Moving {current_path}/{file_['title']}")
                file_['parents'] = [{'kind': 'drive#parentReference', 'id': root['id']}]
                file_.Upload()
    if (current_folder != root):
        delete_empty (current_folder, current_path)

def delete_empty (folder, path):
    file_list = drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false"}).GetList()
    if (len(file_list) == 0):
        print (f"Deleting empty {path}")
        folder.Delete()
    else:
        raise FolderNotEmptyException (path)


def getfolder(path):
    path_list = path.split('/')
    pprint(path_list)
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
            raise AmbigiousFoldernameException (current_path)
    return current_folder

root = getfolder(args.root)
if (root == drive.CreateFile({'id': 'root'})):
        raise InputError("Root is not an allowed prefix")

pprint (root['title'])

traverse(root, args.root)



#pprint(list(files))
