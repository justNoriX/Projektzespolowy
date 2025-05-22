from http.client import responses

import requests
from django.conf import settings

# ta klasa obsługuje komunikowanie się z API google oraz zwraca JSONa ze wszystkimi polami.

class GoogleWeatherService:
    BASE_URL = "https://weather.googleapis.com/v1/history/hours:lookup"

    @staticmethod
    def get_hourly_history(lat: float, lon: float, hours: int = 24) -> dict:
        params = {
            "key": settings.GOOGLE_WEATHER_API_KEY,
            "location.latitude": lat,
            "location.longitude": lon,
            "hours": hours,
        }

        response = requests.get(GoogleWeatherService.BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()


'''
Ta funckja wyodrębnia tylko niezbędne pola z całego JSON otrzymanego z powyższej klasy.
Poniżej przykładowy wygląd JSONa po formatowaniu. 
    [
        {
            'interval': {
                'startTime': '2025-05-22T16: 00: 00Z',
                'endTime': '2025-05-22T17: 00: 00Z'
            },
            'displayDateTime': {
                'year': 2025,
                'month': 5,
                'day': 22,
                'hours': 18,
                'minutes': 0,
                'seconds': 0,
                'nanos': 0,
                'utcOffset': '7200s'
            },
            'wind': 21
        },
        
        ... 
        kolejne godziny 
        ...
    ]
'''
def parse_weather_response(data):
    parsed = []
    for hour in data.get("historyHours", []):
        parsed.append({
            "interval": hour.get("interval"),
            "displayDateTime": hour.get("displayDateTime"),
            "wind": hour.get("wind").get("speed").get("value"),
        })
    return parsed
