######### Software Engineering (Fundamentals) T17        ######################
#######             Compulsory Task 1                            ##############
#         modifying task_manager.py                                           #
#                                                                             #
###############################################################################
# supporting text files (user.txt and tasks.txt) 


#=====importing libraries===========
import os
from datetime import datetime, date
from tabulate import tabulate           # This will help make output of tasks easy to read
import linecache                        # This will aford reading a secific line from a txt file https://tinyurl.com/56vepyfh
DATETIME_STRING_FORMAT = "%Y-%m-%d"


#===== FUNCTIONS ==================

def display_menu(menu_description, menu_choices,curr_user,main_menu):
    '''displays all menus on the screen with a consistent "look& feel"'''

    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print("\n" ,menu_description)
    str_choices = "Select one of the following Options below:"
    if curr_user == "admin" and main_menu:
        str_choices = str_choices + "\n\tds" + "\tDisplay stats"

    for key, value in menu_choices.items():
        str_choices = str_choices + "\n\t" + str(key) + "\t" +str(value) 
    str_choices = str_choices + "\n Your Choice: "

    choice = input(str_choices).lower()

    return choice


################  Function to Create a list of tasks #################################
def create_task_list():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)
        
    return task_list

############# Function to read the usernames and passwords ##########################
def read_usernames_passwords():
    '''This function reads usernames and password from the user.txt file and returns the data as a dictionary 
    '''
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    usernames_passwords = {}
    for user in user_data:
        username, password = user.split(';')
        usernames_passwords[username] = password

    return usernames_passwords


#############   Function logs a valid user onto the system ########
def login():
    logged_in = False
    curr_user = ""
    usernames_passwords = read_usernames_passwords()

    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        if curr_user not in usernames_passwords.keys():
            print("User does not exist")
            continue
        elif usernames_passwords[curr_user] != curr_pass:
            print("Wrong username and/or password")
            continue
        else:
            print("Login Successful!")
            logged_in = True
    return curr_user, logged_in


########### Function registers a new user #########

def reg_user():
    # - Request input of a new username
    unique_username = False 
    username_passwords=read_usernames_passwords()

    # this loop ensures that usernames are not duplicated
    while not unique_username:
        new_username = input("New Username: ")
        if username_already_exists(new_username):
                print ("Username already exists. Please use another username")
        else:
            unique_username = True

    #set up variable to deal with password verification
    password_verified = False
    password_attempts = 0

    # - Check if the new password and confirmed password are the same.
    while password_verified == False and password_attempts <3:
        password_attempts +=1
  
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # save the new username and pasword if password is verified
        if new_password == confirm_password:
            password_verified = True
            usernames_passwords[new_username] = new_password
                
            with open("user.txt", "a") as out_file:
                user_data = []
                user_data.append(f"{new_username};{new_password}")
                out_file.write("\n")
                out_file.write("\n".join(user_data))
            print ("\n User successfully added\n")    

        # - Otherwise you present a relevant message.
        else:
            if password_attempts < 3:
                print("Passwords do not match, try again\n")
            else:
                print("That was your final attempt. You will be returned to the main menu\n")


#####################  Function to Add a user inputted task to the tasks file ############
def add_task():
    '''Allow a user to add a new task to task.txt file
    '''
    task_components = []
    task_username_valid = False
    usernames_passwords = read_usernames_passwords()

    # get a valid username and append it to the task list
    while task_username_valid == False:
        task_username = input("Name of person assigned to task: ")
        if task_username not in usernames_passwords.keys():
            print("User does not exist. Please enter a valid username")
        else:
            task_username_valid = True
    task_components.append(task_username)
 
    # get the tak title and append it to the task list
    task_title = input("Title of Task: ")
    task_components.append(task_title)

    # get a task description and append it to the task list
    task_description = input("Description of Task: ")
    task_components.append(task_description)

    # get a task due date in the correct format and append to the task list
    
    date_today = date.today().strftime(DATETIME_STRING_FORMAT)
    date_today = datetime.strptime(date_today, DATETIME_STRING_FORMAT)
    date_valid = False

    while not date_valid:
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                delta = due_date_time - date_today
                days_to_due_date = delta.days
                if  days_to_due_date < 0 or  days_to_due_date> 366:
                    print ("\n____________________________________________________________________________________")
                    print ("Invald date. You cannot have a date in the past or more than 12 months in the future")
                    print ("------------------------------------------------------------------------------------\n")
                else:
                    date_valid = True
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")    
    
    
    task_components.append(due_date_time)

    # Generate the current date and append it ot the task list with the correct format
    curr_date = date.today()
    task_components.append(curr_date)

    # append the completed status of the task to False as it will not yet be completed
    task_components.append(False)

    # there are now a list of task components in the correct format that can be updates
    update_task_in_file(task_components)
    print("Task successfully added.")
    # print(task_components)
    # ['sim', 'dog', 'walking dogs', datetime.datetime(2023, 12, 12, 0, 0), datetime.date(2023, 6, 20), False]

