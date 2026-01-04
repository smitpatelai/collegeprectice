import requests

def get_weather(city_name, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        print(f"\n🌤️ Weather in {data['name']}, {data['sys']['country']}:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Feels like: {data['main']['feels_like']}°C")
        print(f"Weather: {data['weather'][0]['description'].title()}")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
    else:
        print("\n❌ Error:", data.get("message", "Unable to fetch weather."))

def main():
    print("=== 🌦️ Simple Weather App ===")
    api_key = input("Enter your OpenWeatherMap API key: ").strip()
    while True:
        city = input("\nEnter city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("Goodbye! 👋")
            break
        get_weather(city, api_key)

if __name__ == "__main__":
    main()
