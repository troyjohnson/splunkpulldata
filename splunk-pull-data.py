#! /usr/bin/python

import datetime
import os
import subprocess
import re
import getpass
import sys
import argparse

# version
__version_info__ = ('1', '0', '3')
__version__ = '.'.join(__version_info__)

# argument parsing
parser = argparse.ArgumentParser(description='Do something with Splunk CLI.')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='Turn debugging on')
parser.add_argument('-v', '--version', action='version', version="%(prog)s "+__version__, help='Display version')
parser.add_argument('-b', '--splunkbin', type=str, nargs='?', const='/opt/splunk/bin/splunk', default='/opt/splunk/bin/splunk', help='Splunk binary')
parser.add_argument('-U', '--splunkuri', type=str, nargs='?', const='https://localhost:8089', default='https://localhost:8089', help='Splunk URI')
parser.add_argument('-s', '--splunksearch', type=str, nargs='?', const='*', default='*', help='Splunk search')
parser.add_argument('-u', '--splunkuser', type=str, nargs='?', const='admin', default='admin', help='Splunk user')
parser.add_argument('-p', '--splunkpass', type=str, nargs='?', const='changeme', default='NOTSET', help='Splunk password')
parser.add_argument('-f', '--fileprefix', type=str, nargs='?', const='splunk', default='splunk', help='File name prefix')
parser.add_argument('-m', '--fileminutes', type=int, nargs='?', const='1440', default='1440', help='Minutes of time per log file')
parser.add_argument('--syear', type=int, nargs='?', const=2018, default=2018, help='Start year')
parser.add_argument('--smonth', type=int, nargs='?', const=1, default=1, help='Start month')
parser.add_argument('--sday', type=int, nargs='?', const=1, default=1, help='Start day')
parser.add_argument('--shour', type=int, nargs='?', const=12, default=12, help='Start hour')
parser.add_argument('--sminute', type=int, nargs='?', const=00, default=00, help='Start minute')
parser.add_argument('--ssecond', type=int, nargs='?', const=00, default=00, help='Start second')
parser.add_argument('--eyear', type=int, nargs='?', const=2018, default=2018, help='End year')
parser.add_argument('--emonth', type=int, nargs='?', const=1, default=1, help='End month')
parser.add_argument('--eday', type=int, nargs='?', const=1, default=1, help='End day')
parser.add_argument('--ehour', type=int, nargs='?', const=12, default=12, help='End hour')
parser.add_argument('--eminute', type=int, nargs='?', const=00, default=00, help='End minute')
parser.add_argument('--esecond', type=int, nargs='?', const=00, default=00, help='End second')

args = parser.parse_args()

if args.debug:
        print args

# STUFF THAT NEEDS TO BE DONE BEFORE RUNNING THIS SCRIPT#
splunk_home = args.splunkbin
search_string = args.splunksearch

# Replace this with a username for your environment. Python will prompt for a password
user = args.splunkuser
password = args.splunkpass
if args.splunkpass == 'NOTSET':
	p = getpass.getpass()
	password = p

### Define Stopping Time
t_start = datetime.time(args.ehour, args.eminute, args.esecond)
d_start = datetime.date(args.eyear, args.emonth, args.eday)

### Define the Starting Time
t_stop = datetime.time(args.shour, args.sminute, args.ssecond)
d_stop = datetime.date(args.syear, args.smonth, args.sday)

dt_stop = datetime.datetime.combine(d_stop, t_stop)
dt_start = datetime.datetime.combine(d_start, t_start)
format = "%m/%d/%Y:%T"

while True:
	#if the Start Time and Stop time are the same, end the loop
    if dt_start <= dt_stop:
        print "This is the end"
        print dt_start.strftime(format) + " it the same as " + dt_stop.strftime(format)
        break
    else:        
        #Find the "earliest" time for the search
        dt_start_early = dt_start - datetime.timedelta(minutes=args.fileminutes)
        
        #Convert times to a readable format
        dt_start_early_string = dt_start_early.strftime(format)
        dt_start_string = dt_start.strftime(format)
	if args.debug:
        	print "dt_start_early_string: " + dt_start_early_string
        	print "dt_start_string: " + dt_start_string
        
        #ensure the file exists that we'll export to. 
	if args.fileminutes >= 1440:
		outfilename = args.fileprefix + '-' + str(dt_start.strftime("%Y%m%d")) + ".log"
	else:
		outfilename = args.fileprefix + '-' + str(dt_start.strftime("%Y%m%d%H%M%S")) + ".log"
	file = open(outfilename, "w+") 
        file.close()
        
	# build search command
	search_time = " earliest=" + str(dt_start_early_string) + " latest=" + str(dt_start_string)
	search_options = "-output rawdata -maxout 0 -max_time 0 -auth " + user + ":" + password + " -uri " + args.splunkuri
	splunk_search_string = "search \"" + search_string + " " + search_time + "\" " + search_options
	splunk_command = splunk_home + " " + splunk_search_string + " > " + outfilename
	if args.debug:
		print splunk_command

        #spawn a process to run a search
        p = subprocess.Popen([splunk_command], stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        
        #Set the next start time to the earliest time of our last search
        dt_start = dt_start_early
        
