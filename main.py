from tkinter import *
import datetime
import calendar
from random import randint

window = Tk()
window.title("Aptitude Practice Tracker")
window.geometry("500x500")
# Icon path goes here... ***window.iconbitmap("")
# Data text file path goes here... ***data_file = ""
# Quotes file path goes here... ***quotes_file_path = "" 

def set_variables():
    global first_launch, user_name, today_date, yesterday_date, today_weekday, master_total
    global current, current_date, current_month, current_year, streak, streak_status, remaining_questions_today
    global remaining_questions_yesterday, daily_goal

    first_launch = True
    user_name = "User"
    today_date = datetime.date.today()
    yesterday_date = today_date - datetime.timedelta(days=1)
    today_weekday = calendar.day_name[today_date.weekday()]
    master_total = streak = streak_status = remaining_questions_today = remaining_questions_yesterday = daily_goal = 0
    current = datetime.datetime.now()
    current_date = current.strftime("%d")
    current_month = current.strftime("%B")
    current_year = current.strftime("%Y")

def popup(message, timeout=2000, font_color="Black"):
    popup_label = Label(window, text=message, wraplength=200, padx=20, fg=font_color, font=('arial', 11))
    popup_label.grid()
    popup_label.after(timeout, popup_label.grid_remove)

def __init__():
    global first_launch, daily_goal, master_total, user_name, data_file

    set_variables()
    
    try:
        with open(data_file, "r") as file:
            content = file.readlines()
        with open(quotes_file_path, "r") as quotes_file:
            pass
    except FileNotFoundError:
        error_label_text = "We've run into an error :("
        more_error_info_text = "\n\nSome files could not be found"
        error_label = Label(window, text=error_label_text, fg="red", font=('arial', 15))
        more_error_info_label = Label(window, text=more_error_info_text, font=('arial', 11))
        error_label.grid()
        more_error_info_label.grid()
        return

    if content:
        if content[0][:16] == "Not first launch":
            first_launch = False

    if first_launch:
        first_launch_handler()
        return

    extract_data()
    question_remaining_till_yesterday()
    streak_update()
    today_register()
    save_changes(user_name, daily_goal)
    main_screen()

def extract_data():
    global remaining_questions_today, remaining_questions_yesterday, streak_status, user_name
    global current_date, current_year, streak, current_month, daily_goal, master_total, data_file
    with open(data_file, "r") as file:
        content = file.readlines()
    streak = int(content[5][8:])
    streak_status = int(content[6][15:])
    daily_goal = int(content[1][12:])
    master_total = int(content[4][14:])
    user_name = content[3][11:len(content[3]) - 1]
    remaining_questions_list = content[2][14:].split(", ")
    remaining_questions_list = [int(i) for i in remaining_questions_list]
    remaining_questions_yesterday = remaining_questions_list[0]
    remaining_questions_today = remaining_questions_list[1]
    current_date = content[7][12:len(content[7]) - 1]
    current_month = content[8][13:len(content[8]) - 1]
    current_year = content[9][12:len(content[9]) - 1]

def question_remaining_till_yesterday():
    global remaining_questions_yesterday, today_date, daily_goal, data_file
    with open(data_file, "r") as file_read:
        contents = file_read.readlines()
    for content in contents:
        if content[0] == "$":
            if content[1:11] != str(today_date):
                remaining_questions_yesterday += int(content[17:])
    most_recent = contents[-1]
    if most_recent[0] == "$":
        if most_recent[1:11] != str(today_date):
            most_recent = most_recent[1:11].split("-")
            most_recent = [int(i) for i in most_recent]
            most_recent_date = datetime.date(most_recent[0], most_recent[1], most_recent[2])
            difference = today_date - most_recent_date
            remaining_questions_yesterday += (difference.days - 1) * daily_goal
    return 1

def streak_update():
    global streak_status, yesterday_date, streak, data_file
    with open(data_file, "r+") as file:
        contents = file.readlines()
        last = contents[-1]
        if last[1:11] == str(yesterday_date):
            if streak_status == 1:
                streak_status = 0
            elif streak_status == 0:
                streak = 0
        elif last[1:11] != str(today_date):
            streak_status = streak = 0
    return 0

