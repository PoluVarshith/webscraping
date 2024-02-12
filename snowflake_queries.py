import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd

def execute_sf_query(sql_stmt,schema='REFERENCE'):
    database = "DATACLOUD_TEST"
    #schema = "REFERENCE"
    warehouse = "DATACLOUD_COMPUTE_WH"
    snowflakeaccount = "https://xf56565.west-us-2.azure.snowflakecomputing.com/"
    snowflake_account = "xf56565.west-us-2.azure"
    user = "vpolu"
    password = "k!ndRock64"
    #
    sf_engine = create_engine(URL(account=snowflake_account,
                                user=user,
                                password=password,
                                database=database,
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
    #print(table)
    return table

def get_trackingnums_query(country):
    trackingnums_query = """SELECT TRACKINGNO FROM 
    (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME FROM 
    (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,-30,CURRENT_TIMESTAMP) AND DATEADD(DAY,-7,CURRENT_TIMESTAMP)) P 
    INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE '%USPS%' 
    INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))='""" +country.upper()+"""'  
    INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID  GROUP BY P.TRACKINGNO) 
    WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,-30,CURRENT_TIMESTAMP) AND DATEADD(DAY,-7,CURRENT_TIMESTAMP);"""
    return trackingnums_query

def get_tracknums(trackingnums_query):
    sf_result = execute_sf_query(trackingnums_query)
    #print(sf_result)
    return sf_result

def insert_audit_info(audit_info,country_logger):
    start_datetime = "to_timestamp('" + str(audit_info['START_DATETIME']) + "','DD-MM-YYYY HH24:MI:SS')"
    end_datetime = "to_timestamp('" + str(audit_info['END_DATETIME']) + "','DD-MM-YYYY HH24:MI:SS')" 
    #print(start_datetime,end_datetime)
    values = str((audit_info['POSTAL_SITE_ID'],len(audit_info['ACTUAL_TRACKING_NOS']),len(audit_info['SCRAPING_TRACKING_NOS']),'start_datetime','end_datetime',audit_info['STATUS']))
    values = values.replace("'start_datetime'",start_datetime)
    values = values.replace("'end_datetime'",end_datetime)
    #print(values)
    insert_audit_info_query = """INSERT INTO DATACLOUD_TEST.ETL.WEB_SCRAPING_AUDIT (POSTAL_SITE_ID,
ACTUAL_TRACKING_NOS,SCRAPING_TRACKING_NOS,START_DATETIME,END_DATETIME,STATUS)
VALUES""" + values
    country_logger.info('SQL Query for Audit Table insertion: '+insert_audit_info_query)
    execute_sf_query(insert_audit_info_query,'ETL')
#get_config_table_data()
