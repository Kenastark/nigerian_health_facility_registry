import difflib
import pandas as pd
import duckdb
import difflib as dl


df_master = pd.read_csv("Complied_hubs_from_IHVN_and_TLMN.csv")
df_hub = pd.read_csv("Complied_hubs_from_IHVN_and_TLMN.csv")

# Create an empty list to store the corrected facility names
corrected_names = []

for name in df_hub['facility_name']:

    for state in df_hub["state"]:

        #filter the master list by state
        filter_master = duckdb.query (
        "SELECT * FROM df_master WHERE state =" + '"' + state + '"').to_df()

        #comparing facility name in hub to facility name in master
        for master_name in filter_master:
            if name == master_name:
                
                corrected_names.append(name)
            else: #looking for best match
                best_match = difflib.get_close_matches(name,filter_master["facility_name"],n=1,cutoff=0.8)
                corrected_names.append(best_match)
            
            corrected_names.append("not_found")

# Add the corrected names to a new column in the original DataFrame
df_hub['corrected_facility_name'] = corrected_names

# Save the updated DataFrame to a new CSV file
df_hub.to_csv('./updated_dataset.csv', index=False)

