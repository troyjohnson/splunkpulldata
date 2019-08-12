# splunkpulldata
Get log files out of Splunk. Weird? Yes, but people (managers specifically) sometimes ask for weird.

This script has origins in this process:

   * https://www.hurricanelabs.com/splunk-tutorials/splunk-answers-how-to-export-massive-amounts-of-data-from-splunk

but I wanted to be able to feed it different command line arguments and include it in a loop.


From the help:
```
usage: splunk-pull-data.py [-h] [-d] [-v] [-b [SPLUNKBIN]] [-U [SPLUNKURI]]
                           [-s [SPLUNKSEARCH]] [-u [SPLUNKUSER]]
                           [-p [SPLUNKPASS]] [-f [FILEPREFIX]]
                           [-m [FILEMINUTES]] [--syear [SYEAR]]
                           [--smonth [SMONTH]] [--sday [SDAY]]
                           [--shour [SHOUR]] [--sminute [SMINUTE]]
                           [--ssecond [SSECOND]] [--eyear [EYEAR]]
                           [--emonth [EMONTH]] [--eday [EDAY]]
                           [--ehour [EHOUR]] [--eminute [EMINUTE]]
                           [--esecond [ESECOND]]

Do something with Splunk CLI.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Turn debugging on
  -v, --version         Display version
  -b [SPLUNKBIN], --splunkbin [SPLUNKBIN]
                        Splunk binary
  -U [SPLUNKURI], --splunkuri [SPLUNKURI]
                        Splunk URI
  -s [SPLUNKSEARCH], --splunksearch [SPLUNKSEARCH]
                        Splunk search
  -u [SPLUNKUSER], --splunkuser [SPLUNKUSER]
                        Splunk user
  -p [SPLUNKPASS], --splunkpass [SPLUNKPASS]
                        Splunk password
  -f [FILEPREFIX], --fileprefix [FILEPREFIX]
                        File name prefix
  -m [FILEMINUTES], --fileminutes [FILEMINUTES]
                        Minutes of time per log file
  --syear [SYEAR]       Start year
  --smonth [SMONTH]     Start month
  --sday [SDAY]         Start day
  --shour [SHOUR]       Start hour
  --sminute [SMINUTE]   Start minute
  --ssecond [SSECOND]   Start second
  --eyear [EYEAR]       End year
  --emonth [EMONTH]     End month
  --eday [EDAY]         End day
  --ehour [EHOUR]       End hour
  --eminute [EMINUTE]   End minute
  --esecond [ESECOND]   End second
```

