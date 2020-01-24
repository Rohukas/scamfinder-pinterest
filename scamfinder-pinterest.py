# pip install py3-pinterest - https://github.com/bstoilov/py3-pinterest
import time
from py3pin.Pinterest import Pinterest
import json
from datetime import datetime, timedelta
import re
# Pinterest has weird formatting for dates
time_format = "%a, %d %b %Y %H:%M:%S +%f"


# TODO still breaks in some cases. esp. when error codes are present in strings
def find_possible_phone_number(str):

    # Sometimes we have strings that have a single I or O in them
    # ... Can I Uninstall ...
    # This I would be replaced with a 1 later on and cause the number to become invalid.
    # Look for these sorts of situations and remove them!
    clean = re.sub("[a-zA-Z] [IO] [a-zA-Z]", "", str)

    # Filter out words that have more than 3 consequent characters
    clean = "".join(filter(None, re.split(
        '(?:[a-zA-Z]{3,}|[\$\@()+.])+', clean)))

    # Remove all special characters from string
    clean = ''.join(e for e in clean if e.isalnum())
    # Some scammers use 'I' instead of 1 and 'O' instead of 0
    clean = clean.replace("I", "1").replace("O", "0")

    # Regex for phone numbers
    phone_regex = "\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*"
    phone_numbers = re.findall(phone_regex, clean)
    if len(phone_numbers) > 0:
        return "".join(phone_numbers[0])
    return None


# Search function. This searches pinterest for pins
# Leave max_items at 100000, it will stop automatically once there are no more pins to load
# Scope should also be left to default 'pins'
# For the query try being creative.
def search(max_items=100000, scope='pins', query='amazon support number'):
    # After change in pinterest API, you can no longer search for users
    # Instead you need to search for something else and extract the user data from there.
    # current pinterest scopes are: pins, buyable_pins, my_pins, videos, boards
    results = []
    search_batch = pinterest.search(scope=scope, query=query)
    total = 0
    while len(search_batch) > 0 and len(results) < max_items:
        results += search_batch
        search_batch = pinterest.search(scope=scope, query=query)
        # time.sleep(4) # Not necessary after testing. Pinterest dont give a damn :)
        total += len(search_batch)
        print("Searched: {}".format(total))
    return results


def filter_max_age(pins, max_age_days=5):
    filtered = []

    older_than = datetime.today() - timedelta(days=max_age_days)
    for pin in pins:
        created_at = datetime.strptime(pin["created_at"], time_format)
        if created_at > older_than:
            filtered.append(pin)
    return filtered


def get_query():
    return input("Enter search query. Try something like 'amazon customer number' or 'tech support number'.\nQuery: ")


def get_max_age():
    return int(input("Enter max post age.(Tip: you generally dont find posts that are younger than 3-5 days. Enter at least 5 days in order to get good results).\nMax age(days): "))


# Insert your pinterest credentials here.
# I recommend creating a new account as there is always a possibility of getting banned for bot-like behaviour
PINTEREST_EMAIL = "YOUR_EMAIL_HERE"
PINTEREST_PASSWORD = "YOUR_PASSWORD_HERE"
# The username you see in your profile url when you visit your accounts profile
PINTEREST_USERNAME = "YOUR_USERNAME_HERE"


if PINTEREST_EMAIL == "YOUR_EMAIL_HERE" or PINTEREST_PASSWORD == "YOUR_PASSWORD_HERE" or PINTEREST_USERNAME == "YOUR_USERNAME_HERE":
    print("Missing pinterest credentials. Please open the script in a text editor and insert your")
    print("email, password and username into the correct fields.")
    print("If you do not have a pinterest account, you can create one at https://www.pinterest.com/")
    exit()
# Create out pinterest object
pinterest = Pinterest(email=PINTEREST_EMAIL, password=PINTEREST_PASSWORD,
                      username=PINTEREST_USERNAME)


query = get_query()
age = get_max_age()
#results = pinterest.search(scope='pins', query='technical support')
print("Starting...")
results = search(query=query)
filtered = filter_max_age(results, age)

for item in filtered:
    nr_from_description = find_possible_phone_number(item["description"])
    nr_from_title = find_possible_phone_number(item["title"])
    # With the id we can create a url for the post
    # https://www.pinterest.com/pin/ID/
    id = item['id']
    title = item["title"]
    post_url = "https://www.pinterest.com/pin/" + id
    link = item['link']
    if nr_from_description is not None:
        print("[{} days]Parsed nr: {} - {} - {}".format((datetime.now() -
                                                         datetime.strptime(item['created_at'], time_format)).days, nr_from_description, post_url, link))
    elif nr_from_title is not None:
        print("[{} days]Parsed nr: {} - {} - {}".format((datetime.now() -
                                                         datetime.strptime(item['created_at'], time_format)).days, nr_from_title, post_url, link))
