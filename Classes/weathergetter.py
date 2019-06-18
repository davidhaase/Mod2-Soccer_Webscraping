from Private import api_keys
import requests
import datetime
import re

class WeatherGetter:
    def __init__(self):
        self.ds_key = api_keys.api_key_darkskies
        self.g_key = api_keys.api_key_google_maps

    def is_rain(self, day, city, show=False):

        #####
        # LOCATION -- Use Google to find the lat and long, if the city is not findable with the API, use Berlin
        try:
            response = requests.get(
                f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={self.g_key}')
        except Exception as e:
            print(e)

        google_r = response.json()
        if google_r['status'] != 'OK':
            print(f'[LOCATION ERROR] Unable to find coordinates for {city}. Using Berlin')
            lat, long = 52.520008, 13.404954
            city_echo = 'Berlin'
        else:
            try:
                city_echo = google_r['results'][0]['address_components'][0]['long_name'] + ', ' + google_r['results'][0]['address_components'][2]['long_name']
                lat, long = google_r['results'][0]['geometry']['location']['lat'], google_r['results'][0]['geometry']['location']['lng']
            except:
                lat, long = 52.520008, 13.404954
                city_echo = 'Berlin'


        #####
        # DATE -- use Dark Skies to get the weather in that place on that day
        # Test for a valide date from app (M/D/YYYY)
        date_patt = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{4})')
        match = date_patt.search(day)
        if (match):
            m, d, y = match.group(1), match.group(2), match.group(3)
            t = datetime.datetime(int(y), int(m), int(d))
        else:
            print('[DATE ERROR] Invalid Date: M/D/YYYY')
            return None

        #####
        # EXCLUDE -- Minimize the return JSON from the API by using the exclude list because the API lets us
        exclude = 'currently,hourly'
        query = f'https://api.darksky.net/forecast/{self.ds_key}/{lat},{long},{t.strftime("%s")}?exclude={exclude}'

        try:
            r = requests.get(query)
        except Exception as e:
            print(e)
        #####
        # RAIN --- Determine if it rained that day:  is the string rain in summary or icon?
        # The Expected keys = dict_keys(['latitude', 'longitude', 'timezone', 'daily', 'flags', 'offset'])
        # We want to see if the string 'rain' exists in the ['data']['daily']['summary'], or 'data']['daily']['icon']
        if (r.status_code != 200) | ('daily' not in r.json().keys()):
            print(f'[WEATHER ERROR] Unable to determine weather at {city}, using Berlin')
            lat, long = 52.520008, 13.404954
            city_echo = 'Berlin'
            query = f'https://api.darksky.net/forecast/{self.ds_key}/{lat},{long},{t.strftime("%s")}?exclude={exclude}'

            try:
                r = requests.get(query)
            except Exception as e:
                print(e)

        summary, icon = r.json()['daily']['data'][0]['summary'], r.json()['daily']['data'][0]['icon']
        if (show):
            print(f'WEATHER SUMMARY for ({city_echo}): {summary}')
            print(f'WEATHER ICON for ({city_echo}): {icon}')
        return True if ('rain' in summary.lower()) or ('rain' in icon.lower()) else False 