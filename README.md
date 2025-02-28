# Modern Warfare 2019 Advanced Statistics Tracker

Access comprehensive Call of Duty statistics directly from your command line. No more visiting third-party tracking websites when you can retrieve **every statistic** Call of Duty records in under a minute.

> View example outputs in the `/examples/` directory

## Features

- **Complete Statistics Access**: Download detailed player statistics including lifetime stats, match history, and seasonal rewards
- **Enhanced Sorting**: Sort statistics more effectively than the in-game Barracks
- **Human-Readable Formats**: Convert timestamps and code names to user-friendly formats
- **Detailed Match History**: Split match data into separate files for easier analysis
- **Game Information**: Access lists of all maps and game modes in current rotation

## Prerequisites

- Call of Duty account with API security settings set to "Open"
- Web browser (Chromium-based recommended)
- Python 3.x (optional, tested with Python 3.9.13)

## Installation Options

### Option 1: Download the Latest Release (Recommended)

1. Download `cod_api_tool.exe` from the [latest release](https://github.com/Ahrimdon/detailed-cod-tracker/releases/latest)
2. Open a command prompt in the download directory
3. Execute the tool using the syntax below:

```
cod_api_tool.exe [arguments]
```

### Option 2: Clone the Repository

1. Clone the repository:
```
git clone https://github.com/Ahrimdon/detailed-cod-tracker.git
cd detailed-cod-tracker
```

2. Run the setup script:
```
python setup.py
```

## Authentication Setup

### Obtaining your ACT_SSO_COOKIE

1. Log in to [Call of Duty](https://www.callofduty.com)
2. Open developer tools (F12)
3. Navigate to: Application → Storage → Cookies → https://www.callofduty.com/
4. Copy the value of `ACT_SSO_COOKIE`
5. Provide this value when prompted by the tool

### Setting up userInfo.json (Required for Advanced Features)

Due to recent API changes, additional steps are required for certain features:

1. Navigate to `https://profile.callofduty.com/cod/userInfo/{ACT_SSO_COOKIE}` (replace with your actual cookie)
2. Copy the entire content
3. Create a file named `userInfo.json` in the tool's directory
4. Paste the content and remove `userInfo(` from the beginning and `);` from the end
   - Alternatively, use the regex pattern in `sanitize_userInfo_regex.txt`
5. Run the tool with the `-a` flag to access advanced features

## Command Line Reference

```
usage: cod_api_tool.py [-h] [-tz {GMT,EST,CST,PST}] [-p PLAYER_NAME] [-a]
                       [-sl] [-id] [-m] [-i] [-f] [-e] [-cp] [-ca] [-s] [-c]
                       [-sm] [-csd] [-cmd] [-cff] [-cef]
```

### Default Options
| Argument | Description |
|----------|-------------|
| `-h`, `--help` | Show help message and exit |
| `-tz`, `--timezone` | Specify timezone (GMT, EST, CST, PST) |

### Data Fetching Options
| Argument | Description |
|----------|-------------|
| `-p PLAYER_NAME`, `--player_name PLAYER_NAME` | Target player's username (with #1234567) |
| `-a`, `--all_stats` | Fetch all available statistics |
| `-sl`, `--season_loot` | Fetch only seasonal reward data |
| `-id`, `--identities` | Fetch only logged-in identities data |
| `-m`, `--maps` | Fetch only map list data |
| `-i`, `--info` | Fetch only general information |
| `-f`, `--friendFeed` | Fetch only friend feed |
| `-e`, `--eventFeed` | Fetch only event feed |
| `-cp`, `--cod_points` | Fetch only COD Point balance |
| `-ca`, `--connected_accounts` | Fetch only connected accounts data |
| `-s`, `--settings` | Fetch only account settings |

### Data Processing Options
| Argument | Description |
|----------|-------------|
| `-c`, `--clean` | Beautify all data |
| `-sm`, `--split_matches` | Split matches into separate JSON files |
| `-csd`, `--clean_stats_data` | Beautify stats.json data |
| `-cmd`, `--clean_match_data` | Beautify match_info.json data |
| `-cff`, `--clean_friend_feed` | Clean friend feed data |
| `-cef`, `--clean_event_feed` | Clean event feed data |

## Examples

**Basic Usage: Retrieve Player Statistics**
```
cod_api_tool.exe -p YourUsername#1234567
```

**Full Data Collection with Cleaning**
```
cod_api_tool.exe -p YourUsername#1234567 -a -c -sm
```

**Process Existing Data**
```
cod_api_tool.exe -c -sm
```

> All data is saved to the `/stats/` directory

## Advanced Sorting

The tool offers enhanced sorting capabilities:

- Game modes sorted by **Time Played** (descending)
- Weapons sorted by **Kills** (descending)
- Field upgrades sorted by **Uses** (descending)
- Equipment (lethal and tactical) sorted by **Uses** (descending)
- Scorestreaks sorted by **Times Awarded** (descending)
- Accolades sorted in descending order