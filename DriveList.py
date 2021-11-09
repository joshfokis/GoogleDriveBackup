#!/usr/bin/env python


from typing import List

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def ListFolder(parent):
  filelist=[]
  file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
  for f in file_list:
    if f['mimeType']=='application/vnd.google-apps.folder': # if folder
        filelist.append({"id":f['id'],"title":f['title'],"list":ListFolder(f['id'])})
    # else:
    #     filelist.append(f['title'])
  return filelist


def main():
    folders = ListFolder('root')
    drive_folder = input("Name of folder in Google Drive to back-up to:\n> ")
    for p in folders:
        if p.get('title') == drive_folder:
            print(f'This is the id of your folder: {p.get("id")}')
    

gauth = GoogleAuth()

# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)


if __name__ == "__main__":
    main()