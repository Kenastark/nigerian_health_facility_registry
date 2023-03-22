#test code to change the url each time to loop over the page in a website

for i in range(1,21):
    # URL of the web page containing the HTML table to scrape
    url = 'https://hfr.health.gov.ng/facilities/hospitals-list?page=' + str(i) 

    print(url)