#! /usr/bin/env python3

## Need to download pywapi-0.3.8 and run pip install -e path/to/pywapi-0.3.8 
import pywapi
import pprint

def load_data(zip_code):
    '''
    Load current weather data from weather.com
    '''
    weather_com_result = pywapi.get_weather_from_weather_com( zip_code, units='imperial' )

    return weather_com_result

# pprint.pprint(load_data('60610'))

def temp_description(temp):
    '''
    Return a description of the provided temperature
    '''
    temp_labels = {'blistering': (101, 150),
                    'hot': (91, 100),
                    'warm': (80, 90),
                    'mild': (71, 80),
                    'pleasant': (61, 70),
                    'crisp': (51, 60),
                    'cool': (41, 50),
                    'chilly': (31, 40),
                    'cold': (21, 30),
                    'frigid': (11, 20),
                    'harsh': (1, 10),
                    'bitter': (-9, 0),
                    'polar': (-100, -10)
                    }
    temp_description = ''
    for key, value in temp_labels.items():
        if value[0] < temp < value[1]:
            return key
        
    return 'interesting'


def extract_weather_data(weather_data, email_data):
    '''
    Take a JSON data object.

    Extract pertinent weather data.

    Return a dictionary for use in the email body template.
    '''
    temperature = weather_data['current_conditions']['temperature']
    temperature_units = weather_data['units']['temperature']
    
    general_description = weather_data['current_conditions']['text'].lower()
    feels_like = weather_data['current_conditions']['feels_like'].strip()
    barometer_reading = weather_data['current_conditions']['barometer']['reading']
    barometer_direction = weather_data['current_conditions']['barometer']['direction']
    pressure_units = weather_data['units']['pressure']

    if barometer_direction == 'steady':
        prediction = 'similar weather for a while'
    elif barometer_direction == 'rising':
        prediction = 'better conditions soon'
    else:
        prediction = 'worse weather shortly'

    if pressure_units == 'in':
        pressure_units = 'inches'

    high = weather_data['forecasts'][0]['high']
    low = weather_data['forecasts'][0]['low']
    sunrise = weather_data['forecasts'][0]['sunrise']
    sunset = weather_data['forecasts'][0]['sunset']
    night_precip = weather_data['forecasts'][0]['night']['chance_precip'] 
    day_precip = weather_data['forecasts'][0]['day']['chance_precip']

    city = weather_data['location']['name']
    humidity = weather_data['current_conditions']['humidity']
    wind_speed = weather_data['current_conditions']['wind']['speed']
    wind_direction = weather_data['current_conditions']['wind']['text']
        
    temperature_name = temp_description((int(high)+int(low))/2)
    
    moon_phase_name = weather_data['current_conditions']['moon_phase']['text']
    moon_phase_icon = weather_data['current_conditions']['moon_phase']['icon']

    visibility = weather_data['current_conditions']['visibility']
    current_text = weather_data['current_conditions']['text']
    latitude = weather_data['location']['lat']
    longitude = weather_data['location']['lon']

    data_dict = { 'temperature': temperature,
                  'temperature_units': temperature_units,
                  'general_description': general_description,
                  'feels_like': feels_like,
                  'barometer_reading': barometer_reading,
                  'barometer_direction': barometer_direction,
                  'prediction': prediction,
                  'pressure_units': pressure_units,
                  'high': high,
                  'low': low,
                  'sunrise': sunrise,
                  'sunset': sunset,
                  'night_precip': night_precip,
                  'day_precip': day_precip,
                  'city': city,
                  'temperature_name': temperature_name,
                  'humidity': humidity,
                  'wind_speed': wind_speed,
                  'wind_direction': wind_direction,
                  'moon_phase_name': moon_phase_name,
                  'moon_phase_icon': moon_phase_icon,
                  'visibility': visibility,
                  'current_text': current_text,
                  'latitude': latitude,
                  'longitude': longitude
                  }

    for key, value in data_dict.items():
        email_data[key] = value

    return email_data
