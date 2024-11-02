
#Importing required dependecies
import os

import bcrypt
import maskpass
import pandas as pd


#User related functions
#This function authenticate the User based on credentials
def login():
    try:
        global logged_in_user

        print("\n*****Please enter credentials*****")

        #Reading input from User
        username = read_username()
        password = read_password()

        #Getting User details based on username
        user_details =  get_user(username)

        #Checking User is exists or not
        if(len(user_details) > 0):  
            if(bcrypt.checkpw(password.encode('utf-8'), user_details["password"].values[0].encode('utf-8'))):
                logged_in_user = user_details
                print("\n*****User successfully loggedin*****")
                show_task_menu()
            else:
                print("\n*****Username or Password is wrong, Please try again*****")
        else:
            print("\n*****Username or Password is wrong, Please try again*****")
    except Exception as e:
        print(f"\n*****Something went wrong: {e}*****")


#This function creates new user in dataframe and writes the data in to CSV
def registration():

    try:
        print("\n*****Please enter registration details*****")
        
        #Taking input from the User and checking the Username already exists or not
        while True:
            username = read_username()

            user_details = get_user(username)

            if(len(user_details) > 0):
                print("\n*****Username already exists*****")
            else:
                break

        password = read_password()

        #Hashing password to save it in the Database or CSV
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt) 

        #Creating User and saving it in the Dataframe and CSV file
        if(create_user(username, password)):
            print("\n*****User registered successfully*****")
        else:
            print("\n*****Error while registering user please try again*****")
    except Exception as e:
        print(f"\n*****Something went wrong: {e}*****")

#This function reads username frome the user
def read_username():
    username = ''

    #taking input from User and username is mandatory
    while True:
        username = input("\nPlease enter Username: ")
        if(username):
            break
        print("\n*****Username is required*****")

    return username

#This function reads the password from the user
def read_password():
    password = ''

    while True:
        password = maskpass.askpass("\nPlease enter Password: ")
        if(password):
            break
        print("\n*****Password is required*****")

    return password

#This function creates user details in Data frame and writes the details to CSV file
def create_user(username, password):
    try:
        global users_data_frame, users_csv_db

        #Adding new user details to dataframe and CSV
        users_data_frame = users_data_frame._append({"username": username, "password": password.decode("utf-8")}, ignore_index = True)
        users_data_frame.to_csv(users_csv_db, sep='\t', index=False)

        return True
    except Exception as e:
        print(f"\n*****Something went wrong: {e}*****")
        return False


#This function gets user details based on username from dataframe
def get_user(username):

    global users_data_frame

    user_details =  users_data_frame.loc[users_data_frame['username'] == username]

    return user_details



#Task related functions

#This function shows Task menu list
def show_task_menu():
    global logged_in_user
    while True:
        print( f"\nHi {logged_in_user["username"].values[0]}, Please select an option: ")
        print("\nOptions:")
        print("\n1. Add Task")
        print("\n2. View Tasks")
        print("\n3. Mark as completed")
        print("\n4. Delete Task")
        print("\n5. Logout")

        option = input("\nPlease select a option: ")

        match option:
            case "1":
                if(add_task()):
                    print("\n*****Task added successfully*****")
                else:
                    print("\n*****Error while adding task please try again*****")
            case "2":
                view_task()
            case "3":
                if(update_status()):
                    print("\n*****Task updated successfully*****")
                else:
                    print("\n*****Error while updating task please try again*****")
            case "4":
                if(delete_task()):
                    print("\n*****Task deleted successfully*****")
                else:
                    print("\n*****Error while deleting task please try again*****")
            case "5":
                logged_in_user = None
                break
            case _:
                print("\n*****Invalid option is selected*****")

#This function delete the Task based on the Task ID
def delete_task():
    try:
        global logged_in_user, tasks_csv_db

        #Taking Task ID as input
        task_id = int(input("\nPlease enter Task ID: "))

        #Finding the Task with Task ID and Logged in user ID
        record = tasks_data_frame[(tasks_data_frame.index == task_id) & (tasks_data_frame['user_id'] == logged_in_user.index[0])]
        
        #Checking task found or not
        if(not record.empty):
            #Removing Task from the data frame and CSV
            tasks_data_frame.drop(task_id, axis=0, inplace=True,)
            tasks_data_frame.to_csv(tasks_csv_db, sep="\t", index=False)
            return True
        else:
            return False
    except Exception as e:
        
        print(f"\n*****An unexpected error occurred: {e}*****")
        return False

#This function Update the Task status
def update_status():
    try:
        global tasks_csv_db, logged_in_user

        task_id = int(input("\nPlease enter Task ID: "))

        #Finding the Task with Task ID and Logged in user ID
        record = tasks_data_frame[(tasks_data_frame.index == task_id) & (tasks_data_frame['user_id'] == logged_in_user.index[0])]

        if(not record.empty):
            #Updating Task status
            tasks_data_frame.at[task_id, "status"] = "Completed"

            tasks_data_frame.to_csv(tasks_csv_db, sep="\t", index=False)
            return True
        else:
            return False
    except Exception as e:
        print(f"\n*****Something went wrong ${e}*****")
        return False

#This function shows list of tasks
def view_task():
    #Getting Tasks related to logged in user
    user_tasks = tasks_data_frame[tasks_data_frame["user_id"] == logged_in_user.index[0]]

    print("**************************************************")
    print("Task ID", "Task description", "Status", sep="\t\t")
    print("**************************************************")

    #Checking tasks or there or not 
    if(not user_tasks.empty):
        for index, task in user_tasks.iterrows():
            print(index, task["task_description"], task["status"], sep="\t\t")
    else:
        print("\n*********************No records**********************")

    print("**************************************************")

#This function creates new task
def add_task():

    try:
        global tasks_data_frame, logged_in_user, tasks_csv_db

        #Reading task description from the user
        description = read_description()

        #Adding Task details into the Data frame and CSV file
        tasks_data_frame = tasks_data_frame._append({"user_id": logged_in_user.index[0], "task_description": description, "status": "Pending"}, ignore_index=True)
        tasks_data_frame.to_csv(tasks_csv_db, sep="\t", index=False)
        return True
    except:
        return False
    
#This function reads description from the user
def read_description():
    description = ''

    #taking input from User and username is mandatory
    while True:
        description = input("\nEnter Task description: ")
        if(description):
            break
        print("\n*****Description is required*****")

    return description

    
#This main function shows the Main menu
def main():
    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        option = input("\nPlease select a option: ")

        #Match condition for matching the option
        match option:
            case "1":
                login()
            case "2":
                registration()
            case "3":
                break
            case _:
                print("\nPlease Select a valid Option")


#Application entry point
if __name__ == "__main__":

    #Defining CSV files
    users_csv_db = "users.csv"
    tasks_csv_db = "tasks.csv"

   
    files = [users_csv_db, tasks_csv_db]

     #Creating CSV files If not exists
    for file in files:
        if not  os.path.exists(file):
            open(file, 'w')

    #Loading users data into data frame and If not exists creating empty Data frame
    try:
        users_data_frame = pd.read_csv(users_csv_db, sep='\t')
    except pd.errors.EmptyDataError:
        users_data_frame = pd.DataFrame(columns=["username", "password"])

    #Loading tasks data into data frame and If not exists creating empty Data frame
    try:
        tasks_data_frame = pd.read_csv(tasks_csv_db, sep='\t')
    except pd.errors.EmptyDataError:
        tasks_data_frame = pd.DataFrame(columns=["user_id", "task_description", "status"])

    logged_in_user = None

    #Staring Main application
    main()

    
    print("Bye Bye...")