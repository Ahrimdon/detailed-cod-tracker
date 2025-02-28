import re
import sys
import json
import os
import argparse
from cod_api import API, platforms
import asyncio
import datetime

# Configure asyncio for Windows
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Constants
COOKIE_FILE = 'cookie.txt'
STATS_DIR = 'stats'
MATCH_DIR = 'matches'
REPLACEMENTS_FILE = 'data/replacements.json'
TIMEZONE_OPTIONS = ["GMT", "EST", "CST", "PST"]

# Initialize API
api = API()

class CodStatsManager:
    """Main class to manage COD API interactions and data processing."""
    
    def __init__(self):
        self._ensure_directories_exist()
        self.replacements = self._load_replacements()
        self.api_key = self._get_api_key()
        api.login(self.api_key)
        
    def _ensure_directories_exist(self):
        """Ensure necessary directories exist."""
        if not os.path.exists(STATS_DIR):
            os.makedirs(STATS_DIR)
        match_dir_path = os.path.join(STATS_DIR, MATCH_DIR)
        if not os.path.exists(match_dir_path):
            os.makedirs(match_dir_path)
            
    def _load_replacements(self):
        """Load replacements from the JSON file."""
        # First, handle running as PyInstaller executable
        if getattr(sys, 'frozen', False):
            # If running as bundle (frozen)
            bundle_dir = sys._MEIPASS
            replacements_path = os.path.join(bundle_dir, 'data', 'replacements.json')
        else:
            # If running as a normal Python script
            replacements_path = REPLACEMENTS_FILE
        
        if not os.path.exists(replacements_path):
            raise FileNotFoundError(f"{replacements_path} not found. Ensure it exists in the script's directory.")
        
        with open(replacements_path, 'r') as file:
            return json.load(file)
            
    def _get_api_key(self):
        """Get API key from file or user input."""
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, 'r') as f:
                return f.read().strip()
        else:
            api_key = input("Please enter your ACT_SSO_COOKIE: ")
            with open(COOKIE_FILE, 'w') as f:
                f.write(api_key)
            return api_key
            
    def save_to_file(self, data, filename):
        """Save data to a JSON file."""
        file_path = os.path.join(STATS_DIR, filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to {file_path}")
            
    def get_player_name(self):
        """Get player name from user input."""
        return input("Please enter the player's username (with #1234567): ")
        
    def fetch_data(self, player_name=None, **options):
        """Fetch data based on specified options."""
        if not player_name:
            player_name = self.get_player_name()
            
        # If no specific option is selected, fetch basic stats
        if not any(options.values()):
            self._fetch_basic_stats(player_name)
            return
            
        # If all_stats option is selected, fetch everything
        if options.get('all_stats'):
            self._fetch_all_stats(player_name)
            return
            
        # Otherwise, fetch only requested data
        self._fetch_specific_data(player_name, options)
            
    def _fetch_basic_stats(self, player_name):
        """Fetch basic player stats and match history."""
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        self.save_to_file(player_stats, 'stats.json')
        self.save_to_file(match_info, 'match_info.json')
        
    def _fetch_all_stats(self, player_name):
        """Fetch all available stats for a player."""
        # Basic stats
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        season_loot_data = api.ModernWarfare.seasonLoot(platforms.Activision, player_name)
        
        # Player-specific data
        identities_data = api.Me.loggedInIdentities()
        map_list = api.ModernWarfare.mapList(platforms.Activision)
        
        # Save basic data
        self.save_to_file(player_stats, 'stats.json')
        self.save_to_file(match_info, 'match_info.json')
        self.save_to_file(season_loot_data, 'season_loot.json')
        self.save_to_file(map_list, 'map_list.json')
        self.save_to_file(identities_data, 'identities.json')
        
        # Check if userInfo.json exists to determine if we should fetch additional data
        user_info_file = os.path.join(STATS_DIR, 'userInfo.json')
        if os.path.exists(user_info_file):
            # Additional user data
            info = api.Me.info()
            friend_feed = api.Me.friendFeed()
            event_feed = api.Me.eventFeed()
            cod_points = api.Me.codPoints()
            connected_accounts = api.Me.connectedAccounts()
            
            try:
                settings = api.Me.settings()
                # Make sure settings is JSON serializable
                self.save_to_file(self._ensure_json_serializable(settings), 'settings.json')
            except TypeError as e:
                print(f"Warning: Could not save settings due to serialization error: {e}")
            
            # Save additional data
            self.save_to_file(info, 'info.json')
            self.save_to_file(friend_feed, 'friendFeed.json')
            self.save_to_file(event_feed, 'eventFeed.json')
            self.save_to_file(cod_points, 'cp.json')
            self.save_to_file(connected_accounts, 'connectedAccounts.json')
            
    def _fetch_specific_data(self, player_name, options):
        """Fetch specific data based on provided options."""
        endpoints = {
            'season_loot': (api.ModernWarfare.seasonLoot, [platforms.Activision, player_name], 'season_loot.json'),
            'identities': (api.Me.loggedInIdentities, [], 'identities.json'),
            'maps': (api.ModernWarfare.mapList, [platforms.Activision], 'map_list.json'),
            'info': (api.Me.info, [], 'info.json'),
            'friendFeed': (api.Me.friendFeed, [], 'friendFeed.json'),
            'eventFeed': (api.Me.eventFeed, [], 'eventFeed.json'),
            'cod_points': (api.Me.codPoints, [], 'cp.json'),
            'connected_accounts': (api.Me.connectedAccounts, [], 'connectedAccounts.json'),
            'settings': (api.Me.settings, [], 'settings.json')
        }
        
        for option, value in options.items():
            if value and option in endpoints:
                func, args, filename = endpoints[option]
                data = func(*args)
                self.save_to_file(data, filename)
                
    def beautify_all_data(self, timezone='GMT'):
        """Beautify all data files."""
        self.beautify_stats_data(timezone)
        self.beautify_match_data(timezone)
        self.beautify_feed_data(timezone)
        self.clean_json_files('friendFeed.json', 'eventFeed.json')
        print("All data beautified successfully.")
        
    def beautify_stats_data(self, timezone='GMT'):
        """Beautify stats data."""
        file_path = os.path.join(STATS_DIR, 'stats.json')
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. Skipping beautification.")
            return
            
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        # Convert times and durations
        self._replace_time_and_duration_recursive(data, timezone)
        
        # Replace keys with more readable names
        data = self._recursive_key_replace(data)
        
        # Sort data by relevant metrics
        data = self._sort_data(data)
        
        # Save modified data
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            
        print(f"Keys sorted and replaced in {file_path}.")
        
    def beautify_match_data(self, timezone='GMT'):
        """Beautify match data."""
        file_path = os.path.join(STATS_DIR, 'match_info.json')
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. Skipping beautification.")
            return
            
        with open(file_path, 'r') as file:
            data = json.load(file)
            
        # Convert times and durations
        self._replace_time_and_duration_recursive(data, timezone)
        
        # Replace keys with more readable names
        data = self._recursive_key_replace(data)
        
        # Save modified data
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            
        print(f"Keys replaced in {file_path}.")
        
    def beautify_feed_data(self, timezone='GMT'):
        """Beautify feed data files."""
        for feed_file in ['friendFeed.json', 'eventFeed.json']:
            file_path = os.path.join(STATS_DIR, feed_file)
            if not os.path.exists(file_path):
                print(f"{feed_file} does not exist, skipping.")
                continue
                
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            # Convert times and durations
            self._replace_time_and_duration_recursive(data, timezone)
            
            # Replace keys with more readable names
            data = self._recursive_key_replace(data)
            
            # Save modified data
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                
            print(f"Keys sorted and replaced in {feed_file}.")
            
    def split_matches_into_files(self, timezone='GMT'):
        """Split match data into separate files."""
        matches_dir = os.path.join(STATS_DIR, MATCH_DIR)
        if not os.path.exists(matches_dir):
            os.makedirs(matches_dir)
            
        match_info_path = os.path.join(STATS_DIR, 'match_info.json')
        if not os.path.exists(match_info_path):
            print(f"Match info file not found at {match_info_path}. Skipping split.")
            return
            
        with open(match_info_path, 'r') as file:
            data = json.load(file)
            matches = data.get('data', {}).get('matches', [])
            
        if not matches:
            print("No matches found to split.")
            return
            
        # Check if time conversion is needed
        sample_match = matches[0]
        needs_time_conversion = (
            isinstance(sample_match.get("utcStartSeconds"), int) or 
            isinstance(sample_match.get("utcEndSeconds"), int) or 
            isinstance(sample_match.get("duration"), int)
        )
        
        if needs_time_conversion:
            print("Converting match timestamps to human-readable format...")
            self._replace_time_and_duration_recursive(data, timezone)
            
            # Update the main match file
            with open(match_info_path, 'w') as file:
                json.dump(data, file, indent=4)
                
        # Process each match
        for idx, match in enumerate(matches):
            # Create a copy to avoid modifying the original data
            match_copy = dict(match)
            
            # Remove large loadout data to keep files smaller
            if 'player' in match_copy:
                match_copy['player'].pop('loadouts', None)
                match_copy['player'].pop('loadout', None)
                
            # Save to individual file
            file_name = f"match_{idx + 1}.json"
            file_path = os.path.join(matches_dir, file_name)
            with open(file_path, 'w') as match_file:
                json.dump(match_copy, match_file, indent=4)
                
        print(f"Matches split into {len(matches)} separate files in {matches_dir}.")
        
    def clean_json_files(self, *filenames):
        """Clean JSON files by removing HTML-like tags and entities."""
        regex_pattern = r'&lt;span class=&quot;|&lt;/span&gt;|&quot;&gt;|mp-stat-items|kills-value|headshots-value|username|game-mode|kdr-value|accuracy-value'
        replace = ''
        
        for filename in filenames:
            file_path = os.path.join(STATS_DIR, filename)
            if not os.path.exists(file_path):
                print(f"{filename} does not exist, skipping.")
                continue
                
            with open(file_path, 'r') as file:
                content = file.read()
                
            # Replace unwanted patterns
            modified_content = re.sub(regex_pattern, replace, content)
            
            # Save cleaned content
            with open(file_path, 'w') as file:
                file.write(modified_content)
                
            print(f"Removed unreadable strings from {filename}.")
            
    def _recursive_key_replace(self, obj):
        """Recursively replace keys and values with more readable versions."""
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = self.replacements.get(key, key)
                if isinstance(value, str):
                    new_value = self.replacements.get(value, value)
                    new_obj[new_key] = self._recursive_key_replace(new_value)
                else:
                    new_obj[new_key] = self._recursive_key_replace(value)
            return new_obj
        elif isinstance(obj, list):
            return [self._recursive_key_replace(item) for item in obj]
        else:
            return self.replacements.get(obj, obj) if isinstance(obj, str) else obj
            
    def _sort_data(self, data):
        """Sort data by meaningful metrics for better readability."""
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "mode":
                    # Sort game modes by time played
                    data[key] = dict(sorted(
                        value.items(), 
                        key=lambda item: item[1]['properties']['timePlayed'], 
                        reverse=True
                    ))
                elif key in ["Assault Rifles", "Shotguns", "Marksman Rifles", "Snipers", "LMGs", "Launchers", "Pistols", "SMGs", "Melee"]:
                    # Sort weapons by kills
                    data[key] = dict(sorted(
                        value.items(), 
                        key=lambda item: item[1]['properties']['kills'], 
                        reverse=True
                    ))
                elif key in ["Field Upgrades", "Tactical Equipment", "Lethal Equipment"]:
                    # Sort equipment by uses
                    data[key] = dict(sorted(
                        value.items(), 
                        key=lambda item: item[1]['properties']['uses'], 
                        reverse=True
                    ))
                elif key == "Scorestreaks":
                    # Sort scorestreaks by awarded count
                    for subcategory, scorestreaks in value.items():
                        data[key][subcategory] = dict(sorted(
                            scorestreaks.items(), 
                            key=lambda item: item[1]['properties']['awardedCount'], 
                            reverse=True
                        ))
                elif key == "Accolades":
                    # Sort accolades by count
                    if 'properties' in value:
                        data[key]['properties'] = dict(sorted(
                            value['properties'].items(), 
                            key=lambda item: item[1], 
                            reverse=True
                        ))
                else:
                    # Recursively sort nested data
                    data[key] = self._sort_data(value)
        return data
        
    def _replace_time_and_duration_recursive(self, data, timezone):
        """Recursively replace epoch times with human-readable formats."""
        time_keys = [
            "timePlayedTotal", "timePlayed", "objTime", "time", "timeProne", 
            "timeSpentAsPassenger", "timeSpentAsDriver", "timeOnPoint", 
            "timeWatchingKillcams", "timeCrouched", "timesSelectedAsSquadLeader", 
            "longestTimeSpentOnWeapon", "avgLifeTime", "percentTimeMoving"
        ]
        date_keys = ["date", "updated", "originalDate"]
        
        if isinstance(data, list):
            for item in data:
                self._replace_time_and_duration_recursive(item, timezone)
        elif isinstance(data, dict):
            for key, value in data.items():
                if key in date_keys:
                    data[key] = self._epoch_milli_to_human_readable(value, timezone)
                elif key in time_keys:
                    data[key] = self._convert_duration_seconds(value)
                elif key == "utcStartSeconds":
                    data[key] = self._epoch_to_human_readable(value, timezone)
                elif key == "utcEndSeconds":
                    data[key] = self._epoch_to_human_readable(value, timezone)
                elif key == "duration":
                    data[key] = self._convert_duration_milliseconds(value)
                else:
                    self._replace_time_and_duration_recursive(value, timezone)
                    
    def _epoch_milli_to_human_readable(self, epoch_millis, timezone='GMT'):
        """Convert epoch milliseconds to human-readable date string."""
        if isinstance(epoch_millis, str):
            return epoch_millis
            
        dt_object = datetime.datetime.utcfromtimestamp(epoch_millis / 1000.0)
        return self._format_datetime(dt_object, timezone)
        
    def _epoch_to_human_readable(self, epoch_timestamp, timezone='GMT'):
        """Convert epoch seconds to human-readable date string."""
        if isinstance(epoch_timestamp, str):
            return epoch_timestamp
            
        dt_object = datetime.datetime.utcfromtimestamp(epoch_timestamp)
        return self._format_datetime(dt_object, timezone)
        
    def _format_datetime(self, dt_object, timezone):
        """Format datetime object based on timezone."""
        timezone_offsets = {
            'GMT': 0,
            'EST': -4,
            'CST': -5,
            'PST': -8
        }
        
        if timezone not in timezone_offsets:
            raise ValueError(f"Unsupported timezone: {timezone}")
            
        # Apply timezone offset
        dt_object -= datetime.timedelta(hours=timezone_offsets[timezone])
        
        # Format date string
        return f"{timezone}: {dt_object.strftime('%A, %B %d, %Y %I:%M:%S %p')}"
        
    def _convert_duration_milliseconds(self, milliseconds):
        """Convert milliseconds to a human-readable duration string."""
        if isinstance(milliseconds, str) and "Minutes" in milliseconds:
            return milliseconds  # Already converted
            
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes} Minutes {seconds} Seconds {milliseconds} Milliseconds"
        
    def _convert_duration_seconds(self, seconds):
        """Convert seconds to a human-readable duration string."""
        if isinstance(seconds, str):
            return seconds  # Already converted
            
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        
        return f"{days} Days {hours} Hours {minutes} Minutes {seconds} Seconds"

