import os
import datetime
import subprocess
import constants as c
import file_handlers as fileUtils
import funcs as funcs

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
    def fetchParentTweets():
        children = funcs.pickTweetsByUser(c.MAIN_ACCOUNT)
        parents = []
        fileUtils.addLogToFile(f"Checking {len(children)} children for missing parents. This might take a while...", True)
        for child in children:
            file = os.path.join(c.TWEETS_DIR, child)
            data = fileUtils.loadJSONData(file, ["reply_id", "reply_to"])
            if not data["reply_id"] or not data["reply_to"]:
                continue
            # parent exists, check if file is already downloaded
            parentFilename = fileUtils.findParentTweetById(data["reply_id"])
            if parentFilename:
                # parent file already exists
                continue
            # parent does not exist
            parents.append([
                    data["reply_to"],
                    data["reply_id"]
                ])
        fileUtils.addLogToFile(f"Found {len(parents)} missing parents", True)
        for p in parents:
            log = f"Fetching missing parent [{p}]"
            print(log)
            fileUtils.addLogToFile(p)
            subprocess.run(["get-new-tweet-individual.bat", c.PATH, p[0], str(p[1])])
    
    if not c.FETCH_NEW_TWEETS:
        fileUtils.addLogToFile("Fetching new child tweets disabled. Skipping...")
    else:
        if c.CUSTOM_FETCH_RANGE:
            # TODO This doesn't seem to work very well
            p = c.CUSTOM_FETCH_PARAMS
            if not (isinstance(p, list) and len(p) == 6 and all(isinstance(num, int) and num > 0 for num in p)):
                fileUtils.addLogToFile(f"custom fetch params must be an array of 6 non-negative integers")
                return
            print(f"Running custom batch file with: {p[0]}-{p[1]}-{p[2]} -> {p[3]}-{p[4]}-{p[5]}")
            print(f"\"{c.PATH}\gallery-dl.exe\" https://twitter.com/{c.MAIN_ACCOUNT}/ --filter \"date >= datetime({str(p[0])}, {str(p[1])}, {str(p[2])}) and date < datetime({str(p[3])}, {str(p[4])}, {str(p[5])}) or abort()\"")
            subprocess.run(["get-new-tweets-range.bat", c.PATH, str(p[0]), str(p[1]), str(p[2]), str(p[3]), str(p[4]), str(p[5]), c.MAIN_ACCOUNT])
        else:
            last_run_date = readLastRunDate()
            if last_run_date:
                print("Last run date:", last_run_date.strftime("%Y-%m-%d"))
                year = last_run_date.year
                month = last_run_date.month
                day = last_run_date.day
                print(f"Running standard batch file with: {year}-{month}-{day}")
                subprocess.run(["get-new-tweets.bat", c.PATH, str(year), str(month), str(day), c.MAIN_ACCOUNT])
            else:
                log = "No last run date found. Nothing to fetch"
                fileUtils.addLogToFile(log)
                print(log)
            current_date = datetime.datetime.now()
            writeLastRunDate(current_date)
            print("Updated last run date:", current_date.strftime("%Y-%m-%d"))
        count = len([name for name in os.listdir(c.TWEETS_DIR) if os.path.isfile(os.path.join(c.TWEETS_DIR, name))])
        fileUtils.addLogToFile(f"Found {count} total files after fetch")
    # double-check for orphaned tweets (this sometimes happens)
    if c.FETCH_MISSING_PARENT_TWEETS:
        fileUtils.addLogToFile("Checking for missing parents.")
        fetchParentTweets()
