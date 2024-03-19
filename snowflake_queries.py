import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd
import logfuns

connection_details = []
postal_ids_to_countries = {}
session_log_path = ''
def execute_sf_query(sql_stmt,schema='REFERENCE'):
    snowflakeaccount = "https://xf56565.west-us-2.azure.snowflakecomputing.com/"
    snowflake_account = "xf56565.west-us-2.azure"
    warehouse = "DATACLOUD_COMPUTE_WH"
    
    sf_engine = create_engine(URL(account=snowflake_account,
                                user=connection_details['user'],
                                password=connection_details['password'],
                                database=connection_details['database'],
                                schema=schema,
                                warehouse=warehouse,
                                autocommit=False))
    sf_connection = sf_engine.connect()
    result = sf_connection.execute(sql_stmt).fetchall()
    sf_connection.close()
    return result

def get_config_table_data():
    #schema_quer = """DESCRIBE TABLE DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE;"""
    #schema = execute_sf_query(schema_quer)
    #print(schema)
    data_query  = """SELECT POSTAL_SITE_ID,COUNTRY_NAME,REPLACE(REPLACE(REPLACE(SELECT_SQL,'#COUNTRY_NAME#',COUNTRY_NAME),'#MIN_SELECTED_DAYS#',MIN_SELECTED_DAYS),'#MAX_SELECTED_DAYS#',MAX_SELECTED_DAYS) AS SEL_SQL,SCRAPING_URL,OUTPUT_PATH FROM REFERENCE.WEB_SCRAPING_CONFIG_TABLE WHERE IS_ACTIVE=1;"""
    table = execute_sf_query(data_query)
    return table

#def get_trackingnums_query(country):
#    trackingnums_query = """SELECT TRACKINGNO FROM 
#    (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME FROM 
#    (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,-30,CURRENT_TIMESTAMP) AND DATEADD(DAY,-7,CURRENT_TIMESTAMP)) P 
#    INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE '%USPS%' 
#    INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))='""" +country.upper()+"""'  
#    INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID  GROUP BY P.TRACKINGNO) 
#    WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,-30,CURRENT_TIMESTAMP) AND DATEADD(DAY,-7,CURRENT_TIMESTAMP);"""
#    return trackingnums_query

def get_tracknums(trackingnums_query):
    sf_result = execute_sf_query(trackingnums_query)
    #print(sf_result)
    return sf_result

def insert_audit_info(audit_info,country_logger):
    start_datetime = "to_timestamp('" + str(audit_info['START_DATETIME']) + "','YYYY-MM-DD HH24:MI')"
    end_datetime = "to_timestamp('" + str(audit_info['END_DATETIME']) + "','YYYY-MM-DD HH24:MI')" 
    #print(start_datetime,end_datetime)
    values = str((audit_info['RUN_ID'],audit_info['POSTAL_SITE_ID'],len(audit_info['ACTUAL_TRACKING_NOS']),len(audit_info['SCRAPING_TRACKING_NOS']),'start_datetime','end_datetime',audit_info['STATUS']))
    values = values.replace("'start_datetime'",start_datetime)
    values = values.replace("'end_datetime'",end_datetime)
    #print(values)
    insert_audit_info_query = """INSERT INTO DATACLOUD_TEST.ETL.WEB_SCRAPING_AUDIT (RUN_ID,POSTAL_SITE_ID,
ACTUAL_TRACKING_NOS,SCRAPING_TRACKING_NOS,START_DATETIME,END_DATETIME,STATUS)
VALUES""" + values
    #print('SQL Query for Audit Table insertion: '+insert_audit_info_query)
    country_logger.info('SQL Query for Audit Table insertion: '+insert_audit_info_query)
    execute_sf_query(insert_audit_info_query,'ETL')
    
    
def get_prev_run_id():
    prev_id_query = """SELECT MAX(RUN_ID) from WEB_SCRAPING_AUDIT;"""
    prev_id = execute_sf_query(prev_id_query,'ETL')[0][0]
    if prev_id == None:
        prev_id = 0
    else:
        prev_id = int(prev_id)
    #print('prev_id',prev_id)
    return prev_id

def check_audit_status(cur_run_id,config_data):
    if cur_run_id == 0:
        last_id_query = """SELECT * from WEB_SCRAPING_AUDIT;"""
    else:
        last_id_query = """SELECT * from WEB_SCRAPING_AUDIT WHERE RUN_ID = CUR_ID;"""
        last_id_query = last_id_query.replace('CUR_ID',str(cur_run_id))

    audit_entries = execute_sf_query(last_id_query,'ETL')
    #print(last_id_query,audit_entries)
    logfuns.send_audit_notification(config_data,audit_entries,cur_run_id,postal_ids_to_countries)
    return

