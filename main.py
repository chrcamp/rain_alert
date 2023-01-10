import requests
import os
from twilio.rest import Client
import auth

OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
API_KEY = os.environ.get("OWM_API_KEY")
twilio_sid = auth.twilio_sid
auth_token = os.environ.get("AUTH_TOKEN")

MY_LAT = auth.MY_LAT
MY_LONG = auth.MY_LONG
FROM_PH = auth.FROM_PH
TO_PH = auth.TO_PH

parameters = {
    'lat': MY_LAT,
    'lon': MY_LONG,
    'appid': API_KEY,
    'exclude': "current,minutely,daily,alerts"
}


response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data['hourly'][:12]

will_rain = False

for hour_data in weather_slice:
    condition_cd = hour_data['weather'][0]['id']
    if int(condition_cd) < 700:
        will_rain = True

if will_rain:
    client = Client(twilio_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella ☂️",
        from_=FROM_PH,
        to=TO_PH
    )
    print(message.sid)
    print(message.status)
