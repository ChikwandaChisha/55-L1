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
            
        
        with open('vault.json', 'w') as vault_file:
            vault_data = json.load(vault_file)
            if not vault_data:
                vault_data = {}
            
        vault_data['master_pwd'] = master_password1
        json.dump(vault_data, vault_file)
    
    def password_exists(self):
        with open('vault.json', 'r') as vault_file:
            vault_data = json.load(vault_file)
        if 'master_pwd' in vault_data:
            return True
        else:
            return False
    
    def login(self):
        master_password = getpass("Enter your master password: ")
        with open('vault.json', 'r') as vault_file:
            vault_data = json.load(vault_file)
        if self.password_exists():
            if vault_data['master_pwd'] == master_password:
                return True
            else:
                return False
        else:
            return False
