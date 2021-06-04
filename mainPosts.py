''' Outputs a .csv file that tracks a set of Instagram Profiles based on a selection of posts '''
import instaloader
import configparser
import json
import urllib.request
import csv

def vpn_check():
    ''' Checks if a VPN is currently running based on IP '''

    GEO_IP_API_URL  = 'http://ip-api.com/json/'
    original_country = 'Greece'

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
    print(f"Posts loaded successfully: {posts_list}.")

    return (posts_list)

def get_and_store_likes(post):
    ''' Gets a list of all the Profiles that liked the given Post and stores them on a File '''

    print(f"Processing {post}...")
    
    profiles_list = post.get_likes()



    with open('data/temp.txt', "a+") as f:
        for profile in profiles_list:
            f.write(str(profile.userid) + '\n')

    print(f"Updated output File.")


''' Run Main Function '''
# Load/Read Input .CSV 
f = open("data/source.csv", "r", newline='')
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

print(f"CSV file successfully loaded.")

# Write to Output .CSV 
f = open("data/source.csv", "w", newline='')
print(list(data.values()))
csv_writer = csv.DictWriter(f, fieldnames=data_columnnames)
csv_writer.writeheader()
for row in list(data.values()):
    csv_writer.writerow(row)
f.close()


quit()


print(f"Starting...")

vpn_check()

# Config Parsing
config = configparser.ConfigParser()
config.read('config/config.ini')

# Initiate InstaLoader
InstaLoader = instaloader.Instaloader()

# Run Log In
mode = config['Settings']['login_mode']
if mode == "file":
    InstaLoader.load_session_from_file(config['Settings']['username'])  # Load Session created with `instaloader -l USERNAME`
else:
    InstaLoader.login(config['Settings']['username'], config['Settings']['password'])  # Traditional log in Method, bugged https://github.com/instaloader/instaloader/issues/1150
print(f"Logged in successfully.\n")

# Load/Read Input .CSV 
...

posts_list = posts_parse(InstaLoader)

for post in posts_list:
    get_and_store_likes(post)




# INSTAGRAM SCRAPER
# instagram-scraper j.touni -u thodoris_xrysikos -p fagaabvadaa2xC3Casd2 -t story --filter-location 109790383963906 --include-location --location
# instagram-scraper --tag athens -u thodoris_xrysikos -p fagaabvadaa2xC3Casd2 -t story --include-location --filter-location 109790383963906
# instagram-scraper trolololer86 -u thodoris_xrysikos -p fagaabvadaa2xC3Casd2 -t story --filter-location 14294616 --include-location --location