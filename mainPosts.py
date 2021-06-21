''' Updates a .csv file based on a selection of posts - The goal is to track a set of Instagram Profiles '''
import instaloader
import configparser
import json
import urllib.request
import csv
import sys
import os
from datetime import datetime
from collections import defaultdict, OrderedDict

def vpn_check():
    ''' Checks if a VPN is currently running based on IP '''

    GEO_IP_API_URL  = 'http://ip-api.com/json/'
    original_country = 'Any'

    # Creating request object to GeoLocation API
    req             = urllib.request.Request(GEO_IP_API_URL)
    # Getting response in JSON
    response        = urllib.request.urlopen(req).read()
    # Loading JSON from text to object
    json_response   = json.loads(response.decode('utf-8'))

    if json_response['country'] == original_country:
        raise Exception(f"Error, VPN is not Running, current IP belongs to '{original_country}'. Run a VPN or change the 'original_country' variable.")

    print(f"Current Country of IP: {json_response['country']}.")

def posts_parse(InstaLoader):
    ''' Parses and returns the Source Posts to be tracked '''

    with open('tracking/ActivePosts.txt', "r") as f:
        posts_raw = f.read().splitlines()
        posts_raw = [x.split('/')[-2] for x in posts_raw]

    print(f"Loading Source Posts to be Tracked.")
    posts_list = [instaloader.Post.from_shortcode(InstaLoader.context, x) for x in posts_raw]  # 'Post' Object
    print(f"Posts loaded successfully: {posts_list}.\n")

    return (posts_list)

def get_and_store_likes(post, data, data_columnnames, data_fastset, exclude_fastset, save_every):
    ''' Gets a list of all the Profiles that liked the given Post and stores them on a Dict data Structure '''

    print(f"Processing {post}...")
    
    profiles_list = post.get_likes()

    data = defaultdict(OrderedDict,data)  # A more appropriate data type for direct assignment of values

    count = 0
    items_to_save = []

    # Update Data Structure
    for profile in profiles_list:
        id = profile.userid

        # Debug
        # print(temp_profile.username)
        # print(temp_profile.has_public_story)
        # print(temp_profile.has_viewable_story)
        # quit()

        if id not in exclude_fastset:
            if id in data_fastset:  # Existing Row
                data[id][data_columnnames[0]] = "https://www.instagram.com/" + profile.username + "/"
                data[id][data_columnnames[1]] = profile.userid
                data[id][data_columnnames[2]] = profile.username
                data[id][data_columnnames[3]] = data[id][data_columnnames[3]]
                data[id][data_columnnames[4]] = data[id][data_columnnames[4]] + ", " + post.owner_username + post.shortcode
                data[id][data_columnnames[5]] = data[id][data_columnnames[5]]
                data[id][data_columnnames[6]] = data[id][data_columnnames[6]]
                data[id][data_columnnames[7]] = data[id][data_columnnames[7]]
                data[id][data_columnnames[8]] = data[id][data_columnnames[8]]  
            else:                   # New Row
                data[id][data_columnnames[0]] = "https://www.instagram.com/" + profile.username + "/"
                data[id][data_columnnames[1]] = profile.userid
                data[id][data_columnnames[2]] = profile.username
                data[id][data_columnnames[3]] = not profile.is_private
                data[id][data_columnnames[4]] = post.owner_username + post.shortcode
                data[id][data_columnnames[5]] = ""
                data[id][data_columnnames[6]] = profile.has_public_story
                data[id][data_columnnames[7]] = ""
                data[id][data_columnnames[8]] = ""
            print(f"Profile {id} scraped successfully.")

            count += 1
            items_to_save.append(id)
        else:
            print(f"Profile {id} has already been scraped in a previous Run.")

        # Perform a BackUp of the Data Structure so far. Can be used as a partial Run later in the form of input data.
        if count == save_every:
            current_time = datetime.now()
            current_time = current_time.strftime("%m/%d/%Y, %H:%M:%S")
            log_text = f"-- {current_time} : Performed a BackUp of {save_every} Items. --"
            with open("data/partial_run_log.txt", "a") as f:
                f.write("[" + log_text + "]\n")
                for item in items_to_save:
                    f.write(str(item) + "\n")
            print(log_text)
            save_csv("2", data, data_columnnames)
            count = 0
            items_to_save = []

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
vpn_check()

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

# Ask user for Run Mode ~ Mode=1: Fresh Run, Mode=2: Continue Previous Run
print(f"Select a Run Mode ~ (1): Fresh Run, (2): Continue Previous Partial Run: ")
mode = sys.stdin.readline().strip() 

# Load/Read Input .CSV
if mode == "1":  # Fresh Run
    (data, data_columnnames, data_fastset) = load_csv(mode)
    exclude_fastset = set()

    if os.path.isfile('data/source_partial.csv'):
        current_time = datetime.now()
        os.rename('data/source_partial.csv', 'data/source_partial_wiped_' + current_time.strftime("%m%d%Y_%H%M%S") + '.csv')
        os.rename('data/partial_run_log.txt', 'data/partial_run_log_wiped_' + current_time.strftime("%m%d%Y_%H%M%S") + '.txt')
        print(f"Wiped previous Partial Runs by renaming the Files.")
elif mode == "2":  # Previous Partial Run
    (data, data_columnnames, data_fastset) = load_csv(mode)
    exclude_fastset = set()

    with open('data/partial_run_log.txt', "r") as f:
        temp = f.read().splitlines()
        for line in temp:
            if line.startswith("[") == False:
                exclude_fastset.add(int(line))
else:
    raise Exception(f"Error, Input Mode is not valid. Please enter one of the two possible Options.")

# Parse Source Posts
posts_list = posts_parse(InstaLoader)

for post in posts_list:
    data = get_and_store_likes(post, data, data_columnnames, data_fastset, exclude_fastset, int(config['Settings']['save_every']))

# Write to final Output .CSV
save_csv("1", data, data_columnnames)
print(f"Successfully wrote to Final CSV file.")
