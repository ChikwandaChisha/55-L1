"""
Authors: Chikwanda Chisha and Patrick Bongo
Date: April 13, 2025
Password Manager - Main Module
"""

from auth import Auth
from crypto_utils import CryptoUtils
import time

auth = Auth()

def crypto_utils_menu():
    crypto_utils = CryptoUtils()
    start_time = time.time()
    timeout = start_time + 5*60 # 5 minutes timeout
    
    while time.time() < timeout:
        print(f"\nTime remaining: {timeout - time.time():.0f} seconds")
        print("\nPassword Manager Menu:")
        print("1. Add new account")
        print("2. Retrieve account")
        print("3. Edit account")
        print("4. Delete account")
        print("5. List all services")
        print("6. Delete all accounts")
        print("7. Change master password")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            crypto_utils.add()
        elif choice == "2":
            service = input("Enter service name to retrieve: ")
            print(crypto_utils.retrieve(service))
        elif choice == "3":
            service = input("Enter service name to edit: ")
            crypto_utils.edit(service)
        elif choice == "4":
            service = input("Enter service name to delete: ")
            crypto_utils.delete(service)
        elif choice == "5":
            crypto_utils.list_services()
        elif choice == "6":
            confirm = input("Are you sure you want to delete all accounts? (yes/no): ")
            if confirm.lower() == 'yes':
                crypto_utils.delete_all()
            else:
                print("Operation cancelled")
        elif choice == "7":
            auth.change_master_password()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    
    
def main():
    print("Welcome to the password manager")
    while True:      
        if auth.password_exists():
            if auth.login():
                crypto_utils_menu()
                print('You have been logged out')
                break
                    
            else:
                print('Login failed, please try again')
        else:
            auth.setup()
    
    
if __name__ == "__main__":
    main()
