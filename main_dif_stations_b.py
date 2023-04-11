import streamlit as st
import plotly.express as px
from backend import get_data

st.title("Weather Forecast for the next days")
num_cities = st.slider("Number of Cities", min_value=1, max_value=5)

places = []
for i in range(num_cities):
    place = st.text_input(f"City {i + 1}")
    if place:
        places.append(place)

if len(places) == 0:
    st.write("Please input at least one city.")
else:
    forecast_days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
    option = st.selectbox("Select data to view", ("Temperature", "Sky"))

    for place in places:
        st.subheader(f"{option} for the next {forecast_days} days in {place}")
        try:
            filtered_data = get_data(place, forecast_days)

            if option == "Temperature":
                temperatures = [dct["main"]["temp"] for dct in filtered_data]
                dates = [dct["dt_txt"] for dct in filtered_data]
                # Create a temperature plot
                fig = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperatures (ºC)"})
                st.plotly_chart(fig)

            if option == "Sky":
                images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                          "Rain": "images/rain.png", "Snow": "images/snow.png"}
                sky_conditions = [dct["weather"][0]["main"] for dct in filtered_data]
                image_paths = [images[condition] for condition in sky_conditions]
                st.image(image_paths, width=115)

        except KeyError:
            st.write(f"No weather data available for {place}.")
