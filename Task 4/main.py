# Import necessary libraries
import tkinter as tk
from tkinter import messagebox
import requests
import json
from PIL import Image, ImageTk
import io
import geocoder

# Define the WeatherApp class
class WeatherApp:
        # Initialize the WeatherApp class
        def __init__(self, root):
                self.root = root
                self.root.title("Weather App")
                self.root.geometry("400x400")

                self.api_key = '34cb16035c2fd23d09db615d20e9898b'  # Replace with your OpenWeatherMap API key

                self.setup_ui()

        # Set up the GUI components
        def setup_ui(self):
                # Location entry
                self.location_entry = tk.Entry(self.root, width=30)
                self.location_entry.pack(pady=10)

                # Fetch Weather button
                self.fetch_weather_button = tk.Button(self.root, text="Fetch Weather", command=self.fetch_weather)
                self.fetch_weather_button.pack(pady=10)

                # Display area for weather information
                self.weather_display = tk.Label(self.root, text="", justify="left")
                self.weather_display.pack(pady=20)

                # Automatic location detection button
                self.auto_location_button = tk.Button(self.root, text="Use Current Location", command=self.use_current_location)
                self.auto_location_button.pack(pady=10)

        # Fetch weather data for the location entered by the user.
        def fetch_weather(self):
                location = self.location_entry.get()
                if location:
                        self.get_weather_data(location)
                else:
                        messagebox.showerror("Error", "Please enter a location")

        # Use geolocation to fetch weather data for the user's current location.
        def use_current_location(self):
                g = geocoder.ip('me')
                if g.ok:
                        self.get_weather_data(g.city)
                else:
                        messagebox.showerror("Error", "Unable to detect location")

        # Fetch weather data from OpenWeatherMap API for the specified location.
        def get_weather_data(self, location):
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                complete_url = base_url + "q=" + location + "&appid=" + self.api_key + "&units=metric"

                response = requests.get(complete_url)
                if response.status_code == 200:
                        data = response.json()
                        self.display_weather(data)
                else:
                        messagebox.showerror("Error", "City not found")

        # Display weather information fetched from OpenWeatherMap API.
        def display_weather(self, data):
                try:
                        # Extract relevant weather information from API response
                        city = data['name']
                        country = data['sys']['country']
                        weather_desc = data['weather'][0]['description']
                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        humidity = data['main']['humidity']
                        wind_speed = data['wind']['speed']

                        # Fetch weather icon
                        icon_code = data['weather'][0]['icon']
                        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
                        icon_response = requests.get(icon_url)
                        icon_image = Image.open(io.BytesIO(icon_response.content))
                        icon_photo = ImageTk.PhotoImage(icon_image)

                        # Format weather information for display
                        weather_info = (f"City: {city}, {country}\n"
                                        f"Weather: {weather_desc}\n"
                                        f"Temperature: {temp}°C\n"
                                        f"Feels like: {feels_like}°C\n"
                                        f"Humidity: {humidity}%\n"
                                        f"Wind Speed: {wind_speed} m/s\n")

                        # Update GUI with weather information and icon
                        self.weather_display.config(text=weather_info, image=icon_photo, compound='top')
                        self.weather_display.image = icon_photo
                except KeyError:
                        messagebox.showerror("Error", "Invalid response from API")

if __name__ == "__main__":
        root = tk.Tk()
        app = WeatherApp(root)
        root.mainloop()