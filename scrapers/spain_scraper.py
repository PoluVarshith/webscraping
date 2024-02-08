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
def get_trackinginfo(tracking_num,scraping_url,country_logger,log_country_dir_path=None):
    #tracking_num = 'CY139861975US'
    country_logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    country_logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    logger = logfuns.set_logger(log_country_dir_path,tracking_num=tracking_num)
    logger.info('CURRENT TIME STAMP '+ str(logfuns.get_date_time()))
    logger.info('CURRENT TRACKING NUMBER ' + str(tracking_num))
    try:
        scraping_url = scraping_url.replace('#TRACKING_NUM#',str(tracking_num))
        url = urllib.request.urlopen(scraping_url)
        #url =  urllib.request.urlopen("https://api1.correos.es/digital-services/searchengines/api/v1/?text=" 
        #                            + str(tracking_num) + "&language=EN&searchType=envio") 
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
        logger.info(str((df[['EventDesc','EventDate','EventTime','EventLocation']])))
        country_logger.info(str(tracking_num) +' scraping successful')
        return df
    except:
        country_logger.info(str(tracking_num) + " scraping failed")
        return tocsv.emtpy_frame()

#get_trackinginfo(tracking_num)

def scrape_list(tracking_nums,scraping_url,output_path,logger,log_dir_path):
    #print(len(tracking_nums))
    log_country_dir_path = logfuns.make_logging_country_dir(COUNTRY,log_dir_path)
    country_logger = logfuns.set_logger(log_dir_path,country=COUNTRY)
    country_logger.info("Total Tracking Numbers :" + str(len(tracking_nums)))
    country_logger.info('List of Tracking Numbers ' + str(tracking_nums))
    dfs = []
    threads =[]
    for i in tracking_nums:
        threads.append(twrv.ThreadWithReturnValue(target=get_trackinginfo, args=(i[0],scraping_url,country_logger,log_country_dir_path,)))
    
    for t in threads:
        t.start()

    for t in threads:
        dfs.append(t.join())

    country_frame = tocsv.country_frame(COUNTRY)
    for i in dfs:
        country_frame.df = country_frame.df._append(i,ignore_index=True)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    country_frame.write_to_csv(output_path)
