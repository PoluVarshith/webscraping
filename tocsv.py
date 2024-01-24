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
    
    def write_to_csv(self):
        #print(self.df[['EventDesc','EventDate','EventTime','EventLocation']])
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        filename = "..\\" + str(self.country) + " " + str(current_datetime)  + '.csv'
        self.df.to_csv(filename, sep=',', index=False, encoding='utf-8')

    
