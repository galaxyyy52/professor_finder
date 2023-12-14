# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:36:19 2023

@author: E5734C
"""

import json, os

# Path to your JSON file
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory,"professor_index.json")


# Load the existing data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Add the "university" field to each item
university_name = "University of Illinois at Urbana-Champaign"
for item in data:
    item["university"] = university_name

# Write the updated data back to the file
with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=4)

print("University field added successfully.")