import sys
import json
import os
import argparse
from cod_api import API, platforms
from cod_api.replacements import replacements
import asyncio
import datetime

# Prevent Async error from showing
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initiating the API class
api = API()
COOKIE_FILE = 'cookie.txt'
DIR_NAME = 'stats'
MATCH_DIR_NAME = 'matches'

def save_to_file(data, filename, dir_name='stats'):
    """Utility function to save data to a JSON file."""
    with open(os.path.join(dir_name, filename), 'w') as json_file:
        json.dump(data, json_file, indent=4)

def get_and_save_data(player_name=None, all_stats=False, season_loot=False, identities=False, maps=False, info=False, friendFeed=False, eventFeed=False, cod_points=False, connected_accounts=False, settings=False):
    # Create the stats directory if it doesn't exist
    DIR_NAME = 'stats'
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
    
    # Check if cookie file exists
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            api_key = f.read().strip()
    else:
        api_key = input("Please enter your ACT_SSO_COOKIE: ")
        with open(COOKIE_FILE, 'w') as f:
            f.write(api_key)

    # Check if userInfo.json exists, create it if it doesn't
    USER_INFO_FILE = os.path.join('userInfo.json')
    if not os.path.exists(USER_INFO_FILE):
        with open(USER_INFO_FILE, 'w') as f:
            pass  # Creates an empty file

    # If player_name is not provided via command line, get it from user input
    if not player_name:
        player_name = input("Please enter the player's username (with #1234567): ")

    # Login with sso token
    api.login(api_key)
    
    # Retrieve data from API
    # First, determine if any specific optional arguments were given
    if not (all_stats or season_loot or identities or maps or info or friendFeed or eventFeed or cod_points or connected_accounts or settings):
        # If no specific optional arguments are given, then default behavior:
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        save_to_file(player_stats, 'stats.json')
        save_to_file(match_info, 'match_info.json')
    elif all_stats:
        # If the all_stats argument is given:
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        season_loot_data = api.ModernWarfare.seasonLoot(platforms.Activision, player_name)
        identities_data = api.Me.loggedInIdentities()
        map_list = api.ModernWarfare.mapList(platforms.Activision)

        info = api.Me.info()
        friendFeed = api.Me.friendFeed()
        eventFeed = api.Me.eventFeed()
        cod_points = api.Me.codPoints()
        connectedAccounts = api.Me.connectedAccounts()
        settings = api.Me.settings()

        save_to_file(player_stats, 'stats.json')
        save_to_file(match_info, 'match_info.json')
        save_to_file(season_loot_data, 'season_loot.json')
        save_to_file(map_list, 'map_list.json')
        save_to_file(identities_data, 'identities.json')

        save_to_file(info, 'info.json')
        save_to_file(friendFeed, 'friendFeed.json')
        save_to_file(eventFeed, 'eventFeed.json')
        save_to_file(cod_points, 'cp.json')
        save_to_file(connectedAccounts, 'connectedAccounts.json')
        save_to_file(settings, 'settings.json')
    else:
        # For other specific optional arguments:
        if season_loot:
            season_loot_data = api.ModernWarfare.seasonLoot(platforms.Activision, player_name)
            save_to_file(season_loot_data, 'season_loot.json')
        if identities:
            identities_data = api.Me.loggedInIdentities()
            save_to_file(identities_data, 'identities.json')
        if maps:
            map_list = api.ModernWarfare.mapList(platforms.Activision)
            save_to_file(map_list, 'map_list.json')

        if info:
            info = api.Me.info()
            save_to_file(info, 'info.json')
        if friendFeed:
            friendFeed = api.Me.friendFeed()
            save_to_file(friendFeed, 'friendFeed.json')
        if eventFeed:
            eventFeed = api.Me.eventFeed()
            save_to_file(eventFeed, 'eventFeed.json')
        if cod_points:
            cod_points = api.Me.codPoints()
            save_to_file(cod_points, 'cp.json')
        if connected_accounts:
            connectedAccounts = api.Me.connectedAccounts()
            save_to_file(connectedAccounts, 'connectedAccounts.json')
        if settings:
            settings = api.Me.settings()
            save_to_file(settings, 'settings.json')

