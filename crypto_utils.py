import cryptography
import json
import os
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet


class CryptoUtils:
    def __init__(self):
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
        # Encrypt the message using Fernet
        self.salt = os.urandom(16)
        msg_to_encrypt = self.salt + message.encode()
        encrypted_message = self.fernet.encrypt(msg_to_encrypt)
        return encrypted_message.decode()  
    
    def decrypt(self, encrypted_message):
        # Decrypt the message using Fernet
        decrypted_msg_with_salt = self.fernet.decrypt(encrypted_message.encode())
        decrypted_message = decrypted_msg_with_salt[16:]
        
        return decrypted_message.decode()  
    
    def add(self):
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
            print("Account already exists")
            return
        
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
            
        print("Account added successfully")
        
    def edit(self, service):
        with open('storage.json', 'r') as file:
            data = json.load(file)
        if service not in data:
            print("Account not found")
            return
        password = getpass("Add your password: ")
        username = input("Add your username: ")
        data[service] = [username, self.encrypt(password)]
        with open('storage.json', 'w') as file:
            json.dump(data, file)
        print("Account updated successfully")
    
    def retrieve(self, service):
        with open('storage.json', 'r') as file:
            data = json.load(file)
        
        username, password = data[service]
        password = self.decrypt(password)
        
        return f"Username: {username} \nPassword: {password}"
        
    def delete(self, service):
        with open('storage.json', 'r') as file:
            data = json.load(file)
        if service not in data:
            print("Account not found")
            return
        data.pop(service)
        with open('storage.json', 'w') as file:
            json.dump(data, file)
        print("Account deleted successfully")
    
    # pri
    def list_services(self):
        try:
            with open('storage.json', 'r') as file:
                data = json.load(file)
            services = list(data.keys())
            if services:
                print('The available accounts are: ', services)
            else:
                print('No accounts found')
        except FileNotFoundError:
            print('No accounts found')  
            
    def delete_all(self):
        with open('storage.json', 'w') as file:
            json.dump({}, file)
        print("All accounts deleted successfully")

