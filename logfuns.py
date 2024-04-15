from datetime import datetime,date
import os
import logging
import smtplib
from email.message import EmailMessage
import snowflake_queries

def get_date_time():
    today = date.today()
    Date = today.strftime('%Y-%m-%d')
    now = datetime.now()
    Time = now.strftime("%H_%M")
    START_TIME = Date + ' ' + Time
    #print(START_TIME)
    return START_TIME

def get_date_time_normal_format():
    today = date.today()
    Date = today.strftime('%Y-%m-%d')
    now = datetime.now()
    Time = now.strftime("%H:%M")
    START_TIME = Date + ' ' + Time
    #print(START_TIME)
    return START_TIME

def make_logging_dir(log_path):
    START_TIME = get_date_time()
    #cwd = (os.getcwd())
    #path = os.path.join(cwd, 'logs')
    #print(path)
    #path = r"C:\Users\vpolu\Desktop\WebScraping\webscraping\logs"
    path = os.path.join(log_path,'SESSION_'+str(START_TIME) + '_log')
    os.mkdir(path)
    output_path = os.path.join(path,'output_csvs')
    os.mkdir(output_path)
    return path,output_path


def make_logging_filepath(path,country=None,tracking_num=None):
    START_TIME = get_date_time()
    if tracking_num == None and country == None:
        path = os.path.join(path,'SESSION_'+str(START_TIME)+ '_log' +'.txt')
        return path
    elif country != None:
        path = os.path.join(path,str(country) + '_' +str(START_TIME) + '_log' +'.txt')
        return path
    else:
        path = os.path.join(path,str(tracking_num) + '_log' +'.txt')
        return path


def make_logging_country_dir(COUNTRY,log_dir_path):
    path = os.path.join(log_dir_path,str(COUNTRY) + '_' + str(get_date_time()) + '_log')
    #print('here',path)
    os.mkdir(path)
    return path

def set_logger(log_dir_path,country=None,tracking_num=None):
    if tracking_num == None and country == None :
        name = make_logging_filepath(log_dir_path) 
    elif country != None:
        name = make_logging_filepath(log_dir_path,country=country)       
    else :
        name = make_logging_filepath(log_dir_path,tracking_num)

    logger = logging.getLogger(name)
    formatter = logging.Formatter(
    fmt="%(asctime)s, %(levelname)-s | %(filename)-s:%(lineno)-s | %(threadName)s: %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S")
    sh = logging.StreamHandler()
    fh = logging.FileHandler(f"{name}.log")
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    #logger.addHandler(sh)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


"""logging.basicConfig(filename=make_logging_filepath(log_dir_path),
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')"""

def send_audit_notification(config_data,audit_entries,cur_run_id,postal_ids_to_countries):
    sender = config_data['SENDER']['email']
    sender_password = config_data['SENDER']['password']
    receivers = config_data['RECEIVERS']
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender,sender_password)
    status = [i[3] for i in audit_entries]
    if 0 in status:
        subject = config_data['ENV'] +  '::' + 'Web Scraping ::RUN_ID=' + str(cur_run_id) + '::Failed'
        body = 'The Web Scraping failed for below countries\n' 
        for i in audit_entries:
            if i[3] == 0:
                body += 'POSTAL_ID=' + str(i[1]) + ' :: COUNTRY NAME=' + str(postal_ids_to_countries[int(i[1])]) + " :: PASSED TRACKING NUMBERS=" + str(i[2]) + " :: SUCCESSFUL=" + str(i[3]) + " :: FAILED=" + str(i[2]-i[3]) + "\n"
        
        body += 'please look at logs for additional information in the log folder: ' + str(snowflake_queries.session_log_path)
        #print(body)
    
        #for i in receivers:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg.set_content(body)
        msg['To'] = receivers
        s.send_message(msg)
    s.quit()

# Austria :CY141273077US

def change_time(time,date,offset):
    #print(time,date,offset,'here')
    hr,mn = [int(x) for x in time.split(":")]
    yyyy,mm,dd = [int(x) for x in date.split("/")]
    #print(hr,mn,yyyy,mm,dd,'here')
    mn = mn - offset[1]
    if mn < 0:
        hr = hr -1
        mn = mn + 60

    hr = hr - offset[0]
    if hr < 0 :
        dd = dd - 1
        hr = hr + 24
        if dd == 0:
            mm = mm -1
            if mm == 0:
                mm = 12
                yyyy = yyyy - 1
            if mm in [1,3,5,7,8,10,12]:
                dd = 31
            else :
                dd = 30
    if hr > 24:
        hr = hr -24
        dd = dd + 1
        if mm in [1,3,5,7,8,10,12]:
            if dd > 31:
                dd = dd - 31
                mm = mm + 1
                if mm > 12:
                    mm = mm-12
                    yyyy = yyyy + 1
        elif mm in [2,4,6,9,11]:
            if dd >30:
                dd = dd - 30
                mm = mm + 1
                
    new_time = ':'.join([str(hr),str(mn)])
    new_date = '/'.join([str(yyyy),str(mm),str(dd)])
    #print(new_time,new_date,'down here')
    #print(hr,mn,dd,mm,yyyy,'down here')
    #new_time = time
    #new_date = date
    return new_time,new_date