################# Function to update a task, given a set of task list (task_components)


def update_task_in_file(task_components):
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {}
    new_task['username'] = task_components[0]
    new_task['title'] = task_components[1]
    new_task['description'] = task_components[2]
    # new_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    new_task['due_date'] = task_components[3]
    # new_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    new_task['assigned_date']  = task_components[4]

    new_task['completed'] = True if task_components[5] == "Yes" else False

    task_list = create_task_list()
    task_list.append(new_task)

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]

            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


##################   function to view all tasks    ##################
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    task_list = create_task_list()
    num_tasks = 0
    all_user_tasks = [["Title", "Assigned to", "Date Assigned", "Date Due", "Task Description"]]


    for t in task_list:
        num_tasks +=1
        task_to_add = [str(t['title']), str(t['username']),str(t['assigned_date'].strftime(DATETIME_STRING_FORMAT)),\
                       str(t['due_date'].strftime(DATETIME_STRING_FORMAT)), str(t['description']) ]               
        all_user_tasks.append(task_to_add)
    
    if num_tasks != 0 :
        # Display all tasks in a manner that is easy to read. 
        print("\n")
        print("These are all current tasks")
        print (tabulate(all_user_tasks, headers = "firstrow", tablefmt="fancy_grid"))     
    else:
        print("You have no tasks listed")
        return

