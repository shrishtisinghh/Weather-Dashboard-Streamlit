import requests
import datetime
import mysql.connector

API_KEY = "your_api_key"
CITIES = ["Mumbai", "Delhi", "Bangalore"]

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root@123",
    database="weather_db"
)

cursor = conn.cursor()

for city in CITIES:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    # 🛑 Handle API error
    if data.get("cod") != 200:
        print(f"Error fetching {city}: ", data)
        continue

    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
        "timestamp": datetime.datetime.now()
    }

    print("Fetched:", weather_data)

    query = """
    INSERT INTO weather_data 
    (city, temperature, feels_like, humidity, condition_desc, wind_speed, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        weather_data["city"],
        weather_data["temperature"],
        weather_data["feels_like"],
        weather_data["humidity"],
        weather_data["condition"],
        weather_data["wind_speed"],
        weather_data["timestamp"]
    )

    cursor.execute(query, values)

conn.commit()

print("✅ All data inserted!")

cursor.close()
conn.close()
