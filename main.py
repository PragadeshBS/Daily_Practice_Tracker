from datetime import date
from datetime import datetime
from datetime import timedelta
from os import system, name
from random import randint
import sys
from calendar import day_name
from cryptography.fernet import Fernet
import cryptography

key = "68LMAwnm6-WMy3bNzOporMrph5_g27mzhKF77MYJIbc="

f = Fernet(key)


def encrypt_file(file_name):
    with open(file_name, "r") as file_r:
        insecure_content = file_r.read()
    secure_content = encrypt(insecure_content)
    with open(file_name, "wb") as file_w:
        file_w.write(secure_content)


def decrypt_file(file_name):
    with open(file_name, "rb") as file_r:
        secure_content = file_r.read()
    insecure_content = decrypt(secure_content)
    with open(file_name, "w") as file_w:
        file_w.write(insecure_content)


def encrypt(message):
    encoded_message = message.encode()
    encrypted = f.encrypt(encoded_message)
    return encrypted


def decrypt(message):
    decrypted = f.decrypt(message)
    output = decrypted.decode()
    return output


daily_goal = 0
today_date = date.today()
yesterday_date = today_date - timedelta(days=1)
today_weekday = day_name[today_date.weekday()]
master_total = 0
streak = streak_status = 0
user_name = None
remaining_questions_today = remaining_questions_yesterday = 0
current = datetime.now()
current_date = current.strftime("%d")
current_month = current.strftime("%B")
current_year = current.strftime("%Y")
first_launch = True


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def remaining_qs_unpacker():
    global remaining_questions_today, remaining_questions_yesterday, streak_status, streak, current_month, current_year, current_date
    decrypt_file("data.txt")
    with open("data.txt", "r") as file:
        content = file.readlines()
    encrypt_file("data.txt")
    streak = int(content[5][8:])
    streak_status = int(content[6][15:])
    remaining_questions_list = content[2][14:].split(", ")
    remaining_questions_list = [int(i) for i in remaining_questions_list]
    remaining_questions_yesterday = remaining_questions_list[0]
    remaining_questions_today = remaining_questions_list[1]
    current_date = content[7][8:len(content[7])-1]
    current_month = content[8][8:len(content[8])-1]
    current_year = content[9][8:len(content[9])-1]


def error_handler(code):
    print("Oops, looks like we have run into an error :(")
    if code == 0:
        print("Some files are missing or they might be tampered with")
    elif code == 1:
        print("Some files are corrupt. Try reinstalling the program")
    input("\nPress 'Enter' to exit the program >>")
    sys.exit()


def __init__():
    global daily_goal, user_name, master_total, current_date, current_month, current_year, first_launch
    try:
        file_check = open("data.txt", "r")
        file2_check = open("data.txt", "r")
        file_check.close()
        file2_check.close()
    except FileNotFoundError:
        error_handler(0)
    try:
        decrypt_file("data.txt")
        encrypt_file("data.txt")
        decrypt_file("quotes.txt")
        encrypt_file("quotes.txt")
    except cryptography.fernet.InvalidToken:
        error_handler(1)
    decrypt_file("data.txt")
    with open("data.txt", "r") as file:
        content = file.readlines()
        if content:
            if content[0][:16] == "Not first launch":
                first_launch = False
    encrypt_file("data.txt")
    if not first_launch:
        remaining_qs_unpacker()
        daily_goal = int(content[1][12:])
        master_total = int(content[4][14:])
        question_remaining_till_yesterday()
        user_name = content[3][11:len(content[3])-1]
        streak_update()
        today_register()
        greet("old")
        save_changes(user_name, daily_goal)
        return
    user_name = input("Hello, please enter your name >>")
    attempts = 0
    while (len(user_name) <= 3) and (attempts < 2):
        user_name = input("Name should have more than 3 characters. Please enter a valid name >>")
        if (attempts == 0) and (len(user_name) <= 3):
            print("\nYou have entered an invalid name repeatedly, this is your last try")
            print("If you enter an invalid name again, for now we will assume your name as 'User'")
            print("You can change your name anytime later\n")
        attempts += 1
    if (attempts == 2) and (len(user_name) <= 3):
        user_name = "User"
    greet("new")
    decrypt_file("data.txt")
    with open("data.txt", "w") as file_write:
        file_write.seek(0)
        file_write.write(f"Not first launch\nDaily goal: {daily_goal}\nRemaining qs: 0, {daily_goal}\nuser_name: {user_name}\nMaster total: 0\nStreak: 0\nStreak status: 0\nStartd: {current_date}\nStartm: {current_month}\nStarty: {current_year}")
    encrypt_file("data.txt")
    today_register()