def today_register():
    global today_date, daily_goal, remaining_questions_today, data_file
    with open(data_file, "r+") as file:
        contents = file.readlines()
        last = contents[-1]
        if last[1:11] == str(today_date):
            return 0
        string_to_write = "\n$" + str(today_date) + "--%%--" + str(daily_goal)
        file.seek(0)
        for content in contents:
            if not content[0] == "$":
                file.write(content)
        file.write(string_to_write)
        file.truncate()
        remaining_questions_today = daily_goal
    return 1

def save_changes(new_user_name, new_daily_goal):
    global remaining_questions_today, remaining_questions_yesterday, master_total, data_file
    global streak, streak_status, current_date, current_month, current_year
    with open(data_file, "r+") as file:
        contents = file.readlines()
        initial_string = f"Not first launch\nDaily goal: {new_daily_goal}"
        initial_string += f"\nRemaining qs: {remaining_questions_yesterday}, {remaining_questions_today}"
        initial_string += f"\nuser_name: {new_user_name}\nMaster total: {master_total}\nStreak: {streak}"
        initial_string += f"\nStreak status: {streak_status}\nStart_date: {current_date}\nStart_month: {current_month}"
        initial_string += f"\nStart_year: {current_year}\n"
        file.seek(0)
        file.write(initial_string)
        for content in contents[10:]:
            if content[1:11] == str(today_date):
                file.write(content)
        file.truncate()

def menu(code):
    if code == 1:
        menu_bar = Menu(window)
        view = Menu(menu_bar, tearoff=0)
        options = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=view)
        menu_bar.add_cascade(label="Options", menu=options)
        view.add_command(label="More info", command=more_info_screen)
        view.add_command(label="Exit", command=window.destroy)
        options.add_command(label="Change daily goal", command=change_daily_goal_screen)
        options.add_command(label="Change name", command=change_name_screen)
        options.add_command(label="Reset", command=reset_screen)
        window.config(menu=menu_bar)
        return
    remove_menu = Menu(window)
    window.config(menu=remove_menu)

def main_screen():
    global user_name, daily_goal, first_launch, master_total, streak, quotes_file_path

    # Menu section
    menu(1)
    clear_widgets()

    # Greet section
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        time_greet = f"Good Morning {user_name}"
    elif current_time.hour < 16:
        time_greet = f"Good afternoon {user_name}"
    else:
        time_greet = f"Good evening {user_name}"
    greet_message = f"{time_greet}... Glad to see you back!"
    if first_launch:
        if daily_goal == 1:
            greet_message = f"{time_greet}... Get ready to solve a daily question from today!"
        else:
            greet_message = f"{time_greet}... Get ready to solve {daily_goal} questions daily!"
    greet_label = Label(window, text=greet_message, font=('arial', 11))
    greet_label.grid()

    # info section
    info_message = f"\nStreak: {streak}"
    info_label = Label(window, text=info_message, font=('arial', 11))
    info_label.grid()

    # info section continued
    if (remaining_questions_yesterday == 0) and (remaining_questions_today == 0):
        more_info_text = "You currently have no questions to solve, that's great!"
        more_info_text += f"\nKeep up the good work. Happy {today_weekday}!"
        more_info_text += "\n\nP.S. Increase your daily goal if you want to solve"
        more_info_text += " and keep track of more questions from tomorrow"
    elif remaining_questions_yesterday == 0:
        if remaining_questions_today > 1:
            more_info_text = f"You currently have {remaining_questions_today} questions to solve for today"
        else:
            more_info_text = "You currently have just one question for today, solve it soon"
        more_info_text += f"\n\nHaving no backlog is always good."
        more_info_text += f"\nFinish the work soon and have a great {today_weekday}!"
    else:
        if remaining_questions_yesterday > 1:
            more_info_text = f"You still have to solve {remaining_questions_yesterday} questions from your backlog"
        else:
            more_info_text = f"You still have a question to solve from your backlog"
        more_info_text += "\n\nProcrastination is not good, solve the questions soon :)"
        more_info_text += "\n\nHere's a quote for you...\n"
        with open(quotes_file_path, "r") as quotes_file:
            quotes = quotes_file.readlines()
            quote_no = randint(0, len(quotes) - 1)
            more_info_text += quotes[quote_no]
    more_info_label = Label(window, text=more_info_text, font=('arial', 11), wraplength=250)
    more_info_label.grid()

    # enter solved questions
    questions_button = Button(window, text="Solved questions", font=('arial', 11), command=questions_screen)
    questions_button.grid()

