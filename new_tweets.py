import os
import datetime
import subprocess
import constants as c
import file_handlers as fileUtils

def readLastRunDate():
    if os.path.exists("last-run.txt"):
        with open("last-run.txt", "r") as file:
            date_str = file.read().strip()
            try:
                last_run_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return last_run_date
            except ValueError:
                pass
    return None

def writeLastRunDate(date):
    with open("last-run.txt", "w") as file:
        file.write(date.strftime("%Y-%m-%d"))

def get():
    if not c.FETCH_NEW_TWEETS:
        return
    last_run_date = readLastRunDate()
    if last_run_date:
        print("Last run date:", last_run_date.strftime("%Y-%m-%d"))
        year = last_run_date.year
        month = last_run_date.month
        day = last_run_date.day
        print(f"Running batch file with: {year}-{month}-{day}")
        subprocess.run(["get-new-tweets.bat", c.PATH, str(year), str(month), str(day), c.MAIN_ACCOUNT])  
    current_date = datetime.datetime.now()
    writeLastRunDate(current_date)
    print("Updated last run date:", current_date.strftime("%Y-%m-%d"))
    count = len([name for name in os.listdir(c.TWEETS_DIR) if os.path.isfile(os.path.join(c.TWEETS_DIR, name))])
    fileUtils.addLogToFile(f"Found {count} total files after fetch")
