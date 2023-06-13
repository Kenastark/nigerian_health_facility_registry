import difflib
import pandas as pd
import duckdb



df_master = pd.read_csv("HFR_with_coordinates.csv")
df_hub = pd.read_csv("Complied_hubs_from_IHVN_and_TLMN.csv")

# Create an empty list to store the corrected facility names
corrected_names = []

for name, state in zip(df_hub['facility_name'], df_master['state']):
    # Filter the master DataFrame by state
    filtered_master = df_hub[df_hub['state'] == state]
    
    if name in filtered_master['facility_name'].values:
        corrected_names.append(name)

    else: #looking for best match
        best_match = difflib.get_close_matches(name,filtered_master["facility_name"],n=1,cutoff=0.6) #from 0.6 below the matching becomes less accurate
        #from 0.65 it matches any "General Hospital" to "General Hospital Ohafia"
        # at 0.7 it still matches to "General Hospital Ohafia"
        # at 0.8 it matches a few(3) to "General Hospital Ohafia"
        # at 0.85 it becomes accurate
        if best_match:
            corrected_names.append(best_match[0])
        else:
            corrected_names.append("not_found")


# Add the corrected names to a new column in the original DataFrame
df_hub['corrected_facility_name'] = corrected_names

# Save the updated DataFrame to a new CSV file
df_hub.to_csv('./updated_dataset.csv', index=False)

