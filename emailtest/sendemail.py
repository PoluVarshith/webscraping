

import snowflake.connector
#from snowflake.sqlalchemy import URL
#from sqlalchemy import create_engine
import pandas as pd
import smtplib
from email.message import EmailMessage
import yaml
from snowflake import connector

connection_details = []
postal_ids_to_countries = {}
with open('config.yaml','r') as config:
    config_data = yaml.safe_load(config)
    #print(config_data)
    connection_details = config_data[config_data['ENV']]

def execute_sf_query(sql_stmt,schema='REFERENCE'):
    try:
        snowflakeaccount = "https://xf56565.west-us-2.azure.snowflakecomputing.com/"
        snowflake_account = "xf56565.west-us-2.azure"
        warehouse = "DATACLOUD_COMPUTE_WH"
        
    #    sf_engine = create_engine(URL(account=snowflake_account,
    #                                user=connection_details['user'],
    #                                password=connection_details['password'],
    #                                database=connection_details['database'],
    #                                schema=schema,
    #                                warehouse=connection_details['warehouse'],
    #                                autocommit=False))
        conn = snowflake.connector.connect(account=snowflake_account,
                                    user=connection_details['user'],
                                    password=connection_details['password'],
                                    database=connection_details['database'],
                                    schema=schema,
                                    warehouse=connection_details['warehouse'])
                                    #autocommit=False)
        #sf_connection = sf_engine.connect()
        cur = conn.cursor()
        cur.execute(sql_stmt)
        result = cur.fetchall()
        conn.close()
        return result
    except Exception as error:
        raise error
    
def check_audit_status(cur_run_id,config_data):
    last_id_query = f"SELECT * from WEB_SCRAPING_AUDIT WHERE RUN_ID = {cur_run_id} AND STATUS='FAILED';"
    audit_entries = execute_sf_query(last_id_query,'ETL')
    #print(last_id_query,audit_entries)
    send_audit_notification(config_data,audit_entries,cur_run_id,postal_ids_to_countries)
    return


def send_audit_notification(config_data,audit_entries,cur_run_id,postal_ids_to_countries):
    sender = config_data['SENDER']['email']
    sender_password = config_data['SENDER']['password']
    receivers = config_data['RECEIVERS']
    print(sender,receivers)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender,sender_password)

    status = [i[3] for i in audit_entries]
    if 0 in status:
        subject = config_data['ENV'] +  '::' + 'Web Scraping ::RUN_ID=' + str(cur_run_id) + '::Failed'
        body = 'The Web Scraping failed for below countries\n' 
        for i in audit_entries:
            if i[3] == 0:
                #body += 'POSTAL_ID=' + str(i[1]) + ' :: COUNTRY NAME=' + str(postal_ids_to_countries[int(i[1])]) + ' :: PASSED TRACKING NUMBERS=' + str(i[2]) + ' :: SUCCESSFUL=' + str(i[3]) + ' :: FAILED=' + str(i[2]-i[3]) + '\n'
                body += 'POSTAL_ID=' + str(i[1]) +"\n"
        #body += 'please look at logs for additional information in the log folder: ' + str(snowflake_queries.session_log_path)
        body += 'please look at logs for additional information in the log folder: ' 
        #print(body)
    #s.sendmail(sender, receivers, body)    
    #s.quite()
#        for i in receivers:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg.set_content(body)
        msg['To'] = receivers
        s.send_message(msg)
    s.quit()

check_audit_status('9',config_data)