from deta import Deta
import streamlit as st

#initialize with a project key
deta = Deta(st.secrets['DETA_KEY'])

#this is how to connect a database
db = deta.Base('monthly_reports')

def insert_period(period,incomes,expenses,comment):
    """returns the report on a successful creation, otherwise raises an error."""
    return db.put({'key':period,'incomes':incomes,'expenses':expenses,'comment':comment})

def fetch_all_periods():
    """returns a dict of all periods"""
    res = db.fetch()
    return res.items

def get_period(period):
    """if not found, the function will return none"""
    return db.get(period)

 