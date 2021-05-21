import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapper import *

engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("Live Price Tracker")

st.image('logo.png')
st.header("Write description of your project....")
st.markdown("---")
sidebar = st.sidebar

sidebar.header("Choose your option")
choices = ["Project Overview", "Search Product"]
selOpt = sidebar.selectbox("Choose What to do?", choices)


def intro():
    pass


def searchProduct():
    link = st.text_input('Enter Your Product URL')
    site = st.radio('Select the Website', ['Flipkart', 'Amazon', 'Myntra'])
    btn = st.button('Submit')

    if btn and link and site == 'Flipkart':
        details = Scrap_flipkart(link)
        st.text(details)


if selOpt == choices[0]:
    intro()
elif selOpt == choices[1]:
    searchProduct()