# Save results to a JSON file inside the stats directory
def recursive_key_replace(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = replacements.get(key, key)
            if isinstance(value, str):
                new_value = replacements.get(value, value)
                new_obj[new_key] = recursive_key_replace(new_value)
            else:
                new_obj[new_key] = recursive_key_replace(value)
        return new_obj
    elif isinstance(obj, list):
        return [recursive_key_replace(item) for item in obj]
    else:
        return replacements.get(obj, obj) if isinstance(obj, str) else obj

def sort_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "mode":
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['timePlayed'], reverse=True))
            elif key in ["Assault Rifles", "Shotguns", "Marksman Rifles", "Snipers", "LMGs", "Launchers", "Pistols", "SMGs", "Melee"]:
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['kills'], reverse=True))
            elif key in ["Field Upgrades"]:
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['uses'], reverse=True))
            elif key in ["Tactical Equipment", "Lethal Equipment"]:
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['uses'], reverse=True))
            elif key == "Scorestreaks":
                for subcategory, scorestreaks in value.items():
                    data[key][subcategory] = dict(sorted(scorestreaks.items(), key=lambda item: item[1]['properties']['awardedCount'], reverse=True))
            elif key == "Accolades":
                if 'properties' in value:
                    data[key]['properties'] = dict(sorted(value['properties'].items(), key=lambda item: item[1], reverse=True))
            else:
                # Recursive call to handle nested dictionaries
                data[key] = sort_data(value)
    return data

def replace_time_and_duration_recursive(data):
    """
    Recursively replace epoch times for specific keys in a nested dictionary or list.
    """

    time_keys = ["timePlayedTotal", "timePlayed", "objTime", "time", "timeProne", 
                 "timeSpentAsPassenger", "timeSpentAsDriver", "timeOnPoint", 
                 "timeWatchingKillcams", "timeCrouched", "timesSelectedAsSquadLeader", 
                 "longestTimeSpentOnWeapon", "avgLifeTime", "percentTimeMoving"]

    if isinstance(data, list):
        for item in data:
            replace_time_and_duration_recursive(item)

    elif isinstance(data, dict):
        for key, value in data.items():
            if key in time_keys:
                data[key] = convert_duration_seconds(value)
            
            elif key == "utcStartSeconds":
                data[key] = epoch_to_human_readable(value)
                # For EST conversion: 
                # data[key] = epoch_to_human_readable(value, "EST")
                
            elif key == "utcEndSeconds":
                data[key] = epoch_to_human_readable(value)
                # For EST conversion:
                # data[key] = epoch_to_human_readable(value, "EST")
                
            elif key == "duration":
                data[key] = convert_duration_milliseconds(value)
            
            else:
                replace_time_and_duration_recursive(value)

def epoch_to_human_readable(epoch_timestamp, timezone='GMT'):
    if isinstance(epoch_timestamp, str):
        return epoch_timestamp  # Already converted

    dt_object = datetime.datetime.utcfromtimestamp(epoch_timestamp)
    if timezone == 'GMT':
        date_str = dt_object.strftime("GMT: %A, %B %d, %Y %I:%M:%S %p")
    elif timezone == 'EST':
        dt_object -= datetime.timedelta(hours=4)  # Using 4 hours for EST conversion instead of 5?
        date_str = dt_object.strftime("EST: %A, %B %d, %Y %I:%M:%S %p")
    else:
        raise ValueError("Unsupported timezone.")
    return date_str

def convert_duration_milliseconds(milliseconds):
    if isinstance(milliseconds, str) and "Minutes" in milliseconds:
        return milliseconds  # Already converted
    
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes} Minutes {seconds} Seconds {milliseconds} Milliseconds"

def convert_duration_seconds(seconds):
    """
    Convert duration from seconds to a string format with days, minutes, seconds, and milliseconds.
    """
    if isinstance(seconds, str):
        return seconds  # Already converted

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Convert to integers to remove decimal places
    days = int(days)
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    return f"{days} Days {hours} Hours {minutes} Minutes {seconds} Seconds"

def beautify_data():
    file_path = (os.path.join(DIR_NAME, 'stats.json'))
    with open(file_path, 'r') as file:
        data = json.load(file)
    replace_time_and_duration_recursive(data)
    data = recursive_key_replace(data)
    data = sort_data(data)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Keys sorted and replaced in {file_path}.")

def beautify_match_data():
    file_path = (os.path.join(DIR_NAME, 'match_info.json'))
    with open(file_path, 'r') as file:
        data = json.load(file)
    replace_time_and_duration_recursive(data)
    data = recursive_key_replace(data)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Keys replaced in {file_path}.")

