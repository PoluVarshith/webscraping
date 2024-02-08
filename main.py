import scraper
import snowflake_queries
import twrv
import logging

def main():
    #countries = []
    table = (snowflake_queries.get_config_table_data())
    print(table)
    threads =[]
    returns = []
    for c in table:
        country = c[0]
        query = c[1]
        if country == 'JAPAN':
            scraping_url = 'https://trackings.post.japanpost.jp/services/srv/search/direct?reqCodeNo1=#TRACKING_NUM#&searchKind=S002&locale=en'
        else:
            scraping_url = "https://api1.correos.es/digital-services/searchengines/api/v1/?text=#TRACKING_NUM#&language=EN&searchType=envio"
        
        output_path = "\\\sauw1slprdsftp.file.core.windows.net\cornerstonesftp\FTPData\XPO\EPG\Prod\Tracking\Vendor\CommonVendor\sourcepath\\"
        #print(country,query)#,c[11],c[12])
        threads.append(twrv.ThreadWithReturnValue(target=scraper.scrape, args=(country,query,scraping_url,output_path,)))

    for t in threads:
        t.start()

    for t in threads:
        returns.append(t.join())

def main_test():
    countries = ['SPAIN']
    for i in countries:
        scraper.scrape_test(i)

#main_test()
main()