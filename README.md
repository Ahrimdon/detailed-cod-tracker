# Modern Warfare 2019 Detailed Statistic Tracker

Tired of visiting [cod.tracker.gg](https://cod.tracker.gg/modern-warfare) to check your player stats? With this repository, you'll never have to visit that site again.

Get every single statistic Call of Duty <u>***tracks***</u> in one place, under a minute!

> To see an example, look in `/examples/`

## Table of Contents
  - [**Features**](#features)
  - [**Prerequisites**](#prerequisites)
  - [**Installation**](#installation)
  - [**Obtaining your ACT\_SSO\_COOKIE**](#obtaining-your-act_sso_cookie)
  - [**Command Line Arguments**](#command-line-arguments)
  - [**Sorting**](#sorting)

## Features
- Instantly download detailed statistics for any player, including ***Lifetime Statistics***, ***Match Statistics*** and ***season_loot***
- Download a list of all maps and game modes in current rotation
- Convert match start times, end times, and duration to human readable formats
- [**Sort**](#sorting) your statistics even better than the in-game Barracks does!
- Split detailed match data into separate files from most recent to least recent for easy viewing
- Convert all code names for weapons, killstreaks, equipment, etc. to human-readable strings

## Prerequisites
- Call of Duty Account
- Account API security settings set to open
- `Python 3.x` *(optional)*
- A Web Browser *(Tested with Chromium)*
- ~~[Curl](https://curl.se/download.html) ***(Installed by default on Windows)***~~

## Installation
#### Using the Latest Release **(EASIEST)**
- Navigate to the latest release and download `get_cod_stats.exe`
- Open a command line of your choise, navigate to the directory using `cd` and follow examples below
```
cd "C:\Users\John\Desktop\detailed-cod-tracker"

get_cod_stats.exe [-h] -p PLAYER_NAME [-a] [-sl] [-i] [-m] [-c] [-sm] [-csd] [-cmd]
```

#### Cloning the Repository
- Download the ZIP archive or clone the repository `git clone https://github.com/Ahrimdon/detailed-cod-tracker.git && cd detailed-cod-tracker`
- Run the setup using the command `python setup.py`.

## Obtaining your ACT_SSO_COOKIE
- Go to https://www.callofduty.com and login with your account
- Once logged in, press `F12` for your browsers developer tools. Then go to Application --> Storage --> 
  
  Cookies --> https://www.callofduty.com/ --> ACT_SSO_COOKIE
- Enter the value when prompted

## Obtaining your userInfo.json (Develop Branch ONLY)
- For some reason, Activision broke the userInfo API URL which in turn, broke the API Wrapper's logic to obtain certain user information. Unfortunately, this also means we also cannot use Curl. Follow the steps below if you wish to obtain General Info, friendFeed, eventFeed, Cod Point Balance, Connected Accounts, and Account Settings.
- This feature is only available on the `develop` branch.

1. Clone the repository, `git clone https://github.com/Ahrimdon/detailed-cod-tracker.git && cd detailed-cod-tracker`
2. Run the setup using `python setup.py`
3. Switch to the `develop` branch using `git checkout develop`
4. Obtain your [*ACT_SSO_COOKIE*](#obtaining-your-act_sso_cookie)
5. Go to `https://profile.callofduty.com/cod/userInfo/{ACT_SSO_COOKIE}` and copy the contents into `userInfo.json` in the repo's directory
    > *Note:* Create the `userInfo.json` file manually
6. In the newly created `userInfo.json`, delete "*userInfo(*" and "*);*" at the beginning and end of the file. Alternatively, you can find and replace using the regular expression inside `clean_userInfo_regex.txt`
7. Run `get_cod_stats.py` using the `-a` argument (e.g. `python get_cod_stats.py -p Ahrimdon -a`)

If done correctly, this should return the extra API information.

## Command Line Arguments
```
usage: get_cod_stats.py [-h] [-p PLAYER_NAME] [-a] [-sl] [-id] [-m] [-i] [-f] [-e] [-cp] [-ca] [-s] [-c] [-sm] [-csd] [-cmd] [-cff] [-cef]

Detailed Modern Warfare (2019) Statistics Tool

optional arguments:
  -h, --help            show this help message and exit

Data Fetching Options:
  -p PLAYER_NAME, --player_name PLAYER_NAME
                        Player's username (with #1234567)
  -a, --all_stats       Fetch all the different types of stats data
  -sl, --season_loot    Fetch only the season loot data
  -id, --identities     Fetch only the logged-in identities data
  -m, --maps            Fetch only the map list data
  -i, --info            Fetch only general information
  -f, --friendFeed      Fetch only your friend feed
  -e, --eventFeed       Fetch only your event feed
  -cp, --cod_points     Fetch only your COD Point balance
  -ca, --connected_accounts
                        Fetch only the map list data
  -s, --settings        Fetch only your account settings

Data Cleaning Options:
  -c, --clean           Beautify all data
  -sm, --split_matches  Split the matches into separate JSON files within the 'matches' subfolder
  -csd, --clean_stats_data
                        Beautify the data and convert to human-readable strings in stats.json
  -cmd, --clean_match_data
                        Beautify the match data and convert to human-readable strings in match_info.json
  -cff, --clean_friend_feed
                        Clean the friend feed data
  -cef, --clean_event_feed
                        Clean the event feed data
```

## Command Examples
**Gather Player's Lifetime Statistics & 20 Recent Games**
```
get_cod_stats.exe -p Ahrimdon#1234567
```

**Sort, clean, and organize all data**

```
get_cod_stats.exe -c
```

**Split matches into separate files**
```
get_cod_stats.exe -sm
```

**Gather all data**
```
get_cod_stats.exe -p Ahrimdon#1234567 -a
```

> All data is saved to `/stats/`

## Sorting
* Game Modes are sorted by *Time Played* in descending order
* Weapons are sorted by *Kills* in descending order
* Field Upgrades are sorted by *Uses* in descending order
* Lethal and Tactical equipment are sorted by *Uses* in descending order
* Lethal and Support Scorestreaks by *Times Awarded* in descending order
* Accolades sorted in descending order