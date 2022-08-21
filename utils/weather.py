import json
import logging
import urllib.request
from collections import namedtuple

from settings.config import OW_API_CONFIG


def geocode(city = 'curitiba', state = 'parana', country = 'BR') -> str:
    """
    Converts city, state and country parameters into their coordinates
    """    
    if city == "" and state == "" and country == "":
        city = 'curitiba'
        state = 'parana'
        country = 'BR'
    ow_gc_url = OW_API_CONFIG['gc_url']
    ow_gc_url = ow_gc_url.replace('<CITY>', city)
    ow_gc_url = ow_gc_url.replace('<STATE>', state)
    ow_gc_url = ow_gc_url.replace('<COUNTRY', country)
    ow_gc_url = ow_gc_url.replace('<API_ID>', OW_API_CONFIG['api_id'])

    placedata = urllib.request.urlopen(ow_gc_url)
    placedata = placedata.read().decode()
    placedata = json.loads(str(placedata))

    return str(placedata[0]['lat']), str(placedata[0]['lon'])

def getweatherdata(lat, lon):
    """
    Gets weather data based on coordinates
    """
    ow_wh_url = OW_API_CONFIG['wh_url']
    ow_wh_url = ow_wh_url.replace('<LAT>', lat)
    ow_wh_url = ow_wh_url.replace('<LON>', lon)
    ow_wh_url = ow_wh_url.replace('<API_ID>', OW_API_CONFIG['api_id'])

    weatherdata = urllib.request.urlopen(ow_wh_url)
    weatherdata = weatherdata.read().decode()
    weatherdata = json.loads(str(weatherdata))

    return weatherdata

def displayweather(wdata) -> object:
    """
    "Prettifies" the output for discord
    """
    try:
        description = wdata['weather'][0]['description']
    except:
        description = None

    try:
        tempmsg = wdata['main']['temp']
    except:
        tempmsg = None

    try:
        feels_likemsg = wdata['main']['feels_like']
    except:
        feels_likemsg = None

    try:
        humiditymsg = wdata['main']['humidity']
    except:
        humiditymsg = None

    try:
        wind_speedmsg = wdata['wind']['speed']
    except:
        wind_speedmsg = None

    try:
        wind_gustsmsg = wdata['wind']['gust']
    except:
        wind_gustsmsg =  None
    try:
        cloud_coveragemsg = wdata['clouds']['all']
    except:
        cloud_coveragemsg = None

    name = wdata['name']
    obj = namedtuple('Weather', [
        'name',
        'description',
        'temp',
        'feels_like',
        'humidity',
        'wind_speed',
        'wind_gusts',
        'cloud_coverage',
    ])
    weather = obj(*(
        name,
        description,
        tempmsg,
        feels_likemsg,
        humiditymsg,
        wind_speedmsg,
        wind_gustsmsg,
        cloud_coveragemsg
    ))

    return weather
