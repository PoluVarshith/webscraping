import urllib.request, json 
import tocsv
import pandas as pd
import twrv
from deep_translator import GoogleTranslator
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
This website can track more than one shipment
"""
COUNTRY = 'GERMANY'
def get_trackinginfo(tracking_num):
    #tracking_num ='CY139955908US'
    try:
        print(tracking_num)
        url = ('https://www.deutschepost.de/int-verfolgen/data/search?piececode=' +
                    str(tracking_num) + '&inputSearch=true&language=en')
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        #print(driver.page_source)
        data = driver.find_element(By.TAG_NAME,'body').text
        data = json.loads(data)
        #print(type(data))
        try :
            events = data['sendungen'][0]['sendungsdetails']['sendungsverlauf']['events']
        except:
            #print("too many shipments with one tracking number?")
            return tocsv.emtpy_frame()
        #print(len(events))
        driver.close()
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        for i in events:
            if 'status' in i.keys() and i['status'] not in  ["",'null'] :
                Track_nums.append(tracking_num)
                Codes.append('')
                Descs.append(i['status'])
                date,time = i['datum'].split('T')
                #print(date,time)
                Dates.append(date)
                Times.append(time)
                try:
                    Locs.append(i['ort'])
                except:
                    Locs.append('')
        #print(len(Track_nums),len(Descs))

        Data = {
        'Tracking Number' : Track_nums,
        'EventCode' : Codes,
        'EventDesc' : Descs,
        'EventDate' : Dates,
        'EventTime' : Times,
        'EventLocation' : Locs
        }
        df = pd.DataFrame(Data)
        return df
    except:
        print("can't fetch data")
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)
def split_list(lst, chunk_size):
    chunks = [[] for _ in range((len(lst) + chunk_size - 1) // chunk_size)]
    for i, item in enumerate(lst):
        chunks[i // chunk_size].append(item)
    return chunks

def scrape_list(tracking_nums):
    #print(len(tracking_nums))
    dfs = []
    chunk_size = 5
    batches = split_list(tracking_nums, chunk_size)
    for batch in batches:
        threads =[]
        for i in batch:
            threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],)))
        
        for t in threads:
            t.start()

        for t in threads:
            dfs.append(t.join())


    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv()