import difflib
import pandas as pd
import numpy as np
import difflib as dl


df_master = pd.read_csv("./HFR_with_coordinates.csv")
df_hub = pd.read_csv("Complied_hubs_from_IHVN_and_TLMN.csv")

# Create an empty list to store the corrected facility names
corrected_names = []

# Loop through each facility_name record
for name in df_hub['facility_name']:
    hub_state = df_hub['state']
    
    for state in df_hub["state"]:
        # Filter the master dataset based on the state
        filtered_df = df_master.filter(regex='state', axis=1)

         # Check if any match is found
        if name == df_master.items('facility_name'):
            corrected_name = filtered_df.iloc[0]['facility_name']
            corrected_names.append(corrected_name)
            

        # Find closest name match based on percentage accuracy
        best_match = difflib.get_close_matches(name, [facility['name'] for facility in filtered_df], n=1, cutoff=0.8)
        if best_match:
            corrected_names.append(best_match[0])  # Return the best match
        else:
            corrected_names.append("not_found")
        

# Add the corrected names to a new column in the original DataFrame
df_hub['corrected_facility_name'] = corrected_names

# Save the updated DataFrame to a new CSV file
df_hub.to_csv('./updated_dataset.csv', index=False)

