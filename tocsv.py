import pandas as pd

class country_csv:
    def __init__(self):
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
        self.df.to_csv('..\info.csv', sep=',', index=False, encoding='utf-8')

    
