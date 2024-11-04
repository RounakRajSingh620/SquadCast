import requests
import re
import json

base_url = "https://quest.squadcast.tech/api/RA2111003020213/weather"
weather_url = base_url + "/get?q={}"


def get_cities_and_condition():
    response = requests.get(base_url)

    if response.status_code == 200:
        city1 = re.search(r"City 1: ([A-Za-z ]+)", response.text)
        city2 = re.search(r"City 2: ([A-Za-z ]+)", response.text)
        condition = re.search(r"Condition: ([a-z]+)", response.text)

        if city1 and city2 and condition:
            return (
                city1.group(1).strip(),
                city2.group(1).strip(),
                condition.group(1).strip(),
            )
        else:
            raise ValueError("Expected data not found in the HTML response")
    else:
        raise Exception(
            f"Failed to retrieve cities and condition. Status code: {response.status_code}"
        )


def get_weather(city_name):
    response = requests.get(weather_url.format(city_name))
    if response.status_code == 200:
        weather_data = response.json()
        # Debugging: Print the weather data for inspection
        print(f"Weather data for {city_name}: {json.dumps(weather_data, indent=2)}")
        return weather_data
    else:
        raise Exception(
            f"Failed to retrieve weather data for {city_name}. Status code: {response.status_code}"
        )


def compare_cities(city1, city1_weather, city2, city2_weather, condition):
    if condition == "hot":
        return (
            city1
            if city1_weather["temperature"]["value"]
            > city2_weather["temperature"]["value"]
            else city2
        )
    elif condition == "cold":
        return (
            city1
            if city1_weather["temperature"]["value"]
            < city2_weather["temperature"]["value"]
            else city2
        )
    elif condition == "windy":
        return (
            city1
            if city1_weather["wind_speed"]["value"]
            > city2_weather["wind_speed"]["value"]
            else city2
        )
    elif condition == "rainy":
        return (
            city1
            if city1_weather["rain"]["value"] > city2_weather["rain"]["value"]
            else city2
        )
    elif condition == "sunny":
        return (
            city1
            if city1_weather.get("cloud_cover", {}).get("value", float("inf"))
            < city2_weather.get("cloud_cover", {}).get("value", float("inf"))
            else city2
        )
    elif condition == "cloudy":
        return (
            city1
            if city1_weather.get("cloud_cover", {}).get("value", float("-inf"))
            > city2_weather.get("cloud_cover", {}).get("value", float("-inf"))
            else city2
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")


def get_better_city():
    city1, city2, condition = get_cities_and_condition()

    city1_weather = get_weather(city1)
    city2_weather = get_weather(city2)

    better_city = compare_cities(city1, city1_weather, city2, city2_weather, condition)
    return better_city


if __name__ == "__main__":
    try:
        better_city = get_better_city()
        print(f"The better city based on the condition is: {better_city}")
    except Exception as e:
        print(f"Error: {e}")
