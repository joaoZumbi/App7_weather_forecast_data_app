import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
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

    # Create subplots with one row and multiple columns
    fig = make_subplots(rows=1, cols=len(places), shared_yaxes=True,
                        subplot_titles=[f"{forecast_days} days in {place}" for place in places])

    for i, place in enumerate(places, 1):
        try:
            filtered_data = get_data(place, forecast_days)

            if option == "Temperature":
                temperatures = [dct["main"]["temp"] for dct in filtered_data]
                dates = [dct["dt_txt"] for dct in filtered_data]
                # Add a temperature trace to the corresponding subplot
                fig.add_trace(go.Scatter(x=dates, y=temperatures, mode='lines', name=place), row=1, col=i)

            if option == "Sky":
                images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                          "Rain": "images/rain.png", "Snow": "images/snow.png"}
                sky_conditions = [dct["weather"][0]["main"] for dct in filtered_data]
                image_paths = [images[condition] for condition in sky_conditions]
                # Add an image trace to the corresponding subplot
                fig.add_layout_image(
                    dict(source=image_paths, xref="x", yref="y",
                         x=dates[0], y=temperatures[0],
                         sizex=dates[-1] - dates[0], sizey=max(temperatures) - min(temperatures),
                         sizing="stretch")
                )
                fig.update_xaxes(range=[dates[0], dates[-1]], row=1, col=i)
                fig.update_yaxes(range=[min(temperatures), max(temperatures)], row=1, col=i)

        except KeyError:
            st.write(f"No weather data available for {place}.")

    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig)