##################   function to view the current user's tasks   ###################   
def view_mine(curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    task_list = create_task_list()
    # create a header row to display the user tasks
    curr_user_tasks = [["Task Number", "Title", "Date Assigned", "Date Due", "Description", "Completed?"]]

    task_number = 0
    my_task_number = 0

    # to be able to decide whether the user is choosing a task assigned to them,
    # we create this list which indexes each of the tasks that are assigned to the user
    ref_my_task_to_all_tasks = []

    for t in task_list:
        # the task number affords the user a way of being able to reference each task
        task_number +=1
        if t['username'] == curr_user:
            ref_my_task_to_all_tasks.append(task_number)
            #  Each task is displayed with a corresponding number which can be used to identify the task.
            my_task_number +=1            
            if t['completed'] == False:
                str_completed = "No"
            else:
                str_completed = "Yes"    
            #get each task that is the current users task and update them in the current users task list
            curr_user_task_to_add = [str(task_number), str(t['title']),str(t['assigned_date'].strftime(DATETIME_STRING_FORMAT)),\
                                        str(t['due_date'].strftime(DATETIME_STRING_FORMAT)), str(t['description']), \
                                        str(str_completed)]
            curr_user_tasks.append(curr_user_task_to_add)
    
    if my_task_number != 0 :  
    # Display all tasks in a manner that is easy to read. 
    # After much time struggling with a solution to the "easy to read" output I used solution here https://youtu.be/Smf68icE_as
        print("\n")
        print("These are the tasks assigned to the user ", curr_user)
        print (tabulate(curr_user_tasks, headers = "firstrow", tablefmt="fancy_grid"))     
    else:
        print("You have no tasks listed")
        return

    editable_tasks =[["Task Number", "Title", "Date Assigned", "Date Due", "Description", "Completed?"]]
    my_tasks_editable = False
    editable_task_numbers = []
    
    for c in curr_user_tasks:   
        if c[5] == "No":
            my_tasks_editable = True
            curr_task_number= c[0]
            editable_tasks.append(c)
            editable_task_numbers.append(int((curr_task_number)))

    if not my_tasks_editable:

        # User will be returned to main menu if there are no editable tasks

        menu_description = "NONE OF YOUR TASKS ARE EDITABLE"
        edit_my_tasks_menu = { "ANY KEY" : "To return to the main menu"}
        edit_my_tasks_choice = display_menu(menu_description, edit_my_tasks_menu, curr_user, False)
        return
    else:
        menu_description = "EDIT MY TASKS MENU"
        edit_my_tasks_menu = { " e\t" : "To edit your tasks",
                        "-1\t" : "To return to the main menu"}
        edit_my_tasks_choice = display_menu(menu_description, edit_my_tasks_menu,curr_user, False)

        if edit_my_tasks_choice == -1:
            return
            
        elif edit_my_tasks_choice.lower() == "e":

            valid_choice = False
            while not valid_choice:
                print (tabulate(editable_tasks, headers = "firstrow", tablefmt="fancy_grid"))
                edit_task_number = input("State the number of the task you would like to edit : ")

                if edit_task_number.isnumeric():
                    if int(edit_task_number) in editable_task_numbers:
                        valid_choice = True
                        edit_task_number=int(edit_task_number)
                else:
                    print("\n*****************************************************************")
                    print("Invalid Choice. Please select one of the Task Numbers in the table")
                    print("*****************************************************************")           

            edit_complete = False
            #now go to the file and get the task that the user wants to edit
            with open("tasks.txt", "r") as task_file:
                task_to_edit = linecache.getline("tasks.txt",edit_task_number)
                task_components = task_to_edit.split(";")
                task_components[3] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)      # 2023-06-18 00:00:00
                task_components[4] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)      # 2023-06-18 00:00:00
                # task_component[0], task_component[1], task_component[2], task_component[3], task_component[4], task_component[5], 
                # ['admin', 'Add functionality to task manager', 'Add additional options and refactor the code.', '2022-12-01', '2022-11-22', 'No\n']

            while not edit_complete:
                edit_complete = False
                menu_description = "SELECT EDITS MENU"
                select_edits_menu = { " 1\t" : "To mark the task as completed",
                                      " 2\t"  :  "To change the username assigned or completion date for this task",
                                    "-1\t" : "To return to the main menu"}            
                edit_choice = display_menu(menu_description, select_edits_menu,curr_user,False)
            
                if edit_choice == "-1":
                    edit_complete = True

                elif edit_choice == "1":
                    task_components[5] = "Yes"
                    delete_line_in_file("tasks.txt", edit_task_number)
                    update_task_in_file(task_components)
                    print ("The task has been marked as complete and will no longer be editable")
                    edit_complete = True
                
                elif edit_choice == "2":
                    original_task_username = task_components[0]
                    original_task_due_date = task_components[3]
                    edited_username = ""
                    edited_due_date = ""

                    edited_username, edited_due_date = edit_my_task(original_task_username, original_task_due_date)
                    
                    if not (edited_username == original_task_username and edited_due_date == original_task_due_date):
                        task_components[0] = edited_username
                        task_components[3] = edited_due_date
                        delete_line_in_file("tasks.txt", edit_task_number)
                        update_task_in_file(task_components)
                        print ("The task has been updated")
                        edit_complete = True                    

                else:
                    print("Invalid entry")


########### Function to update an edited task ########
def edit_my_task(username, due_date):
    '''Allow a user to edit a task in task.txt file
    '''
    new_username = username
    new_due_date = due_date
    edit_complete  = False

    menu_description = "EDIT USER ASSIGNED AND DATE DUE MENU"
    edit_my_tasks_menu = { " 1" : "To assign another user to this task",
                        " 2" : "To change the due date",
                        "-1" : "To Return to the main menu"
                        }
    # allow several edits until -1 selected to return to main menu.
    while not edit_complete:
        choice = display_menu(menu_description, edit_my_tasks_menu,curr_user, False)

        if choice == "1":
            #Make sure the user is entering a valid username to assign to this task
            new_username_valid = False
            while not new_username_valid:
                new_username = input("Enter a new username for this task: ")
                if new_username not in usernames_passwords.keys():
                    print("User does not exist. Please enter a valid username")
                else:
                    new_username_valid = True     


        elif choice == "2":

            date_today = date.today().strftime(DATETIME_STRING_FORMAT)
            date_today = datetime.strptime(date_today, DATETIME_STRING_FORMAT)
            date_valid = False

            while not date_valid:
                while True:
                    try:
                        new_due_date = input("Enter the new Due date of this task (YYYY-MM-DD): ")
                        new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        delta = new_due_date - date_today
                        days_to_due_date = delta.days
                        if  days_to_due_date < 0 or  days_to_due_date> 366:
                            print ("\n____________________________________________________________________________________")
                            print ("Invald date. You cannot have a date in the past or more than 12 months in the future")
                            print ("------------------------------------------------------------------------------------\n")
                        else:
                            date_valid = True
                            break
                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")

        elif choice == "-1":
            edit_complete = True
        
        else:
            print("Invalid choice.")

    return new_username, new_due_date