def reset_screen():
    clear_widgets()
    menu(0)

    def reset_data():
        global first_launch, data_file
        with open(data_file, "w") as file:
            file.write("")
        clear_widgets()
        first_launch = True
        restart_label_text = "Data was reset successfully, a program restart is required"
        restart_label = Label(window, text=restart_label_text, font=('arial', 11))
        restart_button = Button(window, text="Restart", font=('arial', 11), command=__init__)
        restart_label.grid()
        restart_button.grid()

    back_button = Button(window, text="Back", command=main_screen)
    back_button.grid()
    reset_info_text = "Your data will be permanently erased, do you want to proceed?"
    reset_info_label = Label(window, text=reset_info_text, fg="Red", font=('arial', 11))
    proceed_button = Button(window, text="Reset data", font=('arial', 11), command=reset_data)
    reset_info_label.grid()
    proceed_button.grid()

def days_since_start():
    global current_date, current_month, current_year, first_launch
    date_now = datetime.datetime.now()
    if not first_launch:
        old_date_string = f"{current_date} {current_month} {current_year}"
        old_date_obj = datetime.datetime.strptime(old_date_string, "%d %B %Y")
        return abs((old_date_obj - date_now).days)
    return -1

def more_info_screen():
    global quotes_file_path
    clear_widgets()
    days_count = days_since_start()

    back_button = Button(window, text="Back", command=main_screen)
    back_button.grid()

    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        time_greet = f"Good Morning {user_name}"
    elif current_time.hour < 16:
        time_greet = f"Good afternoon {user_name}"
    else:
        time_greet = f"Good evening {user_name}"
    greet_message = f"{time_greet}, here's your info..."
    greet_label = Label(window, text=greet_message, font=('arial', 11))
    greet_label.grid()

    if days_count >= 5:
        progress_label_text = f"Tracking your progress for {days_count} days "
        progress_label_text += f"since {current_date} {current_month} {current_year}"
        progress_label = Label(window, text=progress_label_text, font=('arial', 11))
        progress_label.grid()
    daily_goal_label_text = f"Daily goal: {daily_goal}"
    daily_goal_label = Label(window, text=daily_goal_label_text, font=('arial', 11))
    daily_goal_label.grid()

    # info section
    info_message = f"\nTotal number of questions solved: {master_total}"
    info_message += f"\nStreak: {streak}"
    info_label = Label(window, text=info_message, font=('arial', 11))
    info_label.grid()

    # info section continued
    if (remaining_questions_yesterday == 0) and (remaining_questions_today == 0):
        more_info_text = "You currently have no questions to solve, that's great!"
        more_info_text += f"\nKeep up the good work. Happy {today_weekday}!"
        more_info_text += "\n\nP.S. Increase your daily goal if you want to solve"
        more_info_text += " and keep track of more questions from tomorrow"
    elif remaining_questions_yesterday == 0:
        if remaining_questions_today > 1:
            more_info_text = f"You currently have {remaining_questions_today} questions to solve for today"
        else:
            more_info_text = "You currently have just one question for today, solve it soon"
        more_info_text += f"\n\nHaving no backlog is always good."
        more_info_text += f"\nFinish the work soon and have a great {today_weekday}!"
    else:
        if remaining_questions_yesterday > 1:
            more_info_text = f"You still have to solve {remaining_questions_yesterday} questions from your backlog"
        else:
            more_info_text = f"You still have a question to solve from your backlog"
        more_info_text += "\n\nProcrastination is not good, solve the questions soon :)"
        more_info_text += "\n\nHere's a quote for you...\n"
        with open(quotes_file_path, "r") as quotes_file:
            quotes = quotes_file.readlines()
            quote_no = randint(0, len(quotes) - 1)
            more_info_text += quotes[quote_no]
    more_info_label = Label(window, text=more_info_text, font=('arial', 11), wraplength=300)
    more_info_label.grid()

