import streamlit as st
import plotly.graph_objects as go
import datetime as dt
import calendar
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import pandas as pd
import database as db

# ----------- SETTINGS -----------

incomes = ['Salary','Blog','Other Income']
expenses = ['Rent','Utilities','Groceries','Car','Other Expenses','Saving']
currency = 'USD'
page_title = 'Income and Expense Tracker'
page_icon_ = ':money_with_wings:'
layout = 'centered'

st.set_page_config(page_title=page_title,page_icon=page_icon_,layout=layout)
st.title(page_title+" "+page_icon_)

# ----------- DROP DOWN VALUES FOR SELECTING THE PERIOD -------------

years = [dt.date.today().year,dt.date.today().year+1]
months = list(calendar.month_name[1:])


#------DATABASE INTERFACE-----------
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item['key'] for item in items]
    return periods

#------------- HIDE STREAMLIT STYLE ----------------------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)
#------------- NAVIGATION MENU -----------------
selected = option_menu(
    menu_title = None,
    options =['Data Entry','Data Visualization'],
    icons = ['pencil-fill','bar-chart-fill'],
    orientation = 'horizontal'
)

#------------- INPUT AND SAVE PERIODS ----------
if selected=='Data Entry':
    st.header(f'Data Entry in {currency}')
    with st.form('entry_form',clear_on_submit = True):
        col1,col2 = st.columns(2)
        col1.selectbox('Select Month:',months,key='month')
        col2.selectbox('Select Year:',years,key='year')

        '---'
        with st.expander('Income'):
            for income in incomes:
                st.number_input(f'{income}:',min_value=0,format='%i',step=10,key=income)
        
        with st.expander('Expenses'):
            for expense in expenses:
                st.number_input(f'{expense}:',min_value=0,format='%i',step=10,key=expense)
        
        with st.expander('Comment'):
            comment = st.text_area('',placeholder='Enter a comment here ...')

        submitted = st.form_submit_button('Save Data')
        if submitted:
            period = str(st.session_state['year'])+"_"+str(st.session_state['month'])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            db.insert_period(period,incomes,expenses,comment)
            st.success("Data Saved")

if selected=='Data Visualization':
    st.header('Data Visualization')
    with st.form('saved_periods'):
        period = st.selectbox('select period:',get_all_periods())
        submitted = st.form_submit_button('Plot Period')
        if submitted:
            period_data = db.get_period(period)
            comment = period_data.get('comment')
            expenses = period_data.get('expenses')
            incomes = period_data.get('incomes')
            
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income-total_expense

            st.header('Data Visualization')
            col1,col2,col3 = st.columns(3)
            col1.metric('Total Income',value=f'{total_income}',delta='USD')
            col2.metric('Total Expense',value=f'{total_expense}',delta='USD')
            col3.metric('Remaining Budget',value=f'{remaining_budget}') 

            names = list(incomes.keys())
            values = list(incomes.values())
            plt.bar(range(len(incomes)),values,tick_label=names)
            st.pyplot(plt.gcf())