########### Function to remove a line from a file #############
def delete_line_in_file(filename, line_number):
    
    with open (filename) as file:
        lines = file.readlines()
        del lines[line_number-1]

    with open (filename, "w") as file:
        for line in lines:
            file.write(line)

########### function to generate reports    ############

def generate_reports(usernames_passwords):
    task_list = create_task_list()

    
    total_num_tasks = len(task_list)
    num_completed_tasks = 0
    incomplete_overdue_tasks = 0
    overdue_tasks = 0

    #create date in a format where it can be used to compare with the date due to find overdue tasks
    date_today = date.today().strftime(DATETIME_STRING_FORMAT)
    date_today = datetime.strptime(date_today, DATETIME_STRING_FORMAT)

    for t in task_list:
        task_overdue = False
        # Following 2 lines and 2 lines of code above is an attempt to get the date due and todays date into the same format for comparing
        due_date = t['due_date'].strftime(DATETIME_STRING_FORMAT)
        due_date = datetime.strptime(due_date, DATETIME_STRING_FORMAT)

        if due_date < date_today:
            task_overdue = True

        if t['completed']:
            num_completed_tasks +=1
        if task_overdue:
            overdue_tasks +=1
        if task_overdue and not t['completed']:
            incomplete_overdue_tasks +=1
    
    num_uncompleted_tasks = total_num_tasks - num_completed_tasks

    fraction_incomplete_tasks = num_uncompleted_tasks/total_num_tasks

    fraction_overdue_tasks = overdue_tasks/total_num_tasks

    reports=[]
    with open("task_overview.txt", "w") as task_overview_file:

        str_report_temp = "Task Manager Overview"
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
        str_report_temp = "\n\tTotal Number of Tasks generated:\t\t" + str(total_num_tasks)
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
        str_report_temp = "\n\tTotal Number of completed Tasks:\t\t"+str(num_completed_tasks)
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
        str_report_temp = "\n\tTotal Number of Uncompleted Tasks:\t\t" +str(num_uncompleted_tasks)
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
        str_report_temp = "\n\tTotal Number of Uncompleted & Overdue Tasks:\t"+ str(incomplete_overdue_tasks)
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
        str_report_temp = "\n\tThe percentage of tasks that are incomplete:\t"+str( "{:.0%}".format(fraction_incomplete_tasks))
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
        str_report_temp = "\n\tThe percentage of tasks that are overdue:\t" +str("{:.0%}".format(fraction_overdue_tasks))
        reports.append(str_report_temp)
        task_overview_file.write(str_report_temp)
    print("\nSUCCEES")
    print("The file task_overvew.txt has been generated showing the statistics for tasks generated\n")


    usernames_passwords = read_usernames_passwords()
    total_num_users = len(usernames_passwords)

    with open("user_overview.txt", "w") as user_file:
        str_report_temp = "Overview of Users of the Task Manager"
        reports.append(str_report_temp)
        user_file.write(str_report_temp)
        str_report_temp = "\n\tTotal number of users registered:\t"+ str(total_num_users)
        reports.append(str_report_temp)
        user_file.write(str_report_temp)
        str_report_temp = "\n\tTotal number of tasks:\t\t\t" + str(total_num_tasks)
        reports.append(str_report_temp)
        user_file.write(str_report_temp)        
        for username in usernames_passwords:
            num_tasks_this_user = 0
            num_tasks_completed_this_user = 0
            num_tasks_uncompleted_overdue_this_user = 0


            for t in task_list:
                
                task_overdue = False

                due_date = t['due_date'].strftime(DATETIME_STRING_FORMAT)
                due_date = datetime.strptime(due_date, DATETIME_STRING_FORMAT)

                if due_date < date_today:
                    task_overdue = True
                
                if t['username'] == username:
                    num_tasks_this_user +=1
                    if t['completed']:
                        num_tasks_completed_this_user +=1
                    else:
                        if task_overdue:
                            num_tasks_uncompleted_overdue_this_user  +=1
            
            str_report_temp = "\n\nTASK STATISTICS FOR " + username
            reports.append(str_report_temp)
            user_file.write(str_report_temp)
            
            if num_tasks_this_user >0:
                fraction_assigned_this_user = num_tasks_this_user/total_num_tasks
                fraction_assigned_complete_this_user = num_tasks_completed_this_user/num_tasks_this_user
                fraction_assigned_incomplete_this_user = 1-fraction_assigned_complete_this_user
                fraction_incomplete_overdue_this_user = num_tasks_uncompleted_overdue_this_user/num_tasks_this_user

         
                str_report_temp = "\n\t Tasks assigned:    " + str(num_tasks_this_user)
                reports.append(str_report_temp)
                user_file.write(str_report_temp)  
                str_report_temp = "\tPercentage of total:  " + str("{:.0%}".format(fraction_assigned_this_user))
                reports.append(str_report_temp)
                user_file.write(str_report_temp)  
                str_report_temp = "\tCompleted:            " + str("{:.0%}".format(fraction_assigned_complete_this_user))
                reports.append(str_report_temp)
                user_file.write(str_report_temp)  
                str_report_temp = "\tNot completed:        " + str("{:.0%}".format(fraction_assigned_incomplete_this_user))
                reports.append(str_report_temp)
                user_file.write(str_report_temp)
                str_report_temp = "\tIncomplete & overdue: " + str("{:.0%}".format(fraction_incomplete_overdue_this_user))
                reports.append(str_report_temp)
                user_file.write(str_report_temp)
            else:
                str_report_temp = "\nThis user has been assigned no tasks"
                reports.append(str_report_temp)
                user_file.write(str_report_temp)
    
    print("File user_overview.txt has been generated showing the statistics for users of the system")
    return reports

