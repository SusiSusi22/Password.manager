import json 
import secrets 
import string
import subprocess
import sys 
import pprint

def random_password(lenght=16):
        
         zeichen = ( string.ascii_lowercase +
                    string.ascii_uppercase +
                    string.digits +
                    string.punctuation )
         return "".join(secrets.choice(zeichen) for _ in range (lenght))
 


def save_password():
        save_ypassword = input("Please enter the password you want to save \nor enter 'random' to generate a random passwort.\n")

        if save_ypassword == "random":

                Yrandom_password = random_password()
                print(f"Your random password is {Yrandom_password}")
                new_dict1 = input("Please enter the Website for the password.\n")
                new_dict2 = input("Please enter the username realted to the passwort.\n")
                save_ypassword = Yrandom_password      
                       
        else:
           repeat = input("Please enter your password one more time.\n")

           if repeat == save_ypassword:

                new_dict1 = input("Please enter the Website for the password.\n")
                new_dict2 = input("Please enter the username realted to the passwort.\n")
               
                
                print("Your password has been successfully saved!\n")
                
               
           else:
                  print("Please enter your correct password twice\n")


        new_entry = {f"Website": new_dict1,
                      "Username": new_dict2,
                      "Password": save_ypassword 
                         }


        with open("passwords.json", "r") as f:
         passwords = json.load(f)
        passwords.append(new_entry)
        with open("passwords.json", "w") as f:
         json.dump(passwords, f, indent=4)

        print("Your new entry has been saved successfully. What do you want to do?\n")
        subprocess.run ([sys.executable, "main_manager.py"])

def search_data():
         Data = input("Please enter a website, username or password.\n")

         with open("passwords.json", "r") as f:
          passwords = json.load(f)
         
         for entry in passwords:

            if (
                 Data == entry["Website"]
              or Data == entry["Username"]
              or Data == entry["Password"]
               ):
                 pprint.pprint(f"Here ist your Data for {Data}:")
                 print(f"""                    --------------------\n
                     Website: {entry["Website"]}
                     Username: {entry["Username"]}
                     Password: {entry["Password"]}\n
                     --------------------""")
                 
                 
            
                 print("What would you like to do next?\n")
                 subprocess.run([sys.executable, "main_manager.py"])
           

         else:
                no_data = input("I can't find your data. Do you want to save something new?\nPress Y for 'Yes' and N for 'No'\n")

                if no_data == "y":
                    print("What is your new entry?")
                    save_password()
                  
                elif no_data == "n":
                   print ("Okay, what do you want to do?")
                   subprocess.run ([sys.executable, "main_manager.py"])

                else:
                   print ("I didn't understand that. Please enter 'y' or 'n'\n")


         print("What would you like to do next?\n")
         subprocess.run([sys.executable, "main_manager.py"])

def load_passwords():
        print("Here are all your saved passwords!\n")
        with open("passwords.json", "r") as f:
          passwords = json.load(f)
          entry = passwords
          for entry in passwords:
             
             print("--------------------\n")
             print(f"""Password: {entry["Password"]}\nWebsite:  {entry["Website"]}\n""")
             print("--------------------")


        print("What do you want to do now?")
        subprocess.run([sys.executable, "main_manager.py"])


def delete_password():
       P_delete = input("Please enter the Website, Username or Password you want to delete.\n")
       with open("passwords.json", "r") as f:
            passwords = json.load(f)

            for entry in passwords:
                if (
                     P_delete == entry["Website"]
                  or P_delete == entry["Username"]
                  or P_delete == entry["Password"]
                      ):
                     safe = input(f"""Your entry is\n 

                                    {entry["Website"]},
                                    {entry["Username"]},
                                    {entry["Password"]},\n

                           do you really want to delete this entry? (Y / N)\n""") 
                     if safe == "y" or safe == "Y":
                                passwords.remove(entry)
                                with open("passwords.json", "w") as f:
                                    json.dump(passwords, f, indent=4) 

                                 
                                print("The entry has been deleted. What would you like to do?") 
                                subprocess.run([sys.executable, "main_manager.py"])    
                                
                     else:
                      print("Okay, we will not delete this entry.") 
                      subprocess.run([sys.executable, "main_manager.py"])    


                else:
                       print("Your Input is not saved as an entry. What do you want to do?\n")
                       subprocess.run([sys.executable, "main_manager.py"])

       

      
                      
    

         

   

                
                 
                 
        
              


       
