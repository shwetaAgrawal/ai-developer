import requests  
from semantic_kernel.functions import kernel_function
from typing import TypedDict, Annotated, Optional


class WeatherPlugin:  
    @kernel_function(description="Returns the weather for a location specified by latitude and longitude.")
    async def get_current_weather(self, 
                          latitude:Annotated[float, "The latitude of the location"], 
                          longitude:Annotated[float, "The longitude of the location"]):  
        print(f"weather request location: {latitude}, {longitude}")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,weather_code,cloud_cover,wind_speed_10m,uv_index&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&forecast_days=1"  
        response = requests.get(url)  
        print(f"weather response {response.json()}")
        return response.json() 

    @kernel_function(description="Returns the weather forecast for a location specified by latitude and longitude upto 16 days in future.")
    async def get_weather_forecast(self,
                                   latitude:Annotated[float, "The latitude of the location"],
                                   longitude:Annotated[float, "The longitude of the location"], 
                                   days:Annotated[int, "The number of days to forecast"]):
        print(f"weather forecast request location: {latitude}, {longitude}, {days}")
        if days > 16:
            print("Cannot forecast more than 16 days in future")
            return ValueError("Cannot forecast more than 16 days in future")

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,weather_code,cloud_cover,wind_speed_10m,uv_index&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&forecast_days={days}"
        response = requests.get(url)  
        print(f"weather response {response.json()}")
        return response.json()    