def today_qs_register(qs_no):
    global today_date, remaining_questions_today, remaining_questions_yesterday, daily_goal, data_file
    to_return = [0, False]
    if remaining_questions_yesterday == 0:
        remaining_questions_today -= qs_no
    else:
        remaining_questions_yesterday -= qs_no
        if remaining_questions_yesterday < 0:
            remaining_questions_today += remaining_questions_yesterday
            remaining_questions_yesterday = 0
            to_return[1] = True
        elif remaining_questions_yesterday == 0:
            to_return[0] = 3
            return to_return
        else:
            to_return[0] = 2
            return to_return
    if remaining_questions_today <= 0:
        remaining_questions_today = 0
    with open(data_file, "r+") as file:
        contents = file.readlines()
        today_reg = contents[len(contents) - 1][:17] + str(remaining_questions_today)
        file.seek(0)
        for content in contents:
            if content[1:11] != str(today_date):
                file.write(content)
        file.write(today_reg)
        file.truncate()
    to_return[0] = 1
    return to_return

def first_launch_handler():
    global user_name, daily_goal
    clear_widgets()
    user_name = StringVar()
    daily_goal = StringVar()
    daily_goal.set("2")
    user_name.set("")

    def submit_details():
        global user_name, daily_goal
        try:
            user_name = name_entry.get()
            assert ((len(user_name) >= 3) and (len(user_name) <= 20))
        except AssertionError:
            popup("Username should have 3-20 characters", font_color="Red")
            return
        try:
            daily_goal = int(daily_goal_entry.get())
            if daily_goal <= 0: raise ValueError
        except ValueError:
            popup("Enter a valid daily goal", font_color="Red")
            return
        clear_widgets()
        if user_name and daily_goal:
            write_first_details()

    welcome_label = Label(window, pady=30, text="Welcome!", font=('arial', 18))

    name_label = Label(window, text="Enter your name: ", font=('arial', 14))
    name_entry = Entry(window, textvariable=user_name, font=('arial', 11))

    daily_goal_label = Label(window, text="Set a daily goal (Recommended 2):", font=('arial', 14))
    daily_goal_entry = Entry(window, textvariable=daily_goal, font=('arial', 11))

    submit_button = Button(window, text="Done", font=('arial', 14), command=submit_details)

    welcome_label.grid(columnspan=2, row=0, ipadx=35, column=0)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    daily_goal_label.grid(row=2, column=0)
    daily_goal_entry.grid(row=2, column=1)
    submit_button.grid(row=3, column=0, columnspan=3, pady=20)

def write_first_details():
    global user_name, daily_goal, data_file
    with open(data_file, "w") as file:
        file.seek(0)
        file.write(f"Not first launch\nDaily goal: {daily_goal}")
        file.write(f"\nRemaining qs: 0, {daily_goal}\nuser_name: {user_name}")
        file.write("\nMaster total: 0\nStreak: 0\nStreak status: 0")
        file.write(f"\nStart_date: {current_date}\nStart_month: {current_month}\nStart_year: {current_year}")
    today_register()
    main_screen()

def questions_screen():
    global daily_goal

    def get_questions():
        global master_total, remaining_questions_today, streak, streak_status
        nonlocal number_of_questions
        try:
            value = int(number_of_questions.get())
            if value <= 0:
                raise ValueError
        except ValueError:
            popup("Enter a valid number of questions, that you have solved", font_color="Red")
            return
        master_total += value
        register = today_qs_register(value)
        if remaining_questions_today == 0:
            if streak_status == 0:
                streak += 1
                streak_status = 1
        after_entry_screen(register)

    clear_widgets()

    back_button = Button(window, text="Back", command=main_screen)
    back_button.grid(row=0, column=0)

    number_of_questions = StringVar()
    number_of_questions.set(str(daily_goal))
    enter_questions_label = Label(window, text="Enter the number of questions you have solved: ", font=('arial', 11))
    enter_questions_entry = Entry(window, textvariable=number_of_questions)
    submit_button = Button(window, text="Done", font=('arial', 11), command=get_questions)
    enter_questions_label.grid()
    enter_questions_entry.grid(row=1, column=1)
    submit_button.grid()