def greet(status, recall=False):
    global first_launch, user_name, remaining_questions_yesterday, remaining_questions_today, daily_goal, today_weekday, master_total, streak, current_date, current_month, current_year
    current_time = datetime.now()
    if current_time.hour < 12:
        time_greet = "Good Morning"
    elif current_time.hour < 16:
        time_greet = "Good afternoon"
    else:
        time_greet = "Good evening"
    if status == "old":
        if recall:
            days_count = days_since_start()
            out_string = ""
            if days_count >= 5:
                out_string = f"for {days_count} days "
            print(f"Hello {user_name}. Tracking your progress {out_string}since {current_date} {current_month} {current_year}\n")
        else:
            print(f"{time_greet} {user_name}...Glad to see you back!")
        if master_total > 1:
            print(f"You have solved {master_total} problems in total, keep going")
        elif master_total == 1:
            print("You have solved 1 question in total, keep going")
        else:
            print("You have not solved any questions yet")
        print(f"Your current streak is {streak}\n")
        if (remaining_questions_yesterday == 0) and (remaining_questions_today == 0):
            print("You currently have no questions to solve, that's great!")
            print(f"This is superb! Keep up the good work. Happy {today_weekday}!")
            print("P.S. Increase your daily goal if you want to solve and keep track of more questions from tomorrow")
        elif remaining_questions_yesterday == 0:
            if remaining_questions_today > 1:
                print(f"You currently have {remaining_questions_today} questions to solve for today")
            else:
                print("You currently have just one question for today, solve it soon")
            print(f"Having no backlog is always good. Finish the work soon and have a great {today_weekday}!")
        else:
            if remaining_questions_yesterday > 1:
                print(f"You still have to solve {remaining_questions_yesterday} questions from your backlog")
            else:
                print(f"You still have a question to solve from your backlog")
            print("\nProcrastination is not good, solve the questions soon :)")
            if recall:
                print("Here's another quote for you...\n")
            else:
                print("Here's a quote for you...\n")
            decrypt_file("quotes.txt")
            with open("quotes.txt", "r") as quotes_file:
                quotes = quotes_file.readlines()
                quote_no = randint(0, len(quotes) - 1)
                print(quotes[quote_no])
            encrypt_file("quotes.txt")
    elif status == "new":
        clear()
        print(f"Welcome {user_name}...")
        print("How many questions would you like to solve daily?")
        daily_goal = input("Set a daily goal between 1 and 100 (Recommended: 2) >>")
        attempts, default = 0, True
        while attempts <= 3:
            if daily_goal.isdigit():
                daily_goal = int(daily_goal)
                if (daily_goal >= 1) and (daily_goal <= 100):
                    default = False
                    break
            attempts += 1
            if attempts == 2:
                print("\nThis is your last turn to enter a valid daily goal")
                print("If a valid goal is not entered, for now your daily goal will be set to 2")
                print("You can change your daily goal anytime later")
            if attempts < 3:
                daily_goal = input("\nSet a valid daily goal between 1 and 100 (Recommended: 2) >>")
            else:
                break
        if default:
            daily_goal = 2
        print(f"Cool, get ready to solve {daily_goal} or more questions from today to meet your goal")


def days_since_start():
    global current_date, current_month, current_year, first_launch
    date_now = datetime.now()
    if not first_launch:
        old_date_string = f"{current_date} {current_month} {current_year}"
        old_date_obj = datetime.strptime(old_date_string, "%d %B %Y")
        return abs((old_date_obj - date_now).days)
    return -1


def reset():
    decrypt_file("data.txt")
    with open("data.txt", "w") as file:
        file.write("")
    encrypt_file("data.txt")


def streak_update():
    global streak_status, yesterday_date, streak
    decrypt_file("data.txt")
    with open("data.txt", "r+") as file:
        contents = file.readlines()
        last = contents[-1]
        if last[1:11] == str(yesterday_date):
            if streak_status == 1:
                streak_status = 0
            elif streak_status == 0:
                streak = 0
        elif last[1:11] != str(today_date):
            streak_status = streak = 0
    encrypt_file("data.txt")
    return 0


