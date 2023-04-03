import requests

APIkey = "648ddc0322fabc7ef11a2732cfe14cb9"


def get_data(place, forecast_days=None, kind=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={APIkey}&units=metric"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    nr_values = 8 * forecast_days
    filtered_data = filtered_data[:nr_values]
    if kind == "Temperature":
        # filtered_data = [dict["main"]["temp"] for dict in filtered_data ]
        filtered_data = [{"temp": dct["main"]["temp"], "humidity": dct["main"]["humidity"]} for dct in filtered_data]
    if kind == "Sky":
        filtered_data = [dct["weather"][0]["main"] for dct in filtered_data]
    return data


if __name__ == "__main__":
    a = get_data(place="Porto", forecast_days=2, kind="Sky")
    print(a)
