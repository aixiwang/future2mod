#---------------------------------------------------------------------------------------------
# future_taoli -- get future price from Sina data source
#
# BSD license is applied to this code
# Copyright by Aixi Wang (aixi.wang@hotmail.com)
#
#---------------------------------------------------------------------------------------------

import time
import time
import random
import json
import sys
import logging
import os
import thread
from json import JSONDecoder, JSONEncoder
#import bsddb
import urllib2


VERSION = 'v0.1'
#BASE_FOLDER = ''
BASE_FOLDER = '/usr/share/nginx/www/img/'
#-------------------------------------
# global variables
#-------------------------------------
global TARGET_N1
global TARGET_N2
global SLEEP_SECS

TARGET_N1 = 'xx'
TARGET_N2 = 'xx'
SLEEP_SECS = 5
 
#-------------------------------------
# get_future_price
#-------------------------------------
def get_future_price(future_name='AG1512'):
    try:
        url = "http://hq.sinajs.cn/?_=%s/&list=%s" %(str(time.time()*1000),future_name)
        #url = "http://hq.sinajs.cn/&list=%s" %(future_name)
        #print 'get_future_price url:',url
        f = urllib2.urlopen(url)
        s = f.read()
        #print s
        f.close()

        if (s.find('var') != 0):
            #print 'get_future_price --- error!'
            return -2,0
        else:
            s3 = s.split(',')
            #print s3
            if float(s3[8]) == 0:
                return -3, float(s3[8])
            else:
                return 0, float(s3[8])
            
    except:
        return -1,0

        
#------------------------------
# format_time_from_linuxtime
#------------------------------
def format_time_from_linuxtime(t):
    s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(t)))
    return s

#------------------------------
# filename_from_date
#------------------------------
def filename_from_date(t):
    s = time.strftime('%Y-%m-%d.csv', time.localtime(float(t)))
    return s
    
#-------------------
# load_config
#-------------------            
def load_config(config_file):
    import ConfigParser
   
    global TARGET_N1
    global TARGET_N2
    global SLEEP_SECS
    
    try:    
        cf = ConfigParser.ConfigParser()
        cf.read(config_file)
        s = cf.sections()
        #o = cf.options("strategy")
        #print 'options:', o
        #v = cf.items("strategy")
        #print 'v:', v
        #EMA_LEN1 = cf.getint("strategy", "EMA_LEN1")
        #DELTA_P = cf.getfloat("strategy", "DELTA_P")
        TARGET_N1 = cf.get("base", "TARGET_N1")
        TARGET_N2 = cf.get("base", "TARGET_N2")
        SLEEP_SECS = cf.getint("base", "SLEEP_SECS")
        
        print '------ base ---------'        
        print 'TARGET_N1:',TARGET_N1
        print 'TARGET_N2:',TARGET_N2
        print 'SLEEP_SECS:',SLEEP_SECS
        return 0
    except:
        print 'get config file error, exit!'
        return -1


    
#-------------------
# readfile
#-------------------
def readfile(filename):
    f = file(filename,'rb')
    fs = f.read()
    f.close()
    return fs
#-------------------
# writefile
#-------------------
def writefile(filename,content):
    f = file(filename,'wb')
    fs = f.write(content)
    f.close()
    return

#-------------------
# writefile2
#-------------------
def writefile2(filename,content):
    f = file(filename,'ab')
    fs = f.write(content)
    f.close()
    return    
#-------------------
# has_file
#-------------------    
def has_file(filename):
    if os.path.exists(filename):
        return True
    else:
        return False
 
#-------------------
# remove_file
#-------------------   
def remove_file(filename):
    if has_file(filename):
        os.remove(filename)

#-------------------
# log_one_record
#-------------------   
def log_one_record(s):
    global TARGET_N1
    global TARGET_N2
    global BASE_FOLDER
    
    writefile2(BASE_FOLDER + TARGET_N1 + '-' + TARGET_N2 + '-' + filename_from_date(time.time()),s + '\r\n')

#-------------------
# log_error
#-------------------   
def log_error(s):
    writefile2('error.log', format_time_from_linuxtime(time.time()) + '\t' + s + '\r\n')
    
#----------------------
# main
#----------------------
if __name__ == "__main__":
    print 'version:' + VERSION
    #load_config(sys.argv[1])
    TARGET_N1 = sys.argv[1]
    TARGET_N2 = sys.argv[2]
    SLEEP_SECS = int(sys.argv[3])   

    import socket
    socket.setdefaulttimeout(10)

    print '\r\nstart to log data ...\r\n'
    print 'TIME\t\t\t' + TARGET_N1 + '\t' + TARGET_N2 + '\t' + 'DIFF'
    while True:
        
        try:
        #if 1:
            # get data
            ret_code1, d1 = get_future_price(TARGET_N1)
            ret_code2, d2 = get_future_price(TARGET_N2)
            
            if (ret_code1 == 0) and (ret_code2 == 0):
                #--------------------------------------------------
                # TODO valid checking
                s = "%s,%s,%s,%s" %(format_time_from_linuxtime(time.time()),str(d1),str(d2),str(d1-d2))
                s1 = "%s\t%s\t%s\t%s" %(format_time_from_linuxtime(time.time()),str(d1),str(d2),str(d1-d2))
                print s1
                log_one_record(s)
                time.sleep(SLEEP_SECS)
                #----------------------------------------------------
            else:
                log_error('get future_price errror')
                print 'get future_price errror'
                time.sleep(5)                
            
            
        except:
            log_error('future_taoli exception')
            print 'future_taoli exception'
            time.sleep(5)
            
            
