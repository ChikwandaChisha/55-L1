"""
Authors: Chikwanda Chisha and Patrick Bongo
Date: April 13, 2025
Password Manager - Main Module
"""

from auth import Auth
from crypto_utils import CryptoUtils
import time
import os

# Initialize the authentication system
auth = Auth()

def crypto_utils_menu():
    """
    Display and handle the main password manager menu.
    Implements a 3-minute timeout for security.
    """
    crypto_utils = CryptoUtils()
    # Set up 3-minute timeout
    start_time = time.time()
    timeout = start_time + 3*60
    
    menu_text = """
Password Manager Menu:
1. Add new account
2. Retrieve account
3. Edit account
4. Delete account
5. List all services
6. Delete all accounts
7. Change master password
8. Exit
"""
    print(menu_text)
    while True:        
        # Check if timeout has occurred
        if time.time() >= timeout:
            print("\nSession timed out due to inactivity")
            break
            
        # Display remaining time and menu
        print(f"\nTime remaining: {int(timeout - time.time())} seconds")
        
        
        # Get user choice and handle accordingly
        choice = input("\nEnter your choice (1-8): ")
        
        # Reset timeout timer after user input
        timeout = time.time() + 3*60
        
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
            # Confirm before deleting all accounts
            confirm = input("Are you sure you want to delete all accounts? (y/n): ")
            if confirm.lower() == 'y':
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
    """
    Main program loop.
    Handles initial setup, login, and session management.
    """
    print("Welcome to the password manager")
    while True:      
        if auth.password_exists():
            # Attempt login if master password exists
            if auth.login():
                crypto_utils_menu()
                print('You have been logged out')
                break
            else:
                print('Login failed, please try again')
        else:
            # Set up master password if none exists
            auth.setup()
    
if __name__ == "__main__":
    main()
