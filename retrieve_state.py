from bs4 import BeautifulSoup
import requests
import pandas as pd
import duckdb

all_data = []
for i in range(1,80):
    # URL of the web page containing the HTML table to scrape

    #this URL has only 20 entries per page and contains a total of 1955 pages
    #url = 'https://hfr.health.gov.ng/facilities/hospitals-list?page=' + str(i)

    #URL for when 'All States' are selected on the filter
    url = 'https://hfr.health.gov.ng/facilities/hospitals-search?_token=lqDSClMX3WVEbiQnIbJfYQKYUajok3Y1WymK3E2l&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=1&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&entries_per_page=500&page=' + str(i)

    # Fetch the web page content using requests library
    page = requests.get(url).text

    # Create BeautifulSoup object from HTML
    soup = BeautifulSoup(page, 'html.parser')

    # Find the table element in the HTML
    table = soup.find('table')

    # Get the column names from the table header
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip().replace(" ","_").lower())

    # Loop over each row in the table body and store the data in a list of dictionaries
    data = []
    for tr in table.find_all('tr'):
        row = {}
        for i, td in enumerate(tr.find_all('td')):
            row[headers[i]] = td.text.strip()
        if row:
            data.append(row)
    df = pd.DataFrame(data)
    
    # Append the data from the current page to the list of all data
    all_data.extend(data)
    
# Create pandas DataFrame from the list of dictionaries
df = pd.DataFrame(all_data)

# Query definition
myquery = """ SELECT COUNT(*)
            FROM df 
            WHERE state = 'Abia'  
        
        """

abia_df = duckdb.query(myquery)

# Print the resulting DataFrame
print(abia_df)

#df.to_excel("./bystate.xlsx",sheet_name="Hospital number", index=False)