from datetime import datetime,date
import os
import logging

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