def today_register():
    global today_date, daily_goal, remaining_questions_today
    decrypt_file("data.txt")
    with open("data.txt", "r+") as file:
        contents = file.readlines()
        last = contents[-1]
        if last[1:11] == str(today_date):
            encrypt_file("data.txt")
            return 0
        string_to_write = "\n$" + str(today_date) + "--%%--" + str(daily_goal)
        file.seek(0)
        for content in contents:
            if not content[0] == "$":
                file.write(content)
        file.write(string_to_write)
        file.truncate()
        remaining_questions_today = daily_goal
    encrypt_file("data.txt")
    return 1


def today_qs_register(qs_no):
    global today_date, remaining_questions_today, remaining_questions_yesterday, daily_goal
    if remaining_questions_yesterday == 0:
        remaining_questions_today -= qs_no
    else:
        remaining_questions_yesterday -= qs_no
        if remaining_questions_yesterday < 0:
            remaining_questions_today += remaining_questions_yesterday
            remaining_questions_yesterday = 0
            print("You have solved all questions from your backlog")
        elif remaining_questions_yesterday == 0:
            return 3
        else:
            return 2
    if remaining_questions_today <= 0:
        remaining_questions_today = 0
    decrypt_file("data.txt")
    with open("data.txt", "r+") as file:
        contents = file.readlines()
        today_reg = contents[len(contents) - 1][:17] + str(remaining_questions_today)
        file.seek(0)
        for content in contents:
            if content[1:11] != str(today_date):
                file.write(content)
        file.write(today_reg)
        file.truncate()
    encrypt_file("data.txt")
    return 1


def question_remaining_till_yesterday():
    global remaining_questions_yesterday, today_date, daily_goal
    decrypt_file("data.txt")
    with open("data.txt", "r") as file_read:
        contents = file_read.readlines()
    encrypt_file("data.txt")
    for content in contents:
        if content[0] == "$":
            if content[1:11] != str(today_date):
                remaining_questions_yesterday += int(content[17:])
    most_recent = contents[-1]
    if most_recent[0] == "$":
        if most_recent[1:11] != str(today_date):
            most_recent = most_recent[1:11].split("-")
            most_recent = [int(i) for i in most_recent]
            most_recent_date = date(most_recent[0], most_recent[1], most_recent[2])
            difference = today_date - most_recent_date
            remaining_questions_yesterday += (difference.days - 1) * daily_goal
    return 1


def save_changes(new_user_name, new_daily_goal):
    global remaining_questions_today, remaining_questions_yesterday, master_total, streak, streak_status, current_date, current_month, current_year
    decrypt_file("data.txt")
    with open("data.txt", "r+") as file:
        contents = file.readlines()
        initial_string = f"Not first launch\nDaily goal: {new_daily_goal}\nRemaining qs: {remaining_questions_yesterday}, {remaining_questions_today}\nuser_name: {new_user_name}\nMaster total: {master_total}\nStreak: {streak}\nStreak status: {streak_status}\nStartd: {current_date}\nStartm: {current_month}\nStarty: {current_year}\n"
        file.seek(0)
        file.write(initial_string)
        for content in contents[10:]:
            if content[1:11] == str(today_date):
                file.write(content)
        file.truncate()
    encrypt_file("data.txt")


