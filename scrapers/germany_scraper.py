import urllib.request, json 
from urllib.request import urlopen
import tocsv
import pandas as pd
import twrv
from deep_translator import GoogleTranslator
"""
This website can track more than one shipment
It needs 30 sec to load fully,  So implicitly_wait for 30
"""
COUNTRY = 'GERMANY'
def get_trackinginfo(tracking_num):
    tracking_num ='LV770224450US'
    if True:
        print('hello')
        url =  urlopen("https://www.deutschepost.de/int-verfolgen/data/search?piececode=LV770291794US&inputSearch=true&language=en") 
        print('hello')
        print(url)
        data = json.load(url)
        print((data))
        events  = data['shipment'][0]['events']
        #print(len(events))
        Track_nums = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        for i in events:
            if i['extendedText'] not in  ["",'null']:
                Track_nums.append(tracking_num)
                Descs.append(i['extendedText'])
                Dates.append(i['eventDate'])
                Times.append(i['eventTime'])
                Locs.append("")
        #print(len(Track_nums),len(Descs))

        Data = {
        'Tracking Number' : Track_nums,
        'EventDesc' : Descs,
        'EventDate' : Dates,
        'EventTime' : Times,
        'EventLocation' : Locs
        }
        df = pd.DataFrame(Data)
        return df
    else:
        print("can't fetch data")
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)

def scrape_list(tracking_nums):
    #print(len(tracking_nums))
    dfs = []
    for i in tracking_nums[:1]:
        dfs.append(get_trackinginfo(i[0]))

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv()