import json
import os
from cod_api import API, platforms

# initiating the API class
api = API()

COOKIE_FILE = 'cookie.txt'

# Check if cookie file exists
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE, 'r') as f:
        api_key = f.read().strip()
else:
    api_key = input("Please enter your ACT_SSO_COOKIE: ")
    with open(COOKIE_FILE, 'w') as f:
        f.write(api_key)

# Get player name from user
player_name = input("Please enter the player's username (with #1234567): ")

# login with sso token
api.login(api_key)

player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
season_loot = api.ModernWarfare.seasonLoot(platforms.Activision, player_name)
map_list = api.ModernWarfare.mapList(platforms.Activision)
identities = api.Me.loggedInIdentities()

# Save results to a JSON file
with open('stats.json', 'w') as json_file:
    json.dump(player_stats, json_file, indent=4)

with open('match_info.json', 'w') as json_file:
    json.dump(match_info, json_file, indent=4)

with open('season_loot.json', 'w') as json_file:
    json.dump(season_loot, json_file, indent=4)

with open('map_list.json', 'w') as json_file:
    json.dump(map_list, json_file, indent=4)

with open('identities.json', 'w') as json_file:
    json.dump(identities, json_file, indent=4)