def change_daily_goal_screen():
    global daily_goal

    clear_widgets()

    back_button = Button(window, text="Back", command=main_screen)
    back_button.grid()

    if not ((remaining_questions_yesterday == 0) and (remaining_questions_today == 0)):
        info_label_text = "You need to solve all remaining questions before modifying your daily goal"
        info_label = Label(window, text=info_label_text, fg="Red", font=('arial', 11))
        info_label.grid()
        return

    def after_change():
        global daily_goal
        clear_widgets()
        back_button = Button(window, text="Back", command=main_screen)
        back_button.grid()
        info_label_text = f"Cool, you will have to solve {daily_goal} questions from tomorrow"
        info_label = Label(window, text=info_label_text, fg="green", font=('arial', 11))
        info_label.grid()

    def change_daily_goal():
        global daily_goal, user_name
        nonlocal new_daily_goal
        try:
            value = int(new_daily_goal.get())
            if value <= 0: raise ValueError
        except ValueError:
            popup("Set a valid daily goal", font_color="Red")
            return
        daily_goal = value
        save_changes(user_name, daily_goal)
        after_change()
    
    new_daily_goal = StringVar()

    old_dg_label_text = f"Your current daily goal: {daily_goal}"
    old_dg_label = Label(window, text=old_dg_label_text, font=('arial', 11))

    new_dg_entry_label_text = "Set a new daily goal: "
    new_dg_entry_label = Label(window, text=new_dg_entry_label_text, font=('arial', 11))
    new_dg_entry = Entry(window, textvariable=new_daily_goal)
    submit_button = Button(window, text="Done", command=change_daily_goal)
    old_dg_label.grid()
    new_dg_entry_label.grid()
    new_dg_entry.grid(row=2, column=1)
    submit_button.grid()

def change_name_screen():
    global user_name

    clear_widgets()

    back_button = Button(window, text="Back", command=main_screen)
    back_button.grid()


    def after_change():
        global user_name
        clear_widgets()
        back_button = Button(window, text="Back", command=main_screen)
        back_button.grid()
        info_label_text = f"We got your new name, hello {user_name}!"
        info_label = Label(window, text=info_label_text, fg="green", font=('arial', 11))
        info_label.grid()

    def change_user_name():
        global daily_goal, user_name
        nonlocal new_user_name
        try:
            value = new_user_name.get()
            assert ((len(value) >= 3) and (len(value) <= 20))
        except AssertionError:
            popup("Name should have 3-20 characters", font_color="Red")
            return
        user_name = value
        save_changes(user_name, daily_goal)
        after_change()
    
    new_user_name = StringVar()

    old_un_label_text = f"Hello {user_name}, how can we call you from now?"
    old_un_label = Label(window, text=old_un_label_text, font=('arial', 11))

    new_un_entry_label_text = "Set a new name: "
    new_un_entry_label = Label(window, text=new_un_entry_label_text, font=('arial', 11))
    new_un_entry = Entry(window, textvariable=new_user_name)
    submit_button = Button(window, text="Done", command=change_user_name)
    old_un_label.grid()
    new_un_entry_label.grid()
    new_un_entry.grid(row=2, column=1)
    submit_button.grid()

def after_entry_screen(code):
    global streak_status, streak
    clear_widgets()
    out_message = ""
    save_changes(user_name, daily_goal)
    if code[1]:
        out_message += "You have solved all questions from your backlog"
    if code[0] == 1:
        if remaining_questions_today == 0:
            if streak_status == 0:
                streak += 1
                streak_status = 1
            out_message += "\nLooks like you have achieved your daily goal..."
            out_message += "\nThis is superb! Keep up the good work! See you tomorrow"
        else:
            out_message += "\nSome of today's questions were marked as solved"
            out_message += f"\nYou have to solve {remaining_questions_today} more to meet your daily goal"
    elif code[0] == 2:
        out_message += "\nSome of your previous questions are now marked as solved"
        out_message += "\nSolve more questions to put an end to your backlog"
    elif code[0] == 3:
        out_message += "\nGood, you have solved all questions from your backlog"
        out_message += "\nTry solving more to reach your goal"
    out_message_label = Label(window, text=out_message, font=('arial', 11))
    home_button = Button(window, text="Home", font=('arial', 11), command=main_screen)
    out_message_label.grid()
    home_button.grid()

def clear_widgets():
    widgets = window.winfo_children()
    for widget in widgets:
        widget.grid_remove()

if __name__ == '__main__':
    __init__()

window.mainloop()
