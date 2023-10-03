import json

def replace_keys_in_json(file_path, replacements):
    """Replace keys in the JSON file based on the replacements dictionary."""

    with open(file_path, 'r') as file:
        data = json.load(file)

    def recursive_key_replace(obj, replacements):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                new_key = replacements.get(key, key)
                new_obj[new_key] = recursive_key_replace(value, replacements)
            return new_obj
        elif isinstance(obj, list):
            for index, value in enumerate(obj):
                obj[index] = recursive_key_replace(value, replacements)
        return obj

    data = recursive_key_replace(data, replacements)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Define the keys to be replaced and their replacements
    replacements = {
        # Gamemodes
        "dom": "Domination",
        "hc_dom": "Hardcore Domination",
        "war": "Team Deathmatch",
        "hc_war": "Hardcore Team Deathmatch",
        "hq": "Headquarters",
        "hc_hq": "Hardcore Headquarters",
        "conf": "Kill Confirmed",
        "hc_conf": "Hardcore Kill Confirmed",
        "koth": "Hardpoint",
        "koth_hc": "Hardcore Hardpoint",
        "sd": "Search and Destroy",
        "hc_sd": "Hardcore Search and Destroy",
        "cyber": "Cyber Attack",
        "hc_cyber": "Hardcore Cyber Attack",
        "grnd": "Grind",
        "arm": "Ground War",
        "infect": "Infected",
        "gun": "Gun Game",
        "arena": "Gunfight",
        "br": "Battle Royale (Warzone)",
        "br_dmz": "Plunder",
        "br_all": "Battle Royale (Warzone & Plunder)",
        # Weapons
        "weapon_assault_rifle": "Assault Rifles",
        "weapon_shotgun": "Shotguns",
        "weapon_marksman": "Marksman Rifles",
        "weapon_sniper": "Snipers",
        "tacticals": "Tactical Equipment",
        "lethals": "Lethal Equipment",
        "weapon_lmg": "LMGs",
        "weapon_launcher": "Launchers",
        "supers": "Field Upgrades",
        "weapon_pistol": "Pistols",
        "weapon_other": "Primary Melee",
        "weapon_smg": "SMGs",
        "weapon_melee": "Melee",
        "scorestreakData": "Scorestreaks",
        "lethalScorestreakData": "Lethal Scorestreaks",
        "supportScorestreakData": "Support Scorestreaks",
        # Guns
        ## Assault Rifles
        "iw8_ar_tango21": "RAM-7",
        "iw8_ar_mike4": "M4A1",
        "iw8_ar_valpha": "AS VAL",
        "iw8_ar_falpha": "FR 5.56",
        "iw8_ar_mcharlie": "M13",
        "iw8_ar_akilo47": "AK-47",
        "iw8_ar_asierra12": "Oden",
        "iw8_ar_galima": "CR-56 AMAX",
        "iw8_ar_sierra552": "Grau 5.56",
        "iw8_ar_falima": "FAL",
        "iw8_ar_anovember94": "AN-94",
        "iw8_ar_kilo433": "Kilo 141",
        "iw8_ar_scharlie": "FN Scar 17",
        "iw8_sh_mike26": "VLK Rogue",
        ## Shotguns
        "iw8_sh_charlie725": "725",
        "iw8_sh_oscar12": "Origin 12 Shotgun",
        "iw8_sh_aalpha12": "JAK-12",
        "iw8_sh_romeo870": "Model 680",
        "iw8_sh_dpapa12": "R9-0 Shotgun",
        ## Marksman Rifles
        "iw8_sn_sbeta": "MK2 Carbine",
        "iw8_sn_crossbow": "Crossbow",
        "iw8_sn_romeo700": "SP-R 208",
        "iw8_sn_kilo98": "Kar98k",
        "iw8_sn_mike14": "EBR-14",
        "iw8_sn_sksierra": "SKS",
        ## Sniper Rifles
        "iw8_sn_alpha50": "AX-50",
        "iw8_sn_hdromeo": "HDR",
        "iw8_sn_delta": "Dragunov",
        "iw8_sn_xmike109": "Rytec AMR",
        ## Tactical Equipment
        "equip_gas_grenade": "Gas Grenade",
        "equip_snapshot_grenade": "Snapshot Grenade",
        "equip_decoy": "Decoy Grenade",
        "equip_smoke": "Smoke Grenade",
        "equip_concussion": "Concussion Grenade",
        "equip_hb_sensor": "Heartbeat Sensor",
        "equip_flash": "Flash Grenade",
        "equip_adrenaline": "Stim",
        ## Lethal Equipment
        "equip_frag": "Frag Grenade",
        "equip_thermite": "Thermite",
        "equip_semtex": "Semtex",
        "equip_claymore": "Claymore",
        "equip_c4": "C4",
        "equip_at_mine": "Proximity Mine",
        "equip_throwing_knife": "Throwing Knife",
        "equip_molotov": "Mototov Cocktail",
        ## LMGs
        "iw8_lm_kilo121": "M91",
        "iw8_lm_mkilo3": "Bruen Mk9",
        "iw8_lm_mgolf34": "MG34",
        "iw8_lm_lima86": "SA87",
        "iw8_lm_pkilo": "PKM",
        "iw8_lm_sierrax": "FiNN LMG",
        "iw8_lm_mgolf36": "Holger-26",
        # "": "", ### RAAL LMG not implemented
        ## Launchers
        "iw8_la_gromeo": "PILA",
        "iw8_la_rpapa7": "RPG-7",
        "iw8_la_juliet": "JOKR",
        "iw8_la_kgolf": "Strela-P",
        # "": "", ### Unknown Launcher
        ## Field Upgrades
        "super_emp_drone": "EMP Drone",
        "super_trophy": "Trophy System",
        "super_ammo_drop": "Munitions Box",
        "super_weapon_drop": "Weapon Drop",
        "super_fulton": "Cash Deposit Balloon",
        "super_armor_drop": "Armor Box",
        "super_select": "Field Upgrade Pro (Any)",
        "super_tac_insert": "Tactical Insertion",
        "super_recon_drone": "Recon Drone",
        "super_deadsilence": "Dead Silence",
        "super_supply_drop": "Loadout Drop", ### Unsure if this is Loadout Drop
        "super_tac_cover": "Deployable Cover",
        "super_support_box": "Stopping Power Rounds",
        ## Pistols
        "iw8_pi_cpapa": ".357",
        "iw8_pi_mike9": "Renetti",
        "iw8_pi_mike1911": "1911",
        "iw8_pi_golf21": "X16",
        "iw8_pi_decho": ".50 GS",
        "iw8_pi_papa320": "M19",
        # "": "", ### Sykov not implemented
        ## Primary Melee
        "iw8_me_riotshield": "Riot Shield",
        ## SMGs
        "iw8_sm_mpapa7": "MP7",
        "iw8_sm_augolf": "AUG",
        "iw8_sm_papa90": "P90",
        "iw8_sm_charlie9": "ISO",
        "iw8_sm_mpapa5": "MP5",
        "iw8_sm_smgolf45": "Striker 45",
        "iw8_sm_beta": "PP19 Bizon",
        "iw8_sm_victor": "Fennec",
        "iw8_sm_uzulu": "Uzi",
        # "": "", ### CX9 not implemented
        ## Melee
        "iw8_me_akimboblunt": "Kali Sticks",
        "iw8_me_akimboblades": "Dual Kodachis",
        "iw8_knife": "Knife",
        # Scorestreaks
        "precision_airstrike": "Precision Airstrike",
        "cruise_predator": "Cruise Missile",
        "manual_turret": "Shield Turret",
        "white_phosphorus": "White Phosphorus",
        "hover_jet": "VTOL Jet",
        "chopper_gunner": "Chopper Gunner",
        "gunship": "Gunship",
        "sentry_gun": "Sentry Gun",
        "toma_strike": "Cluster Strike",
        "nuke": "Nuke",
        "juggernaut": "Juggernaut",
        "pac_sentry": "Wheelson",
        "chopper_support": "Support Helo",
        "bradley": "Infantry Assault Vehicle",
        "airdrop": "Care Package",
        "radar_drone_overwatch": "Personal Radar",
        "scrambler_drone_guard": "Counter UAV",
        "uav": "UAV",
        "airdrop_multiple": "Emergency Airdrop",
        "directional_uav": "Advanced UAV",
        # Accolades
        "accoladeData": "Accolades",
        "classChanges": "Most Classes Changed (Evolver)",
        "highestAvgAltitude": "Highest Average Altitude (High Command)",
        "killsFromBehind": "Most Kills from Behind (Flanker)",
        "lmgDeaths": "Most LMG Deaths (Target Practice)",
        "riotShieldDamageAbsorbed": "Most Damage Absorbed with Riot Shield (Guardian)",
        "flashbangHits": "Most Flashbang Hits (Blinder)",
        "meleeKills": "Most Melee Kills (Brawler)",
        "tagsLargestBank": "Largest Bank (Bank Account)",
        "shotgunKills": "Most Shotgun Kills (Buckshot)",
        "sniperDeaths": "Most Sniper Deaths (Zeroed In)",
        "timeProne": "Most Time Spent Prone (Grassy Knoll)",
        "killstreakWhitePhosphorousKillsAssists": "Most Kills and Assists with White Phosphorus (Burnout)",
        "shortestLife": "Shortest Life (Terminal)",
        "deathsFromBehind": "Most Deaths from Behind (Blindsided)",
        "higherRankedKills": "Most Kills on Higher Ranked Scoreboard Players (Upriser)",
        "mostAssists": "Most Assists (Wingman)",
        "leastKills": "Fewest Kills (The Fearful)",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": ""
    }

    file_path = "stats.json"

    replace_keys_in_json(file_path, replacements)
    print(f"Keys replaced in {file_path}!")