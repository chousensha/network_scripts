#!/usr/bin/python

import sys
import dns.resolver
import time


def dnsLookup(target, record):
    query = dns.resolver.query(target, record)
    for result in query:
        if record == "A":
            print "Address for %s is " %target + result.address
        elif record == "AAAA":
            print "IPv6 address for %s is " %target + result.address
        elif record == "MX":
             print "Mail server at %s " %result.exchange + "preference: " + \
                   str(result.preference)
        elif record == "NS":
            print "DNS server for %s domain: " %target + result.to_text()         
        else:
            print "No valid record specified"
    return "Query completed at %s" %str(time.asctime(time.localtime(time.time()))) 
     

if len(sys.argv) == 3:
    target = sys.argv[1]
    record = sys.argv[2]
    print dnsLookup(target, record)
else:
    print 'Usage: ' + sys.argv[0] + " '" + 'target_domain' + "' " + 'record_type'
    print 'Valid record types: A, AAAA, MX, NS'
