import encryption
import config
import zipper
import setup

import tempfile
from getpass import getuser
from prettytable import PrettyTable
import os


setup.setupSyncio()

def defineConfig():
    folders_conf_arr = []
    folders_array = [f'C:\\\\Users\\\\{getuser()}\\\\Desktop\\\\', f'C:\\\\Users\\\\{getuser()}\\\\Documents\\\\', f'C:\\\\Users\\\\{getuser()}\\\\Pictures\\\\', f'C:\\\\Users\\\\{getuser()}\\\\Videos\\\\', f'C:\\\\Users\\\\{getuser()}\\\\Music\\\\']

    table = PrettyTable()
    table.field_names = ["Number", "Folder"]

    table.add_row([1, f"C:\\Users\\{getuser()}\\Desktop\\"])
    table.add_row([2, f"C:\\Users\\{getuser()}\\Documents\\"])
    table.add_row([3, f"C:\\Users\\{getuser()}\\Pictures\\"])
    table.add_row([4, f"C:\\Users\\{getuser()}\\Videos\\"])
    table.add_row([5, f"C:\\Users\\{getuser()}\\Music\\"])

    print(table)
    goal_input = input("Enter the numbers of each folder you want to sync. Seperate multiple numbers with a comma(eg 1,2): ")
    goal_input_array = goal_input.replace(" ", "").split(",")
    for number in goal_input_array:
        folders_conf_arr.append(folders_array[int(number)-1])

    config.editConfigurations(", ".join(folders_conf_arr))



master_password = input("Enter master password: ")

if config.getConfigurations() == "ERROR":
    defineConfig()


enc_or_dec = input("E for encrypt and D for decrypt: ")
if enc_or_dec.lower() == "e":
    ZIPNAMES = []

    for folder in config.getConfigurations():
        #append each zip's name to ZIPNAME const
        ZIPNAMES.append(folder.split("\\")[-2]+".zip")

        # zip contents of a folder to %temp%/[zipname].zip
        zipper.zip_folder_contents(folder, folder.split("\\")[-2]+".zip")

        # encrypt the zip file and change extension to .syncio
        encryption.encrypt_file(master_password, tempfile.gettempdir()+"\\"+folder.split("\\")[-2]+".zip", os.getenv('APPDATA')+"\\Syncio\\"+folder.split("\\")[-2]+".syncio")

elif enc_or_dec.lower() == "d":
    backups = os.listdir(os.getenv("APPDATA")+"\\Syncio")
    iteration = 1
    print("Here are your exiting encrypted backups:")

    table = PrettyTable()
    table.field_names = ["Number", "Folder"]

    for backup in backups:
        table.add_row([iteration, backup])
        iteration += 1




    print(table)
    pick = input("Enter the numbers of each folder you want to decrypt. Seperate multiple numbers with a comma(eg 1,2): ")
    picks = pick.split(",")
    for pick in picks:
        
        encryption.decrypt_file(master_password, os.getenv("APPDATA")+"\\Syncio\\"+backups[int(pick)-1], os.getcwd()+"\\"+backups[int(pick)-1].split(".")[0]+".zip")
    

    


