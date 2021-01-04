#!/usr/bin/env python

'''
Author: Dustin Grady
Function: Alert user if VPN/ service provider modifies canary notice
Status: Working/ Tested
'''

import os
import sys
import requests
import subprocess
import configparser
import datetime

def get_datestr():
    now = datetime.datetime.now()
    month, day, year = datetime.datetime.strftime(now, '%B %d %Y').split()
    day = int(day)
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][day % 10 - 1]
    return '%s %d%s, %s' % (month, day, suffix, year)

'''Lookup sysarg and corresponding vpn_link/ vpn_canary in .ini file'''
def lookup(arg):
    arg = arg.strip('-').upper()
    if arg == 'HELP':
        print('To run: "python canary.py -<flag>\nValid flags:\n-nord\n-vpnsecure\n-slickvpn\n-ivpn\n-proxy.sh\n-proton\n-spyoff\n-azire\n-liquid\n-ace\n-cloudflare\n-vpnht\n-anonine')
        sys.exit(0)

    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(dir_path + '/info.ini')

    try:
        link = config[arg]['link']
        canary = [
    'As of <span>%s</span> we state the following:' % get_datestr(),
    'We have NOT received any National Security letters;',
    'We have NOT received any gag orders;',
    'We have NOT received any warrants from any government organization.',
    (u'We are 100% committed to our zero-logs policy – we never log the '
      'activities of our users to ensure their ultimate privacy and security.')]
        check_canary(link, canary)
    except KeyError:
        print('Error reading value. Did you provide a valid flag?')


        
'''Check appropriate website for statements'''
def check_canary(vpn_link, vpn_canary):
    res = requests.get(vpn_link)
    res_text = res.text
    platform = sys.platform
    for statement in vpn_canary:
        if statement not in res_text:
                title = "VPN Canary Alert!"
                body = "The following has been modified on your VPNs Canary page:\n" + statement
                subprocess.call("echo '"+body+"' |  mailx -s '"+title+"' root", shell=True)


try:
    lookup(sys.argv[1])
except IndexError:
    print("Please provide a valid argument, or run 'python canary.py -help' for more info")
