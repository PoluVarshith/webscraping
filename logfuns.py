from datetime import datetime,date
import os
import logging
import smtplib
from email.message import EmailMessage

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

def make_logging_dir():
    START_TIME = get_date_time()
    cwd = (os.getcwd())
    path = os.path.join(cwd, 'logs')
    path = os.path.join(path,'SESSION_'+str(START_TIME) + '_log')
    #path = joinpath('./logs',str(START_TIME))
    #print(path)
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
            if i[-1] == 'FAILED':
                body += 'POSTAL_ID=' + str(i[1]) + '::COUNTRY NAME=' + str(postal_ids_to_countries[int(i[1])]) + "::PASSED TRACKING NUMBERS=" + str(i[2]) + "::SUCCESSFUL=" + str(i[3]) + "::FAILED=" + str(i[2]-i[3]) + "\n"
        
        body += 'please look at logs for additional information'
        #print(body)
    
        for i in receivers:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            msg.set_content(body)
            msg['To'] = i
            s.send_message(msg)
    s.quit()