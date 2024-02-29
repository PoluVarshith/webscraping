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
    
    def write_to_csv(self,output_path,output_dir_path):
        #print(self.df[['EventDesc','EventDate','EventTime','EventLocation']])
        current_datetime = logfuns.get_date_time()
        try:
            output_name = output_path + '\\' + str(self.country) + " " + str(current_datetime)  + '.csv'   
            self.df.to_csv(output_name, sep=',', index=False, encoding='utf-8')
        except:
            output_name = output_dir_path + '\\' + str(self.country) + " " + str(current_datetime)  + '.csv'   
            self.df.to_csv(output_name, sep=',', index=False, encoding='utf-8')

        #output_name = "\\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Prod\Tracking\Vendor\CommonVendor\sourcepath\\" + str(self.country) + " " + str(current_datetime)  + '.csv'        
        #\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Stage\Tracking\Vendor\CommonVendor\SourcePath
        #\\\\sauw1slprdsftp.file.core.windows.net\\cornerstonesftp\\FTPData\\XPO\\EPG\\Stage\\Tracking\\Vendor\\CommonVendor\\sourcepath\\
    
