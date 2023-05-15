import os
import win32security
import time
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",   
    user= "root",
    password= ""
)

mycursor = mydb.cursor()
mycursor.execute("create database if not exists UserPermission")
mycursor.execute("use UserPermission")
mycursor.execute("create table if not exists user (id int primary key auto_increment, name varchar(255))")
mycursor.execute("create table if not exists permission (id int primary key auto_increment,path varchar(255), permission varchar(255), user_id int, foreign key (user_id) references user(id))")
# def get_permissions(file_path):
#     try:
#         security_descriptor = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
#         dacl = security_descriptor.GetSecurityDescriptorDacl()

#         permissions = []
#         if dacl is not None:
#             for i in range(dacl.GetAceCount()):
#                 rev, access, usersid = dacl.GetAce(i)
#                 user, domain, type = win32security.LookupAccountSid(None, usersid)
#                 permissions.append((domain + '\\' + user, access))
#         return permissions

#     except Exception as e:
#         print(f"Erreur lors de la récupération des permissions pour {file_path}: {str(e)}")
#         return []

# def walk_directory(directory_path):
#     for foldername, subfolders, filenames in os.walk(directory_path):
#         for filename in filenames:
#             file_path = os.path.join(foldername, filename)
#             permissions = get_permissions(file_path)
#             print(f"\nFichier : {file_path}")
#             for user, access in permissions:
#                 print(f"Utilisateur/Groupe : {user}, Permissions : {access}")

#         for subfolder in subfolders:
#             folder_path = os.path.join(foldername, subfolder)
#             permissions = get_permissions(folder_path)
#             print(f"\nDossier : {folder_path}")
#             for user, access in permissions:
#                 print(f"Utilisateur/Groupe : {user}, Permissions : {access}")

# if __name__ == "__main__":
#     start_time = time.time()
#     walk_directory('S:\\')  # Remplacer par le chemin du dossier souhaité
#     end_time = time.time()
#     End_time_To_Minute = (end_time - start_time) / 60
#     print(f"\nLe script a pris {End_time_To_Minute} minutes pour s'exécuter.")


 # Remplacer par le chemin du dossier souhaité