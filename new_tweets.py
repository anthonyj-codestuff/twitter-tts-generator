import os
import datetime
import subprocess
import constants as c

def read_last_run_date():
    if os.path.exists("last-run.txt"):
        with open("last-run.txt", "r") as file:
            date_str = file.read().strip()
            try:
                last_run_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return last_run_date
            except ValueError:
                pass
    return None

def write_last_run_date(date):
    with open("last-run.txt", "w") as file:
        file.write(date.strftime("%Y-%m-%d"))

def get():
    last_run_date = read_last_run_date()
    if last_run_date:
        print("Last run date:", last_run_date.strftime("%Y-%m-%d"))
        year = last_run_date.year
        month = last_run_date.month
        day = last_run_date.day
        print("Running batch file with:", year, month, day)
        print(f"subprocess.run(['get-new-tweets.bat', {c.PATH}, {str(year)}, {str(month)}, {str(day)}, {c.MAIN_ACCOUNT}])")
        subprocess.run(["get-new-tweets.bat", c.PATH, str(year), str(month), str(day), c.MAIN_ACCOUNT])  
    current_date = datetime.datetime.now()
    write_last_run_date(current_date)
    print("Updated last run date:", current_date.strftime("%Y-%m-%d"))
