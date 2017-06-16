#!/usr/bin/env python3

# Standard library
from xml.etree import ElementTree
from logging import getLogger
from datetime import datetime
from collections import OrderedDict

# 3rd party
from requests import get


logger = getLogger(__name__)

LATITUDE = 40.0
LONGITUDE = -83.0

def parseDatetime(text):
    # Remove the colon from the UTC offset to convert it into +HHMM / -HHMM
    text = text[:19] + text[19:].replace(':', '')    
    return datetime.strptime(text, '%Y-%m-%dT%H:%M:%S%z')

def processTimeLayout(timeLayout):
    childElements = list(timeLayout)
    if len(childElements) < 2:
        return None
    layoutKey = childElements[0]
    if layoutKey.tag != 'layout-key':
        return None
    if layoutKey.text != 'k-p12h-n14-1':
        return None
    return [parseDatetime(e.text) for e in childElements[1:]]
    
def getNationalWeatherServiceForecast():

    url = ['lat=%.4f' % LATITUDE]
    url.append('lon=%.4f' % LONGITUDE)
    url.append('unit=0')
    url.append('lg=english')
    url.append('FcstType=dwml')
    
    url = 'http://forecast.weather.gov/MapClick.php?' + '&'.join(url)
    logger.info('Downloading %s' %url)    

    response = get(url, timeout=5) 
    
    root = ElementTree.fromstring(response.text)
    
    forecast = root.findall(".//data[@type='forecast']")
    if forecast is None or len(forecast) != 1:
        logger.error('Unable to locate data element for forecast')
        return
    forecast = forecast[0]

    timePeriods = None
    timeLayouts = forecast.findall("./time-layout")
    for timeLayout in timeLayouts:
        timePeriods = processTimeLayout(timeLayout)
        if timePeriods is not None:
            break
    #print('timePeriods', timePeriods)
    
    values = forecast.findall(".//probability-of-precipitation/value")
    values = list(map(lambda x: x.text, values))
    for i, value in enumerate(values):
        if value is None:
            values[i] = 0
            continue
        values[i] = int(value)
    #print(values)
        
    if len(timePeriods) != len(values):
        raise Exception(
            "Number of time periods not equal to number of values")
        
    rainForecast = OrderedDict()
    for i, period in enumerate(timePeriods):
        rainForecast[period] = values[i]
    for period, percentRain in rainForecast.items():
        print("%s  %3d%%" % (period.strftime('%Y:%m:%d %H:%M'), percentRain))


           

    current = root.findall(".//data[@type='current observations']")
    print('current', current)


if __name__ == '__main__':       
    getNationalWeatherServiceForecast()


