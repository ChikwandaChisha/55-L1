"""
Authors: Chikwanda Chisha and Patrick Bongo
Date: April 13, 2025
Password Manager - Authentication Module
"""

import json
from getpass import getpass
import os
import hashlib
from passlib.hash import pbkdf2_sha256
from crypto_utils import CryptoUtils

class Auth:
    def setup(self):
        """
        Set up the master password for the password manager.
        Allows user to either generate a random password or create their own.
        Stores the hashed password in vault.json.
        """
        crypto_utils = CryptoUtils()
        # Check if user wants to generate a random master password
        generate_check = input("Do you want to generate a master password? (y/n): ")
        if generate_check == 'y':
            master_password1 = crypto_utils.generate_pwd()
        else:
            # Get and confirm user's chosen master password
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
            
        # Hash the master password using PBKDF2
        hashed_password = pbkdf2_sha256.hash(master_password1)
        vault_data['master_pwd'] = hashed_password
        
        # Save the hashed password to vault.json
        with open('vault.json', 'w') as vault_file:
            json.dump(vault_data, vault_file)
    
    def password_exists(self):
        """
        Check if a master password has been set up.
        Returns:
            bool: True if master password exists, False otherwise
        """
        try:
            with open('vault.json', 'r') as vault_file:
                vault_data = json.load(vault_file)
                return 'master_pwd' in vault_data
        except (FileNotFoundError, json.JSONDecodeError):
            return False
    
    def login(self):
        """
        Authenticate user with their master password.
        Returns:
            bool: True if password is correct, False otherwise
        """
        master_password = getpass("Enter your master password: ")
        try:
            with open('vault.json', 'r') as vault_file:
                vault_data = json.load(vault_file)
                if 'master_pwd' in vault_data:
                    # Verify the entered password against the stored hash
                    return pbkdf2_sha256.verify(master_password, vault_data['master_pwd'])
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def change_master_password(self):
        """
        Change the master password.
        Requires current password verification before allowing the change.
        """
        if not self.login():
            print("Incorrect password")
        else:
            self.setup()
            print("Master password changed successfully")
