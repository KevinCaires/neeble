import logging

from settings.config import OW_API_CONFIG

import urllib.request
import json
import re2

def geocode(city = 'curitiba', state = 'parana', country = 'BR') -> str:
    """
    Converts city, state and country parameters into their coordinates
    """    
    if city == "" and state == "" and country == "":
        city = 'curitiba'
        state = 'parana'
        country = 'BR'
    ow_gc_url = OW_API_CONFIG['gc_url']
    ow_gc_url = re2.sub('<CITY>', city, ow_gc_url)
    ow_gc_url = re2.sub('<STATE>', state, ow_gc_url)
    ow_gc_url = re2.sub('<COUNTRY', country, ow_gc_url)
    ow_gc_url = re2.sub('<API_ID>', OW_API_CONFIG['api_id'], ow_gc_url)

    placedata = urllib.request.urlopen(ow_gc_url)
    placedata = placedata.read().decode()
    placedata = json.loads(str(placedata))

    return str(placedata[0]['lat']), str(placedata[0]['lon'])

def getweatherdata(lat, lon):
    """
    Gets weather data based on coordinates
    """
    ow_wh_url = OW_API_CONFIG['wh_url']
    ow_wh_url = re2.sub('<LAT>', lat, ow_wh_url)
    ow_wh_url = re2.sub('<LON>', lon, ow_wh_url)
    ow_wh_url = re2.sub('<API_ID>', OW_API_CONFIG['api_id'], ow_wh_url)

    weatherdata = urllib.request.urlopen(ow_wh_url)
    weatherdata = weatherdata.read().decode()
    weatherdata = json.loads(str(weatherdata))

    return weatherdata

def displayweather(wdata):
    """
    "Prettifies" the output for discord
    """
    try:
        wdata['weather'][0]['description']
        description = wdata['weather'][0]['description']
    except:
        description = "No data on description"
    try:
        wdata['main']['temp']
        temp = wdata['main']['temp']
        tempmsg = f"Temperature is {temp}ºC"
    except:
        tempmsg = "No data on temperature"
    try:
        wdata['main']['feels_like']
        feels_like = wdata['main']['feels_like']
        feels_likemsg = f"Feels like {feels_like}ºC"
    except:
        feels_likemsg = "No data on perceived temperature"
    try:
        wdata['main']['humidity']
        humidity = wdata['main']['humidity']
        humiditymsg = f"Humidity is {humidity}%"
    except:
        humiditymsg = "No data on humidity"
    try:
        wdata['wind']['speed']
        wind_speed = wdata['wind']['speed']
        wind_speedmsg = f"Wind speed is {wind_speed}m/s"
    except:
        wind_speedmsg = "No data on wind speed"
    try:
        wdata['wind']['gust']
        wind_gusts = wdata['wind']['gust']
        wind_gustsmsg = f"with gusts of {wind_gusts}m/s"
    except:
        wind_gustsmsg = "with no data on gusts"
    try:
        wdata['clouds']['all']
        cloud_coverage = wdata['clouds']['all']
        cloud_coveragemsg = f"Cloud coverage is {cloud_coverage}%"
    except:
        cloud_coveragemsg = "No data on cloud coverage"
    name = wdata['name']

    msg = f"""
    ```
    Weather for {name}:
    {description}, {tempmsg}. {feels_likemsg}. {humiditymsg}.
    {wind_speedmsg}, {wind_gustsmsg}. {cloud_coveragemsg}.
    ```"""

    return msg