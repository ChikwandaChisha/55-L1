import json
from getpass import getpass

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
            
        # Update vault data with master password
        vault_data['master_pwd'] = master_password1
        
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
                if 'master_pwd' in vault_data and vault_data['master_pwd'] == master_password:
                    return True
            return False
        except (FileNotFoundError, json.JSONDecodeError):
            return False
