import difflib
import pandas as pd
import numpy as np


df_master = pd.read_csv("./HFR_with_coordinates_test.csv")
df_hub = pd.read_csv("_link to hubs csv formated as state, LGA, facility name")

def match_and_correct_name(name, stage, lga, master_list):
    # Filter master list by stage and LGA
    filtered_list = [facility for facility in master_list if facility['stage'] == stage and facility['lga'] == lga]

    # Check for exact name match
    exact_match = [facility for facility in filtered_list if facility['name'] == name]
    if exact_match:
        return exact_match[0]['name']  # Return the exact match

    # Find closest name match based on percentage accuracy
    best_match = difflib.get_close_matches(name, [facility['name'] for facility in filtered_list], n=1, cutoff=0.8)
    if best_match:
        return best_match[0]  # Return the best match

    # If no match found, return None
    return None

# Example usage
master_list = [
    {'name': 'Facility A', 'stage': 'Stage 1', 'lga': 'LGA 1'},
    {'name': 'Facility B', 'stage': 'Stage 2', 'lga': 'LGA 2'},
    {'name': 'Facility C', 'stage': 'Stage 1', 'lga': 'LGA 2'},
    {'name': 'Facility D', 'stage': 'Stage 3', 'lga': 'LGA 3'}
]

name = 'Fecility A'
stage = 'Stage 1'
lga = 'LGA 1'

corrected_name = match_and_correct_name(name, stage, lga, master_list)
if corrected_name:
    print(f"Match found: {corrected_name}")
else:
    print("No match found.")

