import requests

def get_weather(location):
        api_key = "your_api_key"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(base_url)
        weather_data = response.json()
        if weather_data["cod"] != "404":
                main = weather_data["main"]
                temperature = main["temp"] - 273.15  # Convert from Kelvin to Celsius
                weather_desc = weather_data["weather"][0]["description"]
                return f"The temperature is {temperature:.2f}°C with {weather_desc}."
        else:
                return "City not found."