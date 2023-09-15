from bs4 import BeautifulSoup
import requests
import pandas as pd

all_data = []
for i in range(1,9):
    # URL of the web page containing the HTML table to scrap

    #URL for when entries per page is set = 5000
    # and filter set to = "With Coordinates"...8 pages present
    url = 'https://hfr.health.gov.ng/facilities/hospitals-search?_token=3t8E9vOeK2Y7liN0gjzsW3x0z9Ntdt8Lul2CDbcj&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=1&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&facility_name=&entries_per_page=5000&page=' + str(i)
    # URL of the web page containing the HTML table to scrape

    #this URL has only 20 entries per page and contains a total of 1955 pages
    #url = 'https://hfr.health.gov.ng/facilities/hospitals-list?page=' + str(i)

    #URL for when 'All States' are selected on the filter
    # url = 'https://hfr.health.gov.ng/facilities/hospitals-search?_token=lqDSClMX3WVEbiQnIbJfYQKYUajok3Y1WymK3E2l&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=1&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&entries_per_page=500&page=' + str(i)

    #URL for when entries per page is set = 500.
    # url = 'https://hfr.health.gov.ng/facilities/hospitals-search?_token=v37Ezmjpnzm06lHLen3QujAnygzcammHSRzW1K1g&state_id=1&lga_id=1&ward_id=0&facility_level_id=0&ownership_id=0&operational_status_id=1&registration_status_id=0&license_status_id=0&geo_codes=0&service_type=0&service_category_id=0&facility_name=&entries_per_page=500'
    
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
    headers.extend(['longitude', 'latitude', 'physical_location', 'postal_address', 'hiv_capable', 'hours_of_operation'])

    # Loop over each row in the table body and store the data in a list of dictionaries
    data = []
    for tr in table.find_all('tr'):
        row = {}
        for i, td in enumerate(tr.find_all('td')):
            a = td.find('a')
            button = a.find('button') if a else None
            if button and button.get('data-longitude') and button.get('data-latitude'):
                longitude = button.get('data-longitude')
                latitude = button.get('data-latitude')
                physical_location = button.get('data-physical_location')
                postal_address = button.get('data-postal_address')
                hours_of_operation = button.get('data-operational_hours')

                # Search for "HIV/ AIDS Services" label within the td element
                hiv_capable = ""
                hiv_label = td.find('span', {'class': 'label label-default'}, string="HIV/ AIDS Services")
                if hiv_label:
                        hiv_capable = "Yes"
                else:
                        hiv_capable = "Yes"
                        
                row["longitude"] = longitude
                row["latitude"] = latitude
                row["physical_location"] = physical_location
                row["postal_address"] = postal_address
                row["hours_of_operation"] = hours_of_operation
                row["hiv_capable"] = hiv_capable
            row[headers[i]] = td.text.strip() 
        
            
        if row:
            data.append(row)
  
    # Append the data from the current page to the list of all data
    all_data.extend(data)
    
# Create pandas DataFrame from the list of dictionaries
df = pd.DataFrame(all_data)


# export dataframe to an excel workbook
# df.to_excel("./bystate222.xlsx",sheet_name="Hospital list", index=False)

# export dataframe to a CSV file format
df.to_csv("./HFR_additional_headers.csv", index=False)
