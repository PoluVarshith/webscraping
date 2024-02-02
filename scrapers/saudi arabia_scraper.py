import urllib.request, json 
import tocsv
import pandas as pd
import twrv
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wait implicitly_wait for 30
It only give Delivary time and data no location
"""
COUNTRY  = 'SAUDI ARABIA'
def get_trackinginfo(tracking_num):
    tracking_num = 'CY363813004US'
    try:
        url =  urllib.request.urlopen("https://splonline.com.sa/umbraco/api/tools/trackshipment?language=en&shipmentCode="
                                    + str(tracking_num)) 
        data = json.load(url)
        #print(type(data))
        events  = data[0]['TrackingInfoItemList']
        #print('Number of events',len(events))
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        for i in events:
            if i['StatusMessage'] not in  ["",'null']:
                Track_nums.append(tracking_num)
                Codes.append('')
                Descs.append(i['StatusMessage'].strip())
                date,time = i['EventDateTime'].split('T')
                #print(date,time)
                Dates.append(date)
                Times.append(time)
                Locs.append(i['Office']+ " " + i['OfficeCode'])
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

def scrape_list(tracking_nums):
    #print(len(tracking_nums))
    dfs = []
    threads =[]
    for i in tracking_nums[:10]:
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
