import pandas as pd
from datetime import datetime

def emtpy_frame():
    #to define output file format
    Data = {
        'Tracking Number' : [],
        'EventCode' : [],
        'EventDesc' : [],
        'EventDate' : [],
        'EventTime' : [],
        'EventLocation' : []
        }
    
    df = pd.DataFrame(Data)
    #print(df[['EventDesc','EventDate','EventTime','EventLocation']])
    return df

class country_frame:
    def __init__(self,country):
        self.country = country
        self.df = emtpy_frame()
        #print(self.df)
    
    def write_to_csv(self,output_path):
        #print(self.df[['EventDesc','EventDate','EventTime','EventLocation']])
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_name = "..\\" + str(self.country) + " " + str(current_datetime)  + '.csv'
        #output_name = output_path + str(self.country) + " " + str(current_datetime)  + '.csv'        
        #output_name = "\\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Prod\Tracking\Vendor\CommonVendor\sourcepath\\" + str(self.country) + " " + str(current_datetime)  + '.csv'        
        self.df.to_csv(output_name, sep=',', index=False, encoding='utf-8')

    
