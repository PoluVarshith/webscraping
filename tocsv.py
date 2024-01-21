import pandas as pd
from datetime import datetime
class country_frame:
    def __init__(self,country):
        self.country = country
        Data = {
        'Tracking Number' : [],
        'EventDesc' : [],
        'EventDate' : [],
        'EventTime' : [],
        'EventLocation' : []
        }
        self.df = pd.DataFrame(Data)
        #print(self.df)
    
    def write_to_csv(self):
        #print(self.df[['EventDesc','EventDate','EventTime','EventLocation']])
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        filename = "..\\" + str(self.country) + " " + str(current_datetime)  + '.csv'
        self.df.to_csv(filename, sep=',', index=False, encoding='utf-8')

    
