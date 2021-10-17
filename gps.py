#!/usr/bin/env python3
import os
import re

import xml.etree.ElementTree as ET

files = [f.name for f in os.scandir('.') if f.is_file() and '.xml' in f.name.lower()]

files.sort()

base = 'https://www.google.de/maps/place/'
match = r'(\d+):(\d+):(\d+).(\d+)'
replace = r"\1°\2'\3.\4"

for f in files:
    root = ET.parse(f).getroot()

    attributes = {item.attrib.get('name'): item.attrib.get('value')
         for item in root.iter('{urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.00}Item')}

    latref = attributes.get('LatitudeRef')
    lat = attributes.get('Latitude')
    lonref = attributes.get('LongitudeRef')
    lon = attributes.get('Longitude')

    if attributes and latref and lat and lonref and lon:
        lat = re.sub(match, replace, lat)
        lon = re.sub(match, replace, lon)

        url = f'{base}{lat}%22{latref}+{lon}%22{lonref}'
    else:
        url = None

    print(f'{f}: {url}')
