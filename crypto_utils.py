"""
Authors: Chikwanda Chisha and Patrick Bongo
Date: April 13, 2025
Password Manager - Cryptography Utilities Module
"""

import cryptography
import json
import os
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet
import random
import secrets
import string


class CryptoUtils:
    def __init__(self):
        """
        Initialize the CryptoUtils class.
        Loads or generates the encryption key and sets up the Fernet cipher.
        """
        # Try to load existing key, or generate a new one if it doesn't exist
        try:
            with open('vault.json', 'r') as vault_file:
                vault_data = json.load(vault_file)
                self.key = vault_data['key'].encode()
        except (FileNotFoundError, KeyError):
            self.key = Fernet.generate_key()
            with open('vault.json', 'w') as vault_file:
                json.dump({'key': self.key.decode()}, vault_file)
                
        self.fernet = Fernet(self.key)
        self.data = {}
        
    def encrypt(self, message):
        """
        Encrypt a message using Fernet symmetric encryption.
        Args:
            message (str): The message to encrypt
        Returns:
            str: The encrypted message as a string
        """
        # Encrypt the message using Fernet
        self.salt = os.urandom(16)
        msg_to_encrypt = self.salt + message.encode()
        encrypted_message = self.fernet.encrypt(msg_to_encrypt)
        return encrypted_message.decode()  
    
    def decrypt(self, encrypted_message):
        """
        Decrypt a message that was encrypted using Fernet.
        Args:
            encrypted_message (str): The encrypted message to decrypt
        Returns:
            str: The decrypted message
        """
        # Decrypt the message using Fernet
        decrypted_msg_with_salt = self.fernet.decrypt(encrypted_message.encode())
        decrypted_message = decrypted_msg_with_salt[16:]
        
        return decrypted_message.decode()  
    
    def add(self):
        """
        Add a new account to the password manager.
        Handles service name, username, and password input.
        Supports password generation and confirmation.
        """
        input_message = input("Add your service name: ")
        
        # Try to read existing data, or start with empty dict if file doesn't exist or is empty
        try:
            with open('storage.json', 'r') as file:
                content = file.read()
                if not content.strip():
                    data = {}
                else:
                    data = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
            
        if input_message in data:
            print("\nAccount already exists")
            return
        
        # check if the user wants to generate a password
        choice = input("Do you want to generate a password? (y/n): ")
        if choice == 'y':
            password1 = self.generate_pwd()
        
        else:
            password1 = getpass("Add your password: ")
            password2 = getpass("Confirm your password: ")
            
            # check if the passwords match
            while password1 != password2:
                print("Passwords do not match")
                password1 = getpass("Add your password: ")
                password2 = getpass("Confirm your password: ")
        
        username = input("Add your username: ")
        data[input_message] = [username, self.encrypt(password1)]
        
        # save the data to the json file
        with open('storage.json', 'w') as file:
            json.dump(data, file)
            
        print("\nAccount added successfully!")
        
    def edit(self, service):
        """
        Edit an existing account's username and/or password.
        Args:
            service (str): The service name to edit
        """
        with open('storage.json', 'r') as file:
            data = json.load(file)
            
        if service not in data:
            print("Account not found")
            return
        
        # check if the user wants to change the username
        username_change = input("Do you want to change the username? (y/n): ")
        if username_change == 'y':
            username = input("Add your username: ")
        else:
            username = data[service][0]
        
        # check if the user wants to change the password
        password_change = input("Do you want to change the password? (y/n): ")
        if password_change == 'y':
            # check if the user wants to generate a new password
            password_generate = input("Do you want to generate a new password? (y/n): ")
            if password_generate == 'y':
                password = self.generate_pwd()
            else:
                password = getpass("Add your password: ")
        else:
            password = self.decrypt(data[service][1])
            
        print(f"\nUsername: {username} \nPassword: {password}")
            
        data[service] = [username, self.encrypt(password)]
        with open('storage.json', 'w') as file:
            json.dump(data, file)
        print("Account updated successfully")
    
    def retrieve(self, service):
        """
        Retrieve and display an account's credentials.
        Args:
            service (str): The service name to retrieve
        Returns:
            str: Formatted string containing username and decrypted password
        """
        with open('storage.json', 'r') as file:
            data = json.load(file)
        
        # check if the service exists
        if service not in data:
            print("\nAccount does not exist")
            return
        
        username, password = data[service]
        password = self.decrypt(password)
        
        return f"\nUsername: {username} \nPassword: {password}"
        
    def delete(self, service):
        """
        Delete an account from the password manager.
        Args:
            service (str): The service name to delete
        """
        with open('storage.json', 'r') as file:
            data = json.load(file)
            
        # check if the service exists
        if service not in data:
            print("Account not found")
            return
        
        # delete the service
        data.pop(service)
        with open('storage.json', 'w') as file:
            json.dump(data, file)
            
        print("\nAccount deleted successfully")
    
    def list_services(self):
        """
        List all services stored in the password manager.
        """
        try:
            with open('storage.json', 'r') as file:
                data = json.load(file)
            services = list(data.keys())
            if services:
                print('\nThe available accounts are: ', services)
            else:
                print('\nNo accounts found')
        except FileNotFoundError:
            print('\nNo accounts found')  
            
    def delete_all(self):
        """
        Delete all accounts from the password manager.
        Requires user confirmation before proceeding.
        """
        # delete all accounts
        with open('storage.json', 'w') as file:
            json.dump({}, file)
        print("\nAll accounts deleted successfully")
    
    def generate_pwd(self):
        """
        Generate a random password.
        Args:
            master_pwd (bool): If True, indicates this is for a master password   
        Returns:
            str: The generated password
        """
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        selection = letters + digits + special_chars
        password = ''
        
        for _ in range(22):
            password += random.choice(selection)
        
        print(f"\nYour master password is: {password}")
        return password
        