def split_matches_into_files():
    """
    Split the matches in match_info.json into separate files.
    """
    MATCHES_DIR = os.path.join(DIR_NAME, MATCH_DIR_NAME)
    
    # Create matches directory if it doesn't exist
    if not os.path.exists(MATCHES_DIR):
        os.makedirs(MATCHES_DIR)

    # Load the match_info data
    with open(os.path.join(DIR_NAME, 'match_info.json'), 'r') as file:
        data = json.load(file)
        matches = data.get('data', {}).get('matches', [])  # Correct the key to access matches

    # Check if data needs cleaning
    sample_match = matches[0] if matches else {}
    if (isinstance(sample_match.get("utcStartSeconds"), int) or 
        isinstance(sample_match.get("utcEndSeconds"), int) or 
        isinstance(sample_match.get("duration"), int)):
        
        print("Cleaning match data...")
        replace_time_and_duration_recursive(data)
        
        # Save the cleaned data back to match_info.json
        with open(os.path.join(DIR_NAME, 'match_info.json'), 'w') as file:
            json.dump(data, file, indent=4)

    # Split and save each match into a separate file
    for idx, match in enumerate(matches):
        # Create a copy of the match to ensure we don't modify the original data
        match_copy = dict(match)
        # Remove the 'loadouts' subkey from the 'player' key to avoid the cascading data
        match_copy['player'].pop('loadouts', None)
        match_copy['player'].pop('loadout', None)

        # Remove the entire player subkey to avoid the cascading data, if you want to exclude more, add them here
        # match_copy.pop('player', None)

        file_name = f"match_{idx + 1}.json"
        with open(os.path.join(MATCHES_DIR, file_name), 'w') as match_file:
            json.dump(match_copy, match_file, indent=4)

    print(f"Matches split into {len(matches)} separate files in {MATCHES_DIR}.")

def main():
    # Define the block of quote text to display in the help command
    help_text = """
    Obtaining your ACT_SSO_COOKIE

    - Go to https://www.callofduty.com and login with your account
    - Once logged in, press F12 for your browsers developer tools. Then go to Application --> Storage --> Cookies --> https://www.callofduty.com and find ACT_SSO_COOKIE
    - Enter the value when prompted
    """

    parser = argparse.ArgumentParser(description="Detailed Modern Warfare (2019) Statistics Tool", epilog=help_text, formatter_class=argparse.RawDescriptionHelpFormatter)

    # Group related arguments
    group_data = parser.add_argument_group("Data Fetching Options")
    group_cleaning = parser.add_argument_group("Data Cleaning Options")

    # Add arguments for Data Fetching Options
    group_data.add_argument("-p", "--player_name", type=str, help="Player's username (with #1234567)")
    group_data.add_argument("-a", "--all_stats", action="store_true", help="Fetch all the different types of stats data")
    group_data.add_argument("-sl", "--season_loot", action="store_true", help="Fetch only the season loot data")
    group_data.add_argument("-id", "--identities", action="store_true", help="Fetch only the logged-in identities data")
    group_data.add_argument("-m", "--maps", action="store_true", help="Fetch only the map list data")
    group_data.add_argument("-i", "--info", action="store_true", help="Fetch only general information")
    group_data.add_argument("-f", "--friendFeed", action="store_true", help="Fetch only your friend feed")
    group_data.add_argument("-e", "--eventFeed", action="store_true", help="Fetch only your event feed")
    group_data.add_argument("-cp", "--cod_points", action="store_true", help="Fetch only your COD Point balance")
    group_data.add_argument("-ca", "--connected_accounts", action="store_true", help="Fetch only the map list data")
    group_data.add_argument("-s", "--settings", action="store_true", help="Fetch only your account settings")

    # Add arguments for Cleaning Options
    group_cleaning.add_argument("-c", "--clean", action="store_true", help="Beautify all data")
    group_cleaning.add_argument("-sm", "--split_matches", action="store_true", help="Split the matches into separate JSON files within the 'matches' subfolder")
    group_cleaning.add_argument("-csd", "--clean_stats_data", action="store_true", help="Beautify the data and convert to human-readable strings in stats.json")
    group_cleaning.add_argument("-cmd", "--clean_match_data", action="store_true", help="Beautify the match data and convert to human-readable strings in match_info.json")

    args = parser.parse_args()

    # Custom error handling
    # try:
    #     args = parser.parse_args()
    # except SystemExit:
    #     # Check if 'player_name' is in sys.argv, if not, raise exception
    #     if '--player_name' not in sys.argv and '-p' not in sys.argv:
    #         print('You must specify a player name!')
    #     # Otherwise, re-raise the error or print the default error message.
    #     sys.exit(1)

    if args.split_matches:
        split_matches_into_files()
    elif args.clean_stats_data:
        beautify_data()
    elif args.clean_match_data:
        beautify_match_data()
    elif args.clean:
        beautify_data()
        beautify_match_data()
    else:
        get_and_save_data(args.player_name, args.all_stats, args.season_loot, args.identities, args.maps, args.info, args.friendFeed, args.eventFeed, args.cod_points, args.connected_accounts, args.settings)

if __name__ == "__main__":
    main()