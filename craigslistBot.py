#craigslist bot
#AUTHOR: CHARLES SHEELAM
#DATE: 10/13/22
#DESCRIPTION: CRAIGSLIST BOT TO SCRAPE CRAIGSLIST

#imports 
from asyncio.windows_events import NULL
from contextlib import nullcontext
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import statistics
from statistics import mode

#beautifulsoup
from bs4 import BeautifulSoup
import urllib.request

#pandas libary
import pandas as pd
import openpyxl
from openpyxl import Workbook

#create arrays to store info about each listing
listingTitles = [] #contains complete title of each listing    
listingUrls = [] #contains url of each listing
listingDates = [] #contains date of each listing
listingDesc = [] #contains description of each listing
listingPrices = [] #contains prices of each listing
listingLocations = [] #contains locations of each listing
listingIds = [] #contains unique id for each listing

sleepTime = 1
website = "https://phoenix.craigslist.org/search/sss?query="
item = "couch" #enter name of item here in 'item' variable
completeUrl = website + item

#define craigslistBot class
class bot():
    def __init__(self):
        
        self.driver = driver = webdriver.Chrome(executable_path=r'D:\Users\sheel\Downloads\chromedriver_win32 (1)\chromedriver.exe')
    
    #method to open CraigsList
    def openCl(self):
        
        self.driver.get(completeUrl)
        
    #method to gather links to each listing
    def gatherListings(self):
        
        sleep(sleepTime)
        #contain all listings in one variable 'allListings'
        allListings = self.driver.find_elements(By.CLASS_NAME, "result-row")

        
        #adds titles and urls of all listings in an array - *if title of listing is in appropriate format*
        for listing in allListings:
            
            text = listing.text
            splitText = text.split("\n")

            if len(splitText) != 2:
                continue
            else:
                listingTitles.append(text)
                listingIds.append(listing.get_attribute('data-pid'))
                aTag = listing.find_element(By.CSS_SELECTOR, "a")
                listingUrls.append(aTag.get_attribute('href'))

        sleep(sleepTime)
        
        #close window        
        self.driver.quit()
        
        
        #following code is to extract information from listingTitles and store in appropriate arrays
        for item in listingTitles:
            
            splitInput = item.split("\n")
            
            info = splitInput[1]
            splitInput2 = info.split(" ")
                
                
            #get date and append to listingDates[] array
            month = splitInput2[0]
            day = splitInput2[1]
            date = (month + " " + day)
            splitInput2 = ' '.join(splitInput2[2:])
            listingDates.append(date)
                
            #get description and append to listingDescs[] array
            splitInput3 = splitInput2.split("$")
            itemDesc = (splitInput3[0])
            splitInput4 = splitInput3[1]
            listingDesc.append(itemDesc)
                
            #get price and append to listingPrices[] array
            splitInput5 = splitInput4.split(" ")
            price = splitInput5[0]
            listingPrices.append(price)
            rest = ' '.join(splitInput5[1:])
            
            #add rest of remaining string to listingLocations[] array
            listingLocations.append(rest)
            
#main
newBot = bot()
newBot.openCl()
newBot.gatherListings()

numListings = len(listingTitles)

#for x in range (numListings):
    #print("-----------------------")
    #print("DATE : " + listingDates[x])
    #print("PRICE : $" + listingPrices[x])
    #print("DESCRIPTION : " + listingDesc[x])
    #print("LOCATION : " + listingLocations[x])
    #print("URL : " + listingUrls[x])
    #print("LISTING ID : " + listingIds[x])
    #print("-----------------------")


#calculate average price

    #remove commas (',') from each item in listingPrices[]
for x in range(numListings):

    currListing = str(listingPrices[x])
    removedCommas = currListing.replace(',', '')
    listingPrices[x] = removedCommas

total = 0
average = 0

for x in listingPrices:
    currValue = int(x)

    if currValue <= 1: #exclude values of $1 or $0 from average
        continue
    else:
        total += currValue
average = total/numListings

#calculate most common location
def mostCommon(arr):
    return (mode(arr))

mostCommonLocation =  (mostCommon(listingLocations))


#create pandas DataFrame
df = pd.DataFrame(
    {
        "DATE" : listingDates,
        "PRICE" : listingPrices,
        "DESCRIPTION" : listingDesc,
        "LOCATION" : listingLocations,
        "URL" : listingUrls,
        "LISTING ID" : listingIds,
        "AVERAGE PRICE" : average,
        "MOST COMMON LOCATION" : mostCommonLocation
    }
)

#export DataFrame to excel
with pd.ExcelWriter('couches2.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet 1')
