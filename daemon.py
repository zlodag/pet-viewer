#!/usr/bin/env python3

import requests
import json
import time
import os
from xml.etree import ElementTree
from datetime import datetime, timezone

def updateLoop(firebase_app_name, api, lastTimestamp):
    r = requests.get(api)
    tracker = ElementTree.fromstring(r.content)[0]

    lat = tracker.findtext('data.Lat')
    lng = tracker.findtext('data.Lng')
    timestring = tracker.findtext('data.GPSTime')
    time = datetime.strptime(timestring, '%Y/%m/%d %H:%M:%S').replace(tzinfo=timezone.utc)
    timestamp = int(time.timestamp())
    if timestamp <= lastTimestamp:
        print('Skipping...')
    else:
        payload = json.dumps({
            'lat': float(lat[1:]) * (1 if lat[0]=='N' else -1),
            'lng': float(lng[1:]) * (1 if lng[0]=='E' else -1)
        }, separators=(',', ':'))
        r = requests.put('https://%s.firebaseio.com/%d.json' % (firebase_app_name, timestamp), data=payload)
        print('%s using timestamp: %s' % ('Updated' if r.status_code == requests.codes.ok else 'Failed to update', time))
    return timestamp

if __name__ == '__main__':
    config = json.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')))
    lastTimestamp = 0
    while True:
        lastTimestamp = updateLoop(config['firebase_app_name'], config['api'], lastTimestamp)
        time.sleep(config['check_interval_seconds'])
