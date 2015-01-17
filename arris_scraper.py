#!/usr/bin/env python

# A library to scrape statistics from Arris CM820 and similar cable modems
# Inspired by https://gist.github.com/berg/2651577

import BeautifulSoup
import requests
import time

cm_time_format = '%a %Y-%m-%d %H:%M:%S'

def get_status(url):
    # Retrieve and process the page from the modem
    pagedata = requests.get(url).content
    timestamp = time.time() # Get the time immediately after retrieval
    bs = BeautifulSoup.BeautifulSoup(pagedata)

    downstream_table = bs.findAll('table')[1].findAll('tr')[1:]
    upstream_table = bs.findAll('table')[3].findAll('tr')[2:]
    status_table = bs.findAll('table')[5].findAll('tr')
    interface_table = bs.findAll('table')[7].findAll('tr')[1:]
    
    downstream_stats = []
    for row in downstream_table:
        cols = row.findAll('td')
        modem_channel = int(cols[0].string.strip()[-1])
        docsis_channel = int(cols[1].string.strip())
        frequency = float(cols[2].string.strip().split()[0])
        if cols[3].string.strip() == '----':
            channel_available = False
            power = None
            snr = None
            modulation = None
            octets = None
            corrected_errors = None
            uncorrectable_errors = None
        else:
            power = float(cols[3].string.strip().split()[0])
            snr = float(cols[4].string.strip().split()[0])
            modulation = cols[5].string.strip()
            octets = int(cols[6].string.strip())
            corrected_errors = int(cols[7].string.strip())
            uncorrectable_errors = int(cols[8].string.strip())
        channelstats = {'modem_channel': modem_channel,
                        'dcid': docsis_channel,
                        'frequency': frequency,
                        'power': power,
                        'snr': snr,
                        'modulation': modulation,
                        'octets': octets,
                        'corrected_errors': corrected_errors,
                        'uncorrectable_errors': uncorrectable_errors}
        downstream_stats.append(channelstats)
    
    upstream_stats = []
    for row in upstream_table:
        cols = row.findAll('td')
        modem_channel = int(cols[0].string.strip()[-1])
        docsis_channel = int(cols[1].string.strip())
        frequency = float(cols[2].string.strip().split()[0])
        power = float(cols[3].string.strip().split()[0])
        channel_type = cols[4].string.strip()
        symbol_rate = int(cols[5].string.strip().split()[0]) * 1000
        modulation = cols[6].string.strip()
        channelstats = {'modem_channel': modem_channel,
                        'ucid': docsis_channel,
                        'frequency': frequency,
                        'power': power,
                        'channel_type': channel_type,
                        'symbol_rate': symbol_rate,
                        'modulation': modulation}
        upstream_stats.append(channelstats)
    
    uptime_split = status_table[0].findAll('td')[1].string.strip().split(':')
    uptime_days = int(uptime_split[0].strip().split()[0])
    uptime_hours = int(uptime_split[1].strip().split()[0])
    uptime_minutes = int(uptime_split[2].strip().split()[0])
    uptime = ((((uptime_days * 24) + uptime_hours) * 60) + uptime_minutes) * 60
    cpe_split = status_table[1].findAll('td')[1].string.strip().split(',')
    cpelist = {}
    for entry in cpe_split:
        entrystripped = entry.strip()
        entrysplit = entrystripped.split('CPE')
        cpe_type = entrysplit[0]
        cpe_count = int(entrysplit[1].strip('()'))
        cpelist[cpe_type] = cpe_count
    cm_status = status_table[2].findAll('td')[1].string.strip()
    cm_time_string = status_table[3].findAll('td')[1].string.strip()
    cm_time = time.mktime(time.strptime(cm_time_string, cm_time_format))
    modem_status = {'uptime': uptime,
                    'cpe': cpelist,
                    'cm_status': cm_status,
                    'cm_time': cm_time}
    
    interfaces = []
    for row in interface_table:
        cols = row.findAll('td')
        interface_name = cols[0].string.strip()
        provisioning_state = cols[1].string.strip()
        interface_state = cols[2].string.strip()
        interface_speed = cols[3].string.strip()
        mac = cols[4].string.strip()
        interface_data = {'name': interface_name,
                          'provisioned': provisioning_state,
                          'state': interface_state,
                          'speed': interface_speed,
                          'mac': mac}
        interfaces.append(interface_data)
    
    status = {'timestamp': timestamp,
              'status': modem_status,
              'downstream': downstream_stats,
              'upstream': upstream_stats,
              'interfaces': interfaces}
    
    return status

def get_versions(url):
    raise NotImplementedError()

def get_eventlog(url):
    raise NotImplementedError()

def get_cmstate(url):
    raise NotImplementedError()

def get_productdetails(url):
    raise NotImplementedError()

def get_dhcpparams(url):
    raise NotImplementedError()

def get_qos(url):
    raise NotImplementedError()

def get_config(url):
    raise NotImplementedError()
