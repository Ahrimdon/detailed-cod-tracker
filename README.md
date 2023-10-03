# Modern Warfare 2019 Detailed Statistic Tracker

Tired of visiting [cod.tracker.gg](https://cod.tracker.gg/modern-warfare) to check your stats? With this repository, you'll never have to visit that site again.

Get every single statistic Call of Duty tracks in ONE PLACE, in under a minute!

This repository is still a work in progress.

Prerequisites
-------------
- `Python 3.x` *(optional)*
- Call of Duty Account
- Battle.NET Account (PC Only for now)
- Account API security settings set to open

Gathering Detailed Stats
-------------
- Go to [Call of Duty's Website](https://www.callofduty.com/) and login with your account
- Once logged in, press `F12` for your browsers developer tools. Then go to `Application --> Storage --> Cookies --> https://www.callofduty.com` and find `ACT_SSO_COOKIE`
- Copy the Value into the into the `COOKIE_VALUE` variable in either `get_stats.bat` or `get_stats.ps1` (This will authenticate you)
- Replace the `PROF` variable with your profile's Activision ID in the following format - `PlayerName%0000000`
  * *The `%` replaces the `#` in the usual Activision ID*
- Once stats are downloaded, run `beautify_json.py` to beautify the JSON output and then `beautify_data.py` to sort and replace the JSON keys into a human readable string
  > If you don't have Python installed, you can run the executable versions of the scripts `beautify_json.exe` and `beautify_data.exe`

Sorting
-------------
* Game Modes are sorted by *Time Played* in descending order
* Weapons are sorted by *Kills* in descending order
* Field Upgrades are sorted by *Uses* in descending order
* Lethal and Tactical equipment are sorted by *Uses* in descending order
* Lethal and Support Scorestreaks by *Times Awarded* in descending order
* Accolades sorted in descending order

> To see an example, look at `example.json`