#!/usr/bin/python

import socket
import argparse
import sys
import datetime
import select


# argument parsing and program info
desc = """
Simple honeypot that reads a banner from a file and displays it to the
client. It logs the data received to a file 
"""

parser = argparse.ArgumentParser(description=desc)
parser.add_argument(
    '-f',
    help = 'File to read banner from',
    dest = 'banner_file',
    type = str,
    required = True
    )
parser.add_argument(
    '-p',
    help = 'Port to listen on',
    dest = 'port',
    type = int,
    required = True
    )
args = parser.parse_args()
argdict = vars(args)

infile = argdict['banner_file']
port = argdict['port']


# current date and time
now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d %H:%M')
today = now.strftime('%Y-%m-%d')


def getBanner(input_file):
    """Get banner from file"""
    try:
        with open(input_file) as f:
            banner = f.read()
        return banner
    except IOError, e:
        print e
        sys.exit(1)


def logActions(data):
    """"Write data to file"""
    try:
        with open(today +'.log', 'a') as outfile:
            outfile.write(data)
        return
    except IOError, e:
        print e
        sys.exit(1)

    
# server setup
BACKLOG = 5 # value of queued connections
HOST = '' # this refers to all available interfaces
SIZE = 1024 # size for the data buffer

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make socket reusable
    s.bind((HOST, port))
    s.listen(BACKLOG)
    print 'Listening on port %d on %s' % (port, date)

except socket.error, e:
    print e
    s.close()
    sys.exit(1)

banner = getBanner(infile)

server = [s] # needed for select
# server loop
while 1:
    try:
        # input, output and exception lists
        rlist, wlist, xlist = select.select(server, [], [])
        # this loop will handle ready sockets
        for sock in rlist:
            # accept new client
            if sock == s:
                conn, addr = s.accept()
                server.append(conn)
                ip = addr[0]
                port = addr[1]
                print '[%s] Connection received from %s:%d' % (date, ip, port)
                logActions('[%s] Connection received from %s:%d\n' % (date, ip, port))
            # get data from clients and send banner                      
            else:
                data = sock.recv(SIZE)
                if data:
                    sock.send(banner)
                    print 'Received from ' + str(ip) + ': ' + str(data)
                    logActions('Received from ' + str(ip) + ': ' + str(data))
                # if no data, client must have closed the connection
                else:         
                    sock.close()
                    server.remove(sock)
    except KeyboardInterrupt:
        print '\nShutting down...'
        s.close()
        sys.exit()

            
  

    
