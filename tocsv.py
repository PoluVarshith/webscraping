import pandas as pd
import logfuns
from datetime import datetime


def emtpy_frame():
    #to define output file format
    Data = {
        'Tracking Number' : [],
        'EventCode' : [],
        'EventDesc' : [],
        'EventDate' : [],
        'EventTime' : [],
        'EventLocation' : [],
        'EventZipCode':[],
        'IsInHouse':[]
        }
    
    df = pd.DataFrame(Data)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    return df

def make_frame(Track_nums,Codes,Descs,Dates,Times,Locs,EventZipCode,IsInHouse):
    Data = {
        'Tracking Number' : Track_nums,
        'EventCode' : Codes,
        'EventDesc' : Descs,
        'EventDate' : Dates,
        'EventTime' : Times,
        'EventLocation' : Locs,
        'EventZipCode':EventZipCode,
        'IsInHouse': IsInHouse
        }
    df = pd.DataFrame(Data)
    return df


class country_frame:
    def __init__(self,country):
        self.country = country
        self.df = emtpy_frame()
        #print(self.df)
    
    def write_to_csv(self,output_path,output_dir_path,country_logger):
        #print(self.df[['EventDesc','EventDate','EventTime','EventLocation']])
        current_datetime = logfuns.get_date_time()
        try:
            country_logger.info('Trying to Create Output File in Source Path')
            output_name = output_path + '\\' + str(self.country) + " " + str(current_datetime)  + '.csv'   
            self.df.to_csv(output_name, sep=',', index=False, encoding='utf-8')
            country_logger.info('Created Output File in Source Path')
        except Exception as e :
            country_logger.info('Unable to create Output File in Source Path due to below error:')
            country_logger.info("Error: "+str(e))
            country_logger.info('Tryping to Create Output File in Log folder')
            output_name = output_dir_path + '\\' + str(self.country) + " " + str(current_datetime)  + '.csv'   
            self.df.to_csv(output_name, sep=',', index=False, encoding='utf-8')
            country_logger.info('Created Output File in Log folder')

        #output_name = "\\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Prod\Tracking\Vendor\CommonVendor\sourcepath\\" + str(self.country) + " " + str(current_datetime)  + '.csv'        
        #\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Stage\Tracking\Vendor\CommonVendor\SourcePath
        #\\\\sauw1slprdsftp.file.core.windows.net\\cornerstonesftp\\FTPData\\XPO\\EPG\\Stage\\Tracking\\Vendor\\CommonVendor\\sourcepath\\
    
