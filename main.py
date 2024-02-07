import scraper
import snowflake_queries
import twrv

def main():
    #countries = []
    table = (snowflake_queries.get_config_table_data())
    threads =[]
    returns = []
    for c in table:
        country = c[2]
        if country in ['SPAIN','JAPAN']:
            query = c[10]
            query = query.replace('#COUNTRY_NAME#',c[2].upper())
            query = query.replace('#MAX_SELECTED_DAYS#',str(c[12]))
            query = query.replace('#MIN_SELECTED_DAYS#',str(c[11]))
            #print(query)#,c[11],c[12])
            threads.append(twrv.ThreadWithReturnValue(target=scraper.scrape, args=(country,query,)))

    for t in threads:
        t.start()

    for t in threads:
        returns.append(t.join())

def main_test():
    countries = ['JAPAN']
    for i in countries:
        scraper.scrape_test(i)

#main_test()
main()