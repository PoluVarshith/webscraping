import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
import pandas as pd

def execute_sf_query(sql_stmt):
    database = "DATACLOUD_TEST"
    schema = "RAW"
    warehouse = "DATACLOUD_TEST_WH"
    snowflakeaccount = "https://xf56565.west-us-2.azure.snowflakecomputing.com/"
    snowflake_account = "xf56565.west-us-2.azure"
    user = "SAETLDEV"
    password = "KUZKtGuyw7vEmg7"
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

def get_trackingnums_query(country):
    #sql_quer  = """SELECT COUNT(*) FROM DATACLOUD_TEST.REFERENCE.WEB_SCRAPING_CONFIG_TABLE;;"""
    #country_query = execute_sf_query(sql_quer)
    #print(country_query)
    trackingnums_query = """SELECT TRACKINGNO FROM 
    (SELECT P.TRACKINGNO,MAX(E.EVENT_DATETIME) AS MAX_EVENT_DATETIME FROM 
    (SELECT * FROM DATACLOUD.EDW.PARCEL WHERE DELIVERED_DATE IS NULL AND DATE_PROCESSED BETWEEN DATEADD(DAY,-30,CURRENT_TIMESTAMP) AND DATEADD(DAY,-7,CURRENT_TIMESTAMP)) P 
    INNER JOIN DATACLOUD.EDW.VENDOR V ON P.VENDOR_ID=V.VENDOR_ID AND TRIM(UPPER(V.VENDOR_NAME)) LIKE '%USPS%' 
    INNER JOIN DATACLOUD.EDW.COUNTRY C ON P.COUNTRY_ID=C.COUNTRY_ID  AND TRIM(UPPER(C.COUNTRY_NAME))='SPAIN'  
    INNER JOIN DATACLOUD.EDW.EVENT E ON P.PARCEL_ID=E.PARCEL_ID  GROUP BY P.TRACKINGNO) 
    WHERE MAX_EVENT_DATETIME BETWEEN DATEADD(DAY,-30,CURRENT_TIMESTAMP) AND DATEADD(DAY,-7,CURRENT_TIMESTAMP);"""
    return trackingnums_query

def get_tracknums(trackingnums_query):
    sf_result = execute_sf_query(trackingnums_query)
    #print(sf_result)
    return sf_result