def user_handler():
    global daily_goal, user_name, remaining_questions_yesterday, remaining_questions_today, master_total, streak, streak_status
    while True:
        user_input = input("\nTry 'help' for a list of commands >>").lower().strip()
        if user_input == "help":
            clear()
            print("\n'e' - to enter the number of questions that you solved")
            print("Older questions will be first marked as solved.")
            print("So if you have a backlog, the entered number will first be deducted from backlog number")
            print("\n'v' - to view the number of pending questions if you have any")
            print("\n'cd' - to change your daily goal")
            print("\n'cn' - to change your name")
            print("\n'exit' - to save changes and quit the program, please use this command to quit")
            print("Do not use the close button of this window to quit the program")
            print("If not some of your records might not get saved")
            print("\n'delete' - to delete your records and reset the program")
        elif user_input == "v":
            clear()
            greet("old", True)
        elif user_input == "delete":
            clear()
            print("\nThis will permanently delete your records, are you sure?")
            confirmation = input("Enter 'YES' to proceed >>").strip()
            if confirmation == "YES":
                reset()
                clear()
                print("\nRecords were successfully deleted, a program restart is needed")
                input("Press Enter to exit the program >>")
                sys.exit()
            elif confirmation.lower() == "yes":
                clear()
                print("\nEnter 'YES' as such in uppercase to delete records. Records were not deleted now")
            elif (confirmation.lower() == "n") or (confirmation.lower() == "no"):
                clear()
                print("\nRecords were not deleted")
            else:
                clear()
                print("\nThat was not expected. Records were not deleted")
        elif user_input == "e":
            clear()
            num = input("Enter the number of questions you have solved, just press 'Enter' for a single question >>")
            attempts, update = 0, False
            while attempts <= 3:
                if num.isdigit():
                    num = int(num)
                    if num >= 1:
                        update = True
                        break
                if not num:
                    num = 1
                    update = True
                    break
                attempts += 1
                if attempts == 2:
                    print("\nThis is your last turn to enter a valid number")
                    print("If a valid number is not entered, for now we will not update your records")
                    print("You can enter the number of questions you solved anytime later")
                if attempts < 3:
                    num = input("\nEnter a valid number of questions that you have solved, just press 'Enter' for a single question >>")
                else:
                    break
            if update:
                value = today_qs_register(num)
                master_total += num
            else:
                print("Your records were not updated, try again")
                continue
            clear()
            if value == 1:
                save_changes(user_name, daily_goal)
                if remaining_questions_today == 0:
                    if streak_status == 0:
                        streak += 1
                        streak_status = 1
                    print("Looks like you have achieved your daily goal...")
                    print("This is superb! Keep up the good work! See you tomorrow")
                else:
                    print("Some of today's questions were marked as solved")
                    print(f"You have to solve {remaining_questions_today} more to meet your daily goal")
            elif value == 2:
                save_changes(user_name, daily_goal)
                print("Some of your previous questions are now marked as solved")
                print("Solve more questions to put an end to your backlog")
            elif value == 3:
                save_changes(user_name, daily_goal)
                print("Good, you have solved all questions from your backlog")
                print("Try solving more to reach your goal")

        elif user_input == "cd":
            clear()
            if not ((remaining_questions_yesterday == 0) and (remaining_questions_today == 0)):
                print("You need to solve all remaining questions to modify your daily goal")
                continue
            print("\nHow many questions would you like to solve daily?")
            new_goal = input("Set a new daily goal between 1 and 100 (Recommended: 2) >>")
            attempts, update = 0, False
            while attempts <= 3:
                if new_goal.isdigit():
                    new_goal = int(new_goal)
                    if (new_goal >= 1) and (new_goal <= 100):
                        update = True
                        break
                attempts += 1
                if attempts == 2:
                    print("\nThis is your last turn to enter a valid new daily goal")
                    print("If a valid goal is not entered, for now your daily goal will not be updated")
                    print("You can again update your daily goal anytime later")
                if attempts < 3:
                    new_goal = input("\nSet a valid daily goal between 1 and 100 (Recommended: 2) >>")
                else:
                    break
            if update:
                if new_goal == daily_goal:
                    print(f"Your daily goal is already {daily_goal}")
                else:
                    clear()
                    daily_goal = new_goal
                    save_changes(user_name, daily_goal)
                    print("Your daily goal has been successfully changed")
                    print(f"You will be required to solve {daily_goal} questions from tomorrow")
            else:
                print("Your daily goal was not updated")

        elif user_input == "cn":
            clear()
            new_name = input("Enter your new name >>")
            name_attempts = 0
            while (len(new_name) <= 3) and (name_attempts < 2):
                new_name = input("Name should have more than 3 characters. Please enter a valid name >>")
                if (name_attempts == 0) and (len(new_name) <= 3):
                    print("\nYou have entered an invalid name repeatedly, this is your last try")
                    print("If you enter an invalid name again, for now we will not change your name")
                    print("You can change your name anytime later\n")
                name_attempts += 1
            if (name_attempts == 2) and (len(new_name) <= 3):
                print("You have entered an invalid name repeatedly, for now your name will not be changed")
                print("You can change your name anytime later")
                continue
            if new_name.lower() == user_name.lower():
                clear()
                print(f"Your old name was already {new_name}")
            else:
                clear()
                user_name = new_name
                save_changes(user_name, daily_goal)
                print(f"Your name has been successfully changed. Hello {user_name}!")

        elif user_input == "exit":
            save_changes(user_name, daily_goal)
            sys.exit()

        else:
            print("That was not expected, try 'help' for a list of commands")


if __name__ == "__main__":
    __init__()

user_handler()
