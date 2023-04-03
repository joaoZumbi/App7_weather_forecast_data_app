import streamlit as st
import plotly.express as px
from backend import get_data

st.title("Weather Forecast for the next days")
place = st.text_input("Place:")
forecast_days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {forecast_days} days in {place}")

if place:
    # get the temperature/sky data
    try:
        filtered_data = get_data(place, forecast_days)

        if option == "Temperature":
            ## temperatures_humidity = [{"temp": dct["main"]["temp"], "humidity": dct["main"]["humidity"]} for dct in filtered_data]
            temperatures = [dct["main"]["temp"] for dct in filtered_data]
            dates = [dct["dt_txt"] for dct in filtered_data]
            # Create a temperature plot
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperatures (ºC)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dct["weather"][0]["main"] for dct in filtered_data]
            image_paths = [images[condition] for condition in sky_conditions]
            print(sky_conditions)
            st.image(image_paths, width=115)
    except KeyError:
        st.write("That place doesnt exist")
