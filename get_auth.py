import os
import win32security
import time
import mysql.connector
import socket
import ntsecuritycon as con
hostname = socket.gethostname()

mydb = mysql.connector.connect(
    host="localhost",   
    user= "root",
    password= ""
)

mycursor = mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS UserPermission")
mycursor.execute("create database if not exists UserPermission")
mycursor.execute("use UserPermission")
mycursor.execute("create table if not exists user (id int primary key auto_increment, name varchar(255), user_type varchar(255))")
mycursor.execute("create table if not exists permission(id int primary key auto_increment, code varchar(255) , name varchar(255))")
mycursor.execute("create table if not exists _permission (id int primary key auto_increment,path varchar(255), object_type varchar(255), inheritance_enabled varchar(255), permission_id int, user_id int, foreign key (user_id) references user(id), foreign key (permission_id) references permission(id))")

user_cache = {}
permission_cache = {}

PERMISSIONS_MAP = {
    2032127: 'Full Control',
    1245631: 'Modify',
    131241: 'Read & Execute',
    131209: 'Read',
    278: 'Write',
    262144: 'Change Permissions',
    65536: 'Delete',
    131072: 'Read Permissions',
    262144: 'Change Permissions',
    524288: 'Take Ownership',
    1048576: 'Synchronize',
    268435456: 'Access System Security',
    268435457: 'Maximum Allowed',
    1179817: 'Generic All',



}

def is_inherited(directory_path,user):
    root_permissions = get_permissions(directory_path)
    if user not in root_permissions:
        return 'Non'
    else:
        return 'Oui'


def insert_user(user_name, user_type):
    if user_name in user_cache:
        return user_cache[user_name]
        
    mycursor.execute('SELECT id FROM user WHERE name = %s', (user_name,))
    result = mycursor.fetchone()
    if result is not None:
        user_cache[user_name] = result[0]
        return result[0]
    else:
        sql = "insert into user (name, user_type) values (%s, %s)"
        val = (user_name, user_type)
        mycursor.execute(sql, val)
        user_id = mycursor.lastrowid
        user_cache[user_name] = user_id
        return user_id

def insert_permission(permission,permission_name):
    
    if permission in permission_cache:
        return permission_cache[permission]

    mycursor.execute('SELECT id FROM permission WHERE name = %s', (permission,))
    result = mycursor.fetchone()
    if result is not None:
        permission_id = result[0]
        permission_cache[permission] = permission_id
    else:
        sql = "insert into permission (code,name) values (%s, %s)"
        val = (permission,permission_name)
        mycursor.execute(sql, val)
        permission_id = mycursor.lastrowid
        permission_cache[permission] = permission_id

    return permission_id

def insert_user_permission(path, object_type, inheritance_enabled, permission_id, user_id):
    sql = "insert into _permission (path, object_type, inheritance_enabled, permission_id, user_id) values (%s, %s, %s, %s, %s)"
    val = (path, object_type, inheritance_enabled, permission_id, user_id)
    mycursor.execute(sql, val)



def get_permissions(file_path):
    try:
        security_descriptor = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)
        dacl = security_descriptor.GetSecurityDescriptorDacl()
        permissions = {}
        if dacl is not None:
            for i in range(dacl.GetAceCount()):
                ace = dacl.GetAce(i)
                rev, permission, usersid = ace
                user, domain, type = win32security.LookupAccountSid(None, usersid)
                user_type = get_type_user(type)
                user_key = domain + '\\' + user
                permission_name = convert_to_readable_permission(permission)
                permissions[user_key] = (permission, permission_name, user_type)
        return permissions
    except Exception as e:
        print(f"Error while retrieving permissions for {file_path}: {str(e)}")
        return {}




def get_type_user(type):
    if type == win32security.SidTypeUser:
        user_type = 'User'
    elif type == win32security.SidTypeGroup:
        user_type = 'Group'
    elif type == win32security.SidTypeWellKnownGroup:
        user_type = 'WellKnownGroup'
    else:
        user_type = 'Other'
    return user_type

def convert_to_readable_permission(permission):
    if permission in PERMISSIONS_MAP:
        return PERMISSIONS_MAP[permission]
    else:
        return 'Other'



def walk_directory(directory_path):
    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            permissions = get_permissions(file_path)
            for user, (permission, permission_name, user_type) in permissions.items():
                
                user_id = insert_user(user, user_type)
                permission_id = insert_permission(permission, permission_name)
                insert_user_permission(file_path, 'file', is_inherited(directory_path,user), permission_id, user_id)

        for subfolder in subfolders:
            folder_path = os.path.join(foldername, subfolder)
            permissions = get_permissions(folder_path)
            for user, (permission, permission_name, user_type) in permissions.items():
                user_id = insert_user(user, user_type)
                permission_id = insert_permission(permission, permission_name)
                insert_user_permission(folder_path, 'directory', is_inherited(directory_path,user), permission_id, user_id)
		   
            print (folder_path)

if __name__ == "__main__":
    start_time = time.time()
    mydb.start_transaction()
    print('Enter path to directory to scan: ')
    path = input();
    walk_directory(path)
    mydb.commit()  
    end_time = time.time()
    End_time_To_Minute = (end_time - start_time) / 60
    print(f"\nLe script a pris {End_time_To_Minute} minutes pour s'exécuter.")
