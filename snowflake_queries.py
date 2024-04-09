import snowflake.connector
#from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import logfuns

connection_details = []
postal_ids_to_countries = {}
session_log_path = ''
def execute_sf_query(sql_stmt,schema='REFERENCE'):
    try:
        snowflakeaccount = "https://xf56565.west-us-2.azure.snowflakecomputing.com/"
        snowflake_account = "xf56565.west-us-2.azure"
        warehouse = "DATACLOUD_COMPUTE_WH"
        
        conn = snowflake.connector.connect(account=snowflake_account,
                                    user=connection_details['user'],
                                    password=connection_details['password'],
                                    database=connection_details['database'],
                                    schema=schema,
                                    warehouse=connection_details['warehouse'])
                                    #autocommit=False)
        cur = conn.cursor()
        cur.execute(sql_stmt)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as error:
        raise error

def get_config_table_data():

    data_query  = """SELECT POSTAL_SITE_ID,COUNTRY_NAME,REPLACE(REPLACE(REPLACE(SELECT_SQL,'#COUNTRY_NAME#',COUNTRY_NAME),'#MIN_SELECTED_DAYS#',MIN_SELECTED_DAYS),'#MAX_SELECTED_DAYS#',MAX_SELECTED_DAYS) AS SEL_SQL,SCRAPING_URL,OUTPUT_PATH FROM REFERENCE.WEB_SCRAPING_CONFIG_TABLE WHERE IS_ACTIVE=1;"""
    table = execute_sf_query(data_query)
    return table

def get_tracknums(trackingnums_query):
    sf_result = execute_sf_query(trackingnums_query)
    #print(sf_result)
    return sf_result

def insert_audit_info(audit_info,country_logger):
    start_datetime = "to_timestamp('" + str(audit_info['START_DATETIME']) + "','YYYY-MM-DD HH24:MI')"
    end_datetime = "to_timestamp('" + str(audit_info['END_DATETIME']) + "','YYYY-MM-DD HH24:MI')" 
    #print(start_datetime,end_datetime)
    values = str((audit_info['RUN_ID'],audit_info['POSTAL_SITE_ID'],len(audit_info['ACTUAL_TRACKING_NOS'])-len(audit_info['DISCARDED_TRACKING_NOS']),len(audit_info['SCRAPED_TRACKING_NOS']),'start_datetime','end_datetime',audit_info['STATUS']))
    values = values.replace("'start_datetime'",start_datetime)
    values = values.replace("'end_datetime'",end_datetime)
    #print(values)
    insert_audit_info_query = """INSERT INTO ETL.WEB_SCRAPING_AUDIT (RUN_ID,POSTAL_SITE_ID,
ACTUAL_TRACKING_NOS,SCRAPING_TRACKING_NOS,START_DATETIME,END_DATETIME,STATUS)
VALUES""" + values
    #print('SQL Query for Audit Table insertion: '+insert_audit_info_query)
    country_logger.info('SQL Query for Audit Table insertion: '+insert_audit_info_query)
    execute_sf_query(insert_audit_info_query,'ETL')
    
    
def get_prev_run_id():
    prev_id_query = """SELECT NVL(MAX(RUN_ID),0) from ETL.WEB_SCRAPING_AUDIT;"""
    prev_id = execute_sf_query(prev_id_query,'ETL')[0][0]
    if prev_id == None:
        prev_id = 0
    else:
        prev_id = int(prev_id)
    #print('prev_id',prev_id)
    return prev_id

def check_audit_status(cur_run_id,config_data):
    last_id_query = f"SELECT * from WEB_SCRAPING_AUDIT WHERE RUN_ID = {cur_run_id} AND STATUS='FAILED';"
    audit_entries = execute_sf_query(last_id_query,'ETL')
    #print(last_id_query,audit_entries)
    logfuns.send_audit_notification(config_data,audit_entries,cur_run_id,postal_ids_to_countries)
    return

