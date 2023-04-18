import streamlit as st
import plotly.express as px
from backend import get_data
import pandas as pd

st.title("Weather Forecast for the next days")
city_string = st.text_input("Cities (comma-separated):")
forecast_days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")

cities = [city.strip() for city in city_string.split(",")] if city_string else []

if len(cities) > 0:
    # get the temperature data for each city
    data = []
    for city in cities:
        try:
            filtered_data = get_data(city, forecast_days)
            temperatures = [dct["main"]["temp"] for dct in filtered_data]
            dates = [dct["dt_txt"] for dct in filtered_data]
            data.append({"City": city, "Temperature": temperatures, "Date": dates})
        except KeyError:
            st.write(f"No data available for {city}")

    # combine the data for all cities into a single dataframe
    df = pd.DataFrame()
    for d in data:
        df = pd.concat([df, pd.DataFrame({"City": [d["City"]] * len(d["Temperature"]), "Temperature": d["Temperature"], "Date": d["Date"]})])

    # create a temperature plot for all cities
    figure = px.line(df, x="Date", y="Temperature", color="City", labels={"x": "Date", "y": "Temperatures (ºC)"})
    st.plotly_chart(figure)
else:
    st.write("Please enter at least one city.")