##################   function to display stats   ###################
#      o Modify the menu option that allows the admin to display statistics so that the reports generated are read from tasks.txt 
#       and user.txt and displayed on the screen in a user-friendly manner. If these text files don’t exist (because the user hasn’t 
#       selected to generate them yet), first call the code to generate the text files.

def display_stats():
    '''If the user is an admin they can display statistics about number of users
        and tasks.'''

    str_task=""

    print("\n*****  DISPLAYING STATISTICS FOR TASKS  *****\n")
    with open ("task_overview.txt") as file:
        lines = file.readlines()
        for line in lines:
            str_task=str_task+line
    print (str_task)

    str_user =""

    print("\n*****  DISPLAYING STATISTICS FOR USERS   *****\n")
    with open ("user_overview.txt") as file:
        lines = file.readlines()
        for line in lines:
            str_user=str_user+line

    print (str_user)
    return

##################   function username already exists   ###################

def username_already_exists(username_to_test):
    '''This code reads usernamesfrom the user.txt file to see if the username passed already exists
    '''
    username_already_exists = False

    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    username_data = {}
    for user in user_data:
        username, password = user.split(';')
        username_data[username] = password
        
    if username_data.get(username_to_test) is not None:
        username_already_exists = True

    return username_already_exists

############# MAIN PROGRAM  ##############

usernames_passwords = read_usernames_passwords()

curr_user, logged_in = login()

while True:

    menu_description = "MAIN MENU"

    main_menu = { "r" : "Registering a user",
                    "a" : "Adding a task",
                    "va" : "View all tasks",
                    "vm" : "View my tasks",
                    "gr" : "Generate Reports",
                    "e" : "Exit"}

    main_menu_choice = display_menu(menu_description, main_menu, curr_user, True)

    if main_menu_choice == 'r':
        reg_user()

    elif main_menu_choice == 'a':
        add_task()

    elif main_menu_choice == 'va':
        view_all()  

    elif main_menu_choice == 'vm':
        view_mine(curr_user)

    elif main_menu_choice == 'gr':
        generate_reports(usernames_passwords)

    elif main_menu_choice == 'ds' and curr_user == 'admin':
        if not os.path.exists("user_overview.txt") or not os.path.exists("task_overview.txt"):
            generate_reports(usernames_passwords)
        display_stats()
   
    elif main_menu_choice == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")