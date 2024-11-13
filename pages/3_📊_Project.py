import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np
import nsepython
import nselib
import altair as alt
from scipy.optimize import minimize
import plotly.express as px
from nselib import capital_market
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta 
import seaborn as sb
st.set_page_config(page_title = "GET YOUR MARKOWITZ !!!",layout="wide",page_icon=":moneybag:")
st.title("GET YOUR MARKOWITZ !")
# st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
req_dt = (date.today() - relativedelta(years=5)).strftime('%d-%b-%Y')
start_date = (date.today() - relativedelta(years=5)).strftime('%Y-%m-%d')
end_date = (date.today() - relativedelta(days=1)).strftime('%Y-%m-%d')


### --- Fetching the Symbols from equity_list

symbol_df = capital_market.equity_list()
symbol_df.columns = symbol_df.columns.str.strip()
symbol_df['DATE OF LISTING'] = pd.to_datetime(symbol_df['DATE OF LISTING'])
symbol_df = symbol_df[(symbol_df['DATE OF LISTING'] < req_dt)]
symbol_list = st.sidebar.multiselect("Select Stocks:",options = list(symbol_df['SYMBOL'].unique()))
symbol_list = [x + '.NS' for x in symbol_list]
### --- Gathering price data from price_volume_data

if symbol_list:
    @st.cache_data
    def get_data_from_yfinance_data(symbol_list,start_date,end_date):
        price_data = pd.DataFrame()
        for symbol in symbol_list:
            data = yf.download(symbol, start=start_date, end = end_date )
            data['Symbol'] = symbol[0:-3]
            data = data.reset_index()
            price_data = pd.concat([price_data, data])
        price_data.columns = price_data.columns.str.strip()
        price_data['Symbol'] = price_data['Symbol'].replace("\s+", " ", regex=True).str.strip()
        price_data = price_data.drop_duplicates(subset=['Date', 'Symbol','Close'])
        price_data['returns'] = price_data.groupby('Symbol')['Close'].pct_change()
        price_data = price_data.dropna()
        price_data = price_data[['Date','Symbol','returns','Close']]
        stockreturns = price_data.pivot_table(index='Date', columns='Symbol', values='returns')
        return price_data, stockreturns
    price_data = get_data_from_yfinance_data(symbol_list,start_date,end_date)[0]
    stock_returns_data = get_data_from_yfinance_data(symbol_list,start_date,end_date)[1]     

    
    @st.cache_data
    def Calculate_portfolio_returns_and_sd(price_data,stock_returns_data):
        pivot = price_data.pivot_table(index=['Symbol'],
                           values=['returns'],
                           aggfunc='mean')

        req_df = pivot.reset_index()
        req_df['Annual_Returns'] = ((1 + (req_df['returns']))**252) - 1 
        data_of_stocks_AR = req_df[['Symbol', 'Annual_Returns']]
        r_s = req_df['Annual_Returns'].to_numpy()
        var_s = (stock_returns_data.cov()*252).to_numpy()
        
        portfoilo_return = []
        portfoilo_sd = []
        for i in range(9000):
            W = np.random.rand(len(symbol_list))
            W = W / sum(W)
            W_T = W.T
            r_p = np.dot(W,r_s)
            portfoilo_return.append(r_p)
            sd_p = (np.sqrt(np.dot(W,np.dot(var_s,W_T))))
            portfoilo_sd.append(sd_p)
        dict = {'Mean': portfoilo_return, 'Standard_Deviation':portfoilo_sd} 
        data_of_portfolio_mean_sd = pd.DataFrame(dict)
        return data_of_portfolio_mean_sd, var_s, r_s, data_of_stocks_AR

    df_return_sd_pf = Calculate_portfolio_returns_and_sd(price_data,stock_returns_data)[0]
    var_s = Calculate_portfolio_returns_and_sd(price_data,stock_returns_data)[1]
    r_s = Calculate_portfolio_returns_and_sd(price_data,stock_returns_data)[2]
    data_of_stocks_AR = Calculate_portfolio_returns_and_sd(price_data,stock_returns_data)[3]
    
    def get_heatmap_of_covariance():
        z = stock_returns_data.cov()*252
        fig = px.imshow(z, text_auto=True,aspect="auto")
        st.write("## Covariance Matrix")
        st.plotly_chart(fig, theme=None,use_container_width=True,height = 300)
        
    def get_scatter_plot():
        fig = px.scatter(df_return_sd_pf,x='Standard_Deviation', y='Mean', title='Efficient Frontier')
        st.plotly_chart(fig, theme="streamlit",use_container_width=True,height=300)

    def get_line_chart():
        temp_data = stock_returns_data.reset_index().sort_values('Date')
        temp_data = temp_data.set_index('Date')
        cumulative_returns_data = ((temp_data + 1).cumprod()) -1 
        st.write("## Cumulative Returns")
        st.line_chart(cumulative_returns_data)
            
    def objective_function(w):
        return (np.dot(w,np.dot(var_s,w.T))) * 0.5
    r_user = st.number_input(label='Enter Portfolio return you want(ex.0.20 i.e 20%)',step=1.,format="%.2f")
    st.write('Your rate of Return:',r_user*100,'%')

    def constraint_1(w):
        return r_user - np.dot(w,r_s)
    
    def constraint_2(w):
        return np.sum(w) - 1 
    
    def calculate_efficient_weights():
        k = len(symbol_list)
        w0 = []
        bounds = ()
        for i in range(k):
            w0.append(1/k)
            bounds += ((-2,2),)
        constraints = ({'type':'eq','fun':constraint_1},{'type':'eq','fun':constraint_2})
        w_opt = minimize(objective_function, w0, method='SLSQP', bounds=bounds, constraints=constraints)
        efficient_weights = pd.DataFrame([data_of_stocks_AR['Symbol'],w_opt.x ],index=['Stocks','Optimal_weights'])
        efficient_weights.columns = efficient_weights.iloc[0]
        return efficient_weights.T.reset_index(drop=True)
   
    # col_1, col_2 = st.columns(2)
    # with col_1:
    #     st.dataframe(calculate_efficient_weights(),use_container_width=True)
    # with col_2:
    #     get_scatter_plot()
    st.dataframe(calculate_efficient_weights(),use_container_width=True)
    get_scatter_plot()
    get_line_chart()
    get_heatmap_of_covariance()

        
        

        
    
        
   


