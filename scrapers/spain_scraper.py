import urllib.request, json 
import tocsv
import pandas as pd
import twrv
import logfuns
"""
Spain website can only track one item
It needs 30 sec to load fully,  So wait implicitly_wait for 30
It only give Delivary time and data no location
"""
COUNTRY  = 'SPAIN'
def get_trackinginfo(tracking_num,scraping_url,log_country_dir_path):
    #tracking_num = 'CY139861975US'
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        url = urllib.request.urlopen(scraping_url)

        #url =  urllib.request.urlopen("https://api1.correos.es/digital-services/searchengines/api/v1/?text=" 
        #                            + str(tracking_num) + "&language=EN&searchType=envio") 
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        data = json.load(url)
        #print(type(data))
        events  = data['shipment'][0]['events']
        #print(len(events))
        Track_nums = []
        Codes = []
        Dates = []
        Times = []
        Descs = []
        Locs = []
        for i in events:
            if i['extendedText'] not in  ["",'null']:
                Track_nums.append(tracking_num)
                Codes.append('')
                Descs.append(i['extendedText'])
                Dates.append(i['eventDate'])
                Times.append(i['eventTime'])
                Locs.append("")
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

def scrape_list(tracking_nums,scraping_url,output_path,logger,log_dir_path):
    #print(len(tracking_nums))
    #print(COUNTRY,log_dir_path)
    log_country_dir_path = logfuns.make_logging_country_dir(logger,COUNTRY,log_dir_path)
    dfs = []
    threads =[]
    for i in tracking_nums:
        threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],scraping_url,log_country_dir_path,)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path)
