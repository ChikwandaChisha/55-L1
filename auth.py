import json
from getpass import getpass
import os
import hashlib
from passlib.hash import pbkdf2_sha256


class Auth:
    def __init__(self):
        pass
    
    def setup(self):
        master_password1 = getpass("Setup your master password: ")
        master_password2 = getpass("Confirm your master password: ")
        # Check if the passwords match
        while master_password1 != master_password2:
            print("Passwords do not match")
            master_password1 = getpass("Setup your master password: ")
            master_password2 = getpass("Confirm your master password: ")
            
        # Try to read existing vault data
        try:
            with open('vault.json', 'r') as vault_file:
                vault_data = json.load(vault_file)
        except (FileNotFoundError, json.JSONDecodeError):
            vault_data = {}
            
        # Hash the master password
        hashed_password = pbkdf2_sha256.hash(master_password1)
        vault_data['master_pwd'] = hashed_password
        
        # Save to vault.json
        with open('vault.json', 'w') as vault_file:
            json.dump(vault_data, vault_file)
    
    def password_exists(self):
        try:
            with open('vault.json', 'r') as vault_file:
                vault_data = json.load(vault_file)
                return 'master_pwd' in vault_data
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def login(self):
        master_password = getpass("Enter your master password: ")
        try:
            with open('vault.json', 'r') as vault_file:
                vault_data = json.load(vault_file)
                if 'master_pwd' in vault_data:
                    return pbkdf2_sha256.verify(master_password, vault_data['master_pwd'])
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def change_master_password(self):
        if not self.login():
            print("Incorrect password")
        else:
            self.setup()
            print("Master password changed successfully")
