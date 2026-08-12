from manager import *
print()
print ("####### PASSWORD MANAGER #######\n\n")

choice = input("Save Password (press '1')\nSearch Data (press '2')\nLoad Passwords (press '3')\nDelete an entry (press '4')\n") 

if choice == "1":
    save_password()

elif choice == "2":
    search_data()

elif choice == "3":
    load_passwords()

elif choice == "4":
    delete_password()

else:
    print("Please enter '1', '2', '3' or '4'.")



