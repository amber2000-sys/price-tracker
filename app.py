import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapper import *
from database import Product

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
        with st.spinner("Scrapping Data ..."):
            details = Scrap_flipkart(link)
            st.text(details)

        with st.spinner("Saving Data..."):
            try:
                product = Product(name=details['name'],
                                  link=details['link'],
                                  website=details['website'],
                                  time=details['time'],
                                  price=details['price'],
                                  lastprice=0)
                sess.add(product)
                sess.commit()
                st.success('Product Saved Successfully')
            except Exception as e:
                print(e)
                st.error('Something went Wrong')


if selOpt == choices[0]:
    intro()
elif selOpt == choices[1]:
    searchProduct()
