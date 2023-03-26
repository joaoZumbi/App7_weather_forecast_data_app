import pandas as pd
import streamlit as st
import plotly.express as px

# Load data from CSV file
data = pd.read_csv('happy.csv')


# Define Streamlit app
def app():
    st.title('Plotting Happiness Data')

    # Ask user to choose X and Y variables
    x_var = st.selectbox('Select X variable', options=list(data.columns)[1:])
    y_var = st.selectbox('Select Y variable', options=list(data.columns)[1:])

    # Plot data using Plotly Express
    fig = px.scatter(data, x=x_var, y=y_var, color='country')
    st.plotly_chart(fig)


# Run Streamlit app
app()
