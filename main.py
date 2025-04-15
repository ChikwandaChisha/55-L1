from auth import Auth
from getpass import getpass
from crypto_utils import CryptoUtils

def crypto_utils_menu():
    crypto_utils = CryptoUtils()
    while True:
        print("\nPassword Manager Menu:")
        print("1. Add new account")
        print("2. Retrieve account")
        print("3. Edit account")
        print("4. Delete account")
        print("5. List all services")
        print("6. Delete all accounts")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    
    
def main():
    auth = Auth()
    print("Welcome to the password manager")
    while True:
        if auth.password_exists():
            if auth.login():
                crypto_utils_menu()
                if crypto_utils_menu().choice == "7":
                    break
            else:
                print('Login failed, please try again')
        else:
            auth.setup()
    
    
if __name__ == "__main__":
    main()
