import json
import os
from json.decoder import JSONDecodeError

def pretty_print_json_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
            data = json.loads(content)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)
    except JSONDecodeError as e:
        print(f"Error decoding JSON in {input_file}: {e}")

# Hardcoding the input and output file paths
input_file = 'stats.json'
output_file = 'stats_temp.json'

pretty_print_json_file(input_file, output_file)

# Remove the original file and rename the beautified file
os.remove(input_file)
os.rename(output_file, input_file)