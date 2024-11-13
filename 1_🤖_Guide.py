import pandas as pd
import streamlit as st
st.set_page_config(page_title = "Guide",layout="wide")
st.sidebar.success("Select a demo above.")
st.write("# Welcome to Markowitz Dashboard! 👋")


st.write(
    """
    ### 📍Objectives
    - Constructs Efficient Portfolio of multiple selected Assets using Markowitz Model
    - Compare the performance of Selected Stocks
    ### 📍Uses and Workings of Dashboard
    - Go to 📊Project
    - Select the stocks from the sidebar
    - get_data_from_yfinance_data(...) will run to gether the data for selected stocks
    - Enter the return you want from your generated portfolio
    - Dataframe will resulted with optimal weights according to your selected stocks
    ### 📍Notes and Charts
    - Short selling is allowed,so User might get Negative Weights.
    - Mean-Standard_Deviation Scatter plot shows 9000 randomly generated Portfolio's Mean and SD.
    - Line chart shows time series of returns.
    - Covariance Matrix shows risk of stocks individually and correlation with others.
"""
)