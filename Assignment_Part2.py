from os import path
from bs4 import BeautifulSoup
import json
import ndjson
import os.path
import requests

#json file path
filename = './wiki.json'

#########################
### Scraping Function ###
#########################
# Reference: 
# https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/
# https://qiita.com/eg_i_eg/items/aff02f6057b476cb15fa
def scrapeWiki(url, visit_list, n, n_remain):
    try:
        link_list=[]
        print("Scraping ", n_remain + 1, " times:")
        
        ### 1-2) Accepts a Wikipedia link - return/throw an error if the link is not a valid wiki link
        response = requests.get(url)
        #print(response.status_code)
        if not response.status_code == 200:
            print("[exit code=-3] The link is not valid.")
            exit()

        soup = BeautifulSoup(response.content, 'html.parser')
        #title = soup.find(id="firstHeading")
        #print(title.content)

        # Get Wikipedia title
        # to avoid AttributeError: 'NoneType' object has no attribute 'string' 
        if soup.find( class_= "mw-page-title-main" ) != None:
            title = soup.find( class_= "mw-page-title-main" ).string
        else:
            title = soup.find( "title" )
        print("[", title.string, "]", url)

        # Get all <a> tag
        allLinks = soup.find(id="bodyContent").find_all("a")
        
        ### 3) Scrape the link provided in Step 1, for all wiki links embedded in the page and store them in a data structure of your choice.
        for link in allLinks:

            # to avoid AttributeError: 'NoneType' object has no attribute 'find' 
            if link.get('href') == None:
                continue

            # Get href="/wiki/" 
            if link.get('href').find("/wiki/") == -1:
                continue

            # Create wiki url
            link_embedded = "https://en.wikipedia.org" + link['href']
            
            #Optional-1) Optimize your code not to visit any links you've already visited.    
            if (link_embedded in visit_list) == False:
                visit_list.append(link_embedded)
            
            #if (link_embedded in link_list) == False:
            link_list.append(link_embedded)

        # Prepare Json data
        json_dict = {str(title.string): url,
                        'all found links' : link_list, 
                        'total count' : len(link_list),
                        'unique count' : len(set(link_list))}
        # write Json
        with open(filename, 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(json_dict)

        n_remain = n_remain + 1
        ### 4) Repeat Step 3 for all newly found links and store them in the same data structure.
        ### 5) This process should terminate after n cycles.
        if n_remain < int(n, 10):
            if len(visit_list) > n_remain:
                next_url = visit_list[n_remain -1]
                scrapeWiki(next_url, visit_list, n, n_remain)


    # handle error
    except Exception as e:
        print ("=== An Error Occured ===")
        print ("type: ",  str(type(e)))
        print ("args: " + str(e.args))
        print ("message: " + e.message)
        print ("e: " + str(e))



#########################
###   Main Function   ###
#########################
### 1-1) Accepts a Wikipedia link - return/throw an error if the link is not a valid wiki link
wiki_link = input("Please input a wiki link: ")
#wiki_link="https://en.wikipedia.org/wiki/LinkedIn"

### 2) Accepts a valid integer between 1 to 20 - call it n
n = input("Please input a number between 1 to 20: ")

# check if the input number is valid
try:
    int(n, 10)  # convert an input string to an integer

except ValueError: # not an integer
    print("[exit code=-1] Input is not a number.")
    exit()

if int(n, 10) < 1 or 20 < int(n, 10): # not 1-20
    print("[exit code=-2] Input number is not between 1 and 20.")
    exit()

wiki_visit_list=[]
n_remain = 0

#if json file exists, delete the file
if os.path.exists(filename) == True:
    os.remove(filename)

print()
#invoke scarpe function
scrapeWiki(wiki_link, wiki_visit_list, n, n_remain)
print()
print("Jason file is created in the same folder as this script. Please check the file.")