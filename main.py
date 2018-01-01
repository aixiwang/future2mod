#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# based on https://github.com/firatkucuk/modslave
#---------------------------------------------------------------------------------------------
# future2mod -- map future price to modbus tcp interface
#
# BSD license is applied to this code
# Copyright by Aixi Wang (aixi.wang@hotmail.com)
#---------------------------------------------------------------------------------------------


# [dependencies] #######################################################################################################

import socket
import json
import thread
import future
import random

from modbus import request, response


# [globals] ############################################################################################################

tables  = [
    [0] * 65536,   # discreteOutputCoils - 0000 to FFFF - 65536 bits
    [0] * 65536,   # discreteInputContacts - 0000 to FFFF - 65536 bits
    [0] * 65536,   # analogOutputRegisters - 0000 to FFFF - 65535 words
    [0] * 65536    # analogInputRegisters - 0000 to FFFF - 65535 words
]


# [inject_analog_table] ##############################################################################################

def inject_analog_table(table_id, config_table):

    for index in config_table:
        reference = int(index)

        if config_table[index] > 65535 or config_table[index] < 0:
            tables[table_id][reference] = 0
        else:
            tables[table_id][reference] = int(config_table[index])


# [inject_discrete_table] ##############################################################################################

def inject_discrete_table(table_id, config_table):

    for index in config_table:
        reference = int(index)

        if config_table[index] > 0:
            tables[table_id][reference] = 1
        else:
            tables[table_id][reference] = 0


# [inject_config] ######################################################################################################

def inject_config():

    inject_discrete_table(0, config["tables"]["discreteOutputCoils"])
    inject_discrete_table(1, config["tables"]["discreteInputContacts"])
    inject_analog_table(2, config["tables"]["analogOutputRegisters"])
    inject_analog_table(3, config["tables"]["analogInputRegisters"])


# [main block] #########################################################################################################

if __name__ == "__main__":

    config  = json.load(open('config.json'))
    host    = config["listenAddress"]
    port    = config["listenPort"]
    backlog = 5
    size    = 1024

    inject_config()
    #print tables[3][0]
    #print tables[3][1]
    #print tables[3][2]
    
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    socket_server.listen(backlog)

    while True:
        try:
            client, address = socket_server.accept()    
            while True:
                try:
                    data = client.recv(size)
                    # print "connected"
                    if data:
                        #retcode,p = future.get_future_price('RB1805')
                        #if retcode == 0:
                        #    tables[2][0] = int(p)
                        #else:
                        #    tables[2][0] = 0
                        i = random.randint(0,1000)
                        tables[2][0] = i
                        tables[3][0] = i
                        print '-------------------------------'
                        req = request.Request(data)
                        res = response.Response(req, tables)
                        out = res.out()

                        print "request : ", ':'.join(x.encode('hex') for x in data)
                        print "response: ", ':'.join(x.encode('hex') for x in out)

                        client.send(out)
                        
                    else:
                        print 'break 1'
                        break
                except Exception as e:
                    print 'exception 1:' + str(e)
                    break
        
        except Exception as e:
            print 'exception 2:' + str(e)
            

