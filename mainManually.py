''' Updates a .csv file based on Instagram usernames manually inserted by the user - The goal is to track a set of Instagram Profiles '''
import instaloader
import configparser
import csv
import sys
from collections import defaultdict, OrderedDict

def update_profile(username, data, data_columnnames, data_fastset, InstaLoader):
    ''' Parses a single user Profile and stores it on a Dict data Structure '''

    profile = instaloader.Profile.from_username(InstaLoader.context, username)

    id = profile.userid
    username = profile.username
    
    print(f"\nProcessing Profile: /{username}")

    data = defaultdict(OrderedDict,data)  # A more appropriate data type for direct assignment of values

    # Update Data Structure
    if id in data_fastset:  # Existing Row
        data[id][data_columnnames[0]] = "https://www.instagram.com/" + profile.username + "/"
        data[id][data_columnnames[1]] = profile.userid
        data[id][data_columnnames[2]] = profile.username
        data[id][data_columnnames[3]] = not profile.is_private
        data[id][data_columnnames[4]] = data[id][data_columnnames[4]] + ", " + "manually"
        data[id][data_columnnames[5]] = data[id][data_columnnames[5]]
        data[id][data_columnnames[6]] = profile.has_public_story
        data[id][data_columnnames[7]] = data[id][data_columnnames[7]]
        data[id][data_columnnames[8]] = data[id][data_columnnames[8]]  
    else:                   # New Row
        data[id][data_columnnames[0]] = "https://www.instagram.com/" + profile.username + "/"
        data[id][data_columnnames[1]] = profile.userid
        data[id][data_columnnames[2]] = profile.username
        data[id][data_columnnames[3]] = not profile.is_private
        data[id][data_columnnames[4]] = "manually"
        data[id][data_columnnames[5]] = ""
        data[id][data_columnnames[6]] = profile.has_public_story
        data[id][data_columnnames[7]] = ""
        data[id][data_columnnames[8]] = ""
    print(f"Profile {id} scraped successfully.")

    return (data)

def load_csv(mode):
    ''' Load/Read Input .CSV '''

    if mode == "1":
        filepath = "data/source.csv"
    elif mode == "2":
        filepath = "data/source_partial.csv"

    f = open(filepath, "r", newline='')
    csv_reader = csv.DictReader(f)
    data = {}
    data_columnnames = ['instagram_url','instagram_id','instagram_name','is_public','done_posts','high_priority','has_story_available','score','notes']

    for row in csv_reader:
        data[int(row['instagram_id'])] = row

    data_fastset = set(data.keys())  # A 'set' object of just the IDs

    if len(data_columnnames) == len(data[next(iter(data))]):
        print(f"Number of columns of input .csv matches the expected value: {len(data_columnnames)}")
    else:
        raise Exception(f"Error, Number of columns of input .csv does not match the expected value. Change the 'data_columnnames' variable.")

    f.close()
    print(f"CSV file successfully loaded.")

    return (data, data_columnnames, data_fastset)

def save_csv(mode, data, data_columnnames):
    ''' Write to Output .CSV '''

    if mode == "1":
        filepath = "data/source.csv"
    elif mode == "2":
        filepath = "data/source_partial.csv"

    f = open(filepath, "w", newline='')
    csv_writer = csv.DictWriter(f, fieldnames=data_columnnames)
    csv_writer.writeheader()
    for row in list(data.values()):
        csv_writer.writerow(row)

    f.close()


''' Run Main Function '''
print(f"Starting...")

# Config Parsing
config = configparser.ConfigParser()
config.read('config/config.ini')

# Initiate InstaLoader
InstaLoader = instaloader.Instaloader()

# Run Log In
login_mode = config['Settings']['login_mode']
if login_mode == "file":
    InstaLoader.load_session_from_file(config['Settings']['username'])  # Load Session created with `instaloader -l USERNAME`
else:
    InstaLoader.login(config['Settings']['username'], config['Settings']['password'])  # Traditional log in Method, bugged https://github.com/instaloader/instaloader/issues/1150
print(f"Logged in successfully.\n")

user_input = ""

while True:
    # User Input of an Instagram username
    print(f"Insert an Instagram username to be Updated (Q to Quit): ")
    user_input = sys.stdin.readline().strip() 

    if user_input.lower() in ["q", "quit", "exit"]:
        break

    # Load/Read Input .CSV
    (data, data_columnnames, data_fastset) = load_csv("1")

    data = update_profile(user_input, data, data_columnnames, data_fastset, InstaLoader)

    # Write to final Output .CSV
    save_csv("1", data, data_columnnames)
    print(f"Successfully wrote to Final CSV file.\n")    