def _ensure_json_serializable(self, obj):
    """Recursively convert objects to JSON serializable types."""
    if isinstance(obj, dict):
        return {key: self._ensure_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [self._ensure_json_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return [self._ensure_json_serializable(item) for item in obj]
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    else:
        # Convert any other type to string representation
        return str(obj)

class CLI:
    """Command Line Interface manager."""
    
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager
        self.help_text = """
        Obtaining your ACT_SSO_COOKIE

        - Go to https://www.callofduty.com and login with your account
        - Once logged in, press F12 for your browsers developer tools. Then go to Application --> Storage --> Cookies --> https://www.callofduty.com and find ACT_SSO_COOKIE
        - Enter the value when prompted
        """
        
    def display_menu(self):
        """Display the main menu and get user choice."""
        print("\nBeautify Options:")
        print("1) Beautify all data")
        print("2) Split matches into separate files")

        print("\nOptions Requiring Player Name:")
        print("3) Get all stats")
        print("4) Get identities")
        print("5) Get general information")
        print("6) Get friend feed")
        print("7) Get event feed")
        print("8) Get COD Point balance")
        print("9) Get connected accounts")
        print("10) Get account settings")

        print("\nOptions Not Requiring Player Name:")
        print("11) Get season loot")
        print("12) Get map list")

        print("\n0) Exit")

        try:
            choice = int(input("Enter your choice: "))
            return choice
        except ValueError:
            print("Please enter a valid number.")
            return -1
            
    def handle_menu_choice(self, choice):
        """Handle the user's menu choice."""
        if choice == 0:
            print("Exiting...")
            return False
            
        if choice in [3, 4, 5, 6, 7, 8, 9, 10, 11]:
            player_name = input("Please enter the player's username (with #1234567): ")
            
            options = {
                3: {'all_stats': True},
                4: {'season_loot': True},
                5: {'identities': True},
                6: {'info': True},
                7: {'friendFeed': True},
                8: {'eventFeed': True},
                9: {'cod_points': True},
                10: {'connected_accounts': True},
                11: {'settings': True}
            }
            
            if choice in options:
                self.stats_manager.fetch_data(player_name=player_name, **options[choice])
                
        elif choice == 1:
            self.stats_manager.beautify_all_data()
        elif choice == 2:
            self.stats_manager.split_matches_into_files()
        elif choice == 12:
            self.stats_manager.fetch_data(season_loot=True)
        elif choice == 13:
            self.stats_manager.fetch_data(maps=True)
        else:
            print("Invalid choice. Please try again.")
            return True
            
        return True
        
    def run_interactive_mode(self):
        """Run the interactive menu mode."""
        running = True
        while running:
            choice = self.display_menu()
            running = self.handle_menu_choice(choice)
            
    def setup_argument_parser(self):
        """Set up command line argument parser."""
        parser = argparse.ArgumentParser(
            description="Detailed Modern Warfare (2019) Statistics Tool", 
            epilog=self.help_text, 
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Group arguments for better help display
        group_default = parser.add_argument_group("Default Options")
        group_data = parser.add_argument_group("Data Fetching Options")
        group_cleaning = parser.add_argument_group("Data Cleaning Options")
        
        # Default options
        group_default.add_argument(
            "-tz", "--timezone", 
            type=str, 
            default="GMT", 
            choices=TIMEZONE_OPTIONS, 
            help="Specify the timezone (GMT, EST, CST, PST)"
        )
        
        # Data fetching options
        group_data.add_argument("-p", "--player_name", type=str, help="Player's username (with #1234567)")
        group_data.add_argument("-a", "--all_stats", action="store_true", help="Fetch all the different types of stats data")
        group_data.add_argument("-sl", "--season_loot", action="store_true", help="Fetch only the season loot data")
        group_data.add_argument("-id", "--identities", action="store_true", help="Fetch only the logged-in identities data")
        group_data.add_argument("-m", "--maps", action="store_true", help="Fetch only the map list data")
        group_data.add_argument("-i", "--info", action="store_true", help="Fetch only general information")
        group_data.add_argument("-f", "--friendFeed", action="store_true", help="Fetch only your friend feed")
        group_data.add_argument("-e", "--eventFeed", action="store_true", help="Fetch only your event feed")
        group_data.add_argument("-cp", "--cod_points", action="store_true", help="Fetch only your COD Point balance")
        group_data.add_argument("-ca", "--connected_accounts", action="store_true", help="Fetch only connected accounts data")
        group_data.add_argument("-s", "--settings", action="store_true", help="Fetch only your account settings")
        
        # Data cleaning options
        group_cleaning.add_argument("-c", "--clean", action="store_true", help="Beautify all data")
        group_cleaning.add_argument("-sm", "--split_matches", action="store_true", help="Split matches into separate JSON files")
        group_cleaning.add_argument("-csd", "--clean_stats_data", action="store_true", help="Beautify stats.json data")
        group_cleaning.add_argument("-cmd", "--clean_match_data", action="store_true", help="Beautify match_info.json data")
        group_cleaning.add_argument("-cff", "--clean_friend_feed", action="store_true", help="Clean friend feed data")
        group_cleaning.add_argument("-cef", "--clean_event_feed", action="store_true", help="Clean event feed data")
        
        return parser
        
    def run_cli_mode(self, args):
        """Run the command line mode with parsed arguments."""
        # Prioritize cleaning operations
        if args.clean:
            self.stats_manager.beautify_all_data(timezone=args.timezone)
        elif args.clean_stats_data:
            self.stats_manager.beautify_stats_data(timezone=args.timezone)
        elif args.clean_match_data:
            self.stats_manager.beautify_match_data(timezone=args.timezone)
        elif args.split_matches:
            self.stats_manager.split_matches_into_files(timezone=args.timezone)
        elif args.clean_friend_feed:
            self.stats_manager.clean_json_files('friendFeed.json')
        elif args.clean_event_feed:
            self.stats_manager.clean_json_files('eventFeed.json')
        else:
            # Data fetching operations
            options = {
                'all_stats': args.all_stats,
                'season_loot': args.season_loot,
                'identities': args.identities,
                'maps': args.maps,
                'info': args.info,
                'friendFeed': args.friendFeed,
                'eventFeed': args.eventFeed,
                'cod_points': args.cod_points,
                'connected_accounts': args.connected_accounts,
                'settings': args.settings
            }
            self.stats_manager.fetch_data(args.player_name, **options)

def main():
    """Main entry point for the application."""
    stats_manager = CodStatsManager()
    cli = CLI(stats_manager)
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        parser = cli.setup_argument_parser()
        args = parser.parse_args()
        cli.run_cli_mode(args)
    else:
        # Run interactive mode
        cli.run_interactive_mode()

if __name__ == "__main__":
    main()