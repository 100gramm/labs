import pandas as pd
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO


class WeatherAnalyzer:

    def __init__(self, cities, api_key):
        self.cities = cities
        self.api_key = api_key
        self.data = pd.DataFrame()
    

    def fatch_city(self, city):
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'ошибка в получении данных для {city}:{e}')
            return None
    

    def parse_city(self, city, raw_data):
        if not raw_data:
            return []
        
        return {
            'city': city,
            'temperature': raw_data['main']['temp'],
            'feels_like': raw_data['main']['feels_like'],
            'humidity': raw_data['main']['humidity'],
            'pressure': raw_data['main']['pressure'],
            'weather': raw_data['weather'][0]['description'],
            'wind_speed': raw_data['wind']['speed']
        }
    

    def collect_all(self):
        all_data = []
        for city in self.cities:
            raw = self.fatch_city(city)
            parsed = self.parse_city(city, raw)
            if parsed:
                all_data.append(parsed)
        self.data = pd.DataFrame(all_data)
    

    def analyze(self):
        if self.data.empty:
            print('Нет данных для анализа')
            return
        else:
            print(self.data)


def get_astronauts():
    url = 'http://api.open-notify.org/astros.json'
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"Всего людей в космосе: {data['number']}")
        print('Список астронавтов')
        
        for person in data['people']:
            print(f"- {person['name']} ({person['craft']})")

    except requests.RequestException as e:
        print('Ошибка получения данных:', e)


class ImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Generator')

        self.label = tk.Label(root)
        self.label.pack()

        self.button = tk.Button(
            root, 
            text='Следующая картинка', 
            command=self.load_image)
        self.button.pack()

        self.load_image()
    
    def load_image(self):
        url = 'https://cataas.com/cat'
        response = requests.get(url, timeout=5)

        image = Image.open(BytesIO(response.content))
        image = image.resize((400, 400))

        self.photo = ImageTk.PhotoImage(image)
        self.label.config(image=self.photo)
        self.label.image = self.photo


if __name__=='__main__':
    cities = ['Saint Petersburg', 'San Francisco', 'Tokyo']
    api_key = 'a69a4a0ce7b4f263be7148056b2b41b2'

    weather = WeatherAnalyzer(cities, api_key)
    weather.collect_all()
    weather.analyze()

    get_astronauts()

    root = tk.Tk()
    app = ImageGenerator(root)
    root.mainloop()