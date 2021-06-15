from utils import sendMail
import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from scrapper import *
from database import Products
import scrapper as sc
import pandas as pd
from datetime import datetime
import plotly.express as px


engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("Live Price Tracker")

st.image('logo.png')
st.markdown("---")
sidebar = st.sidebar

sidebar.header("Choose your option")
choices = ["Project Overview", "Search Product"]
selOpt = sidebar.selectbox("Choose What to do?", choices)

plot_area = st.empty()
data_area = st.empty()
data = None

def intro():
    # st.markdown("""#### Price Tracker is Python Data Science project for
    # tracking live prices of products on Ecommerce Websites.
    # """)

    st.markdown("""
        <h2>Price Tracker is Python Data Science project for 
    tracking live prices of products on Ecommerce Websites.</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)
    # col1.image("amb.jpg")

    st.markdown("""
        ### Features of Project
        1. Search product from various websites
        2. Set the Custom Tracking Time
        3. Get email when price dropped
        4. If you have an eCommerce store, you can use a dynamic pricing system to draw from the tracked data to update your prices automatically.
    """)


def searchProduct():
    product_name = st.text_input('enter the product name to show')
    amz_urls = st.text_input('Enter url for amazon')
    flip_urls = st.text_input('Enter url for flipkart')
    myn_urls = st.text_input('Enter url for Myntra')
    btn = st.button('Check tracker')
    if (amz_urls or flip_urls or myn_urls) and btn:
        df = []
        if amz_urls:
            details = sc.extract_amazon_data(amz_urls)
            df.append(details)

        if flip_urls:
            details = sc.extract_flipkart_data(flip_urls)
            df.append(details)

        if myn_urls:
            details = sc.extract_myntra_data(myn_urls)
            df.append(details)

        st.write(df)

        st.markdown(f"""
            <h2>Name : </h2>
            <h3>{df[0]['name']}</h3>
            <h2>Name : </h2>
            <h3>{df[0]['name']}</h3>
        """, unsafe_allow_html=True)

    st.subheader('Run Tracker ')
    time_gap = st.select_slider("How Much time difference between each tracking call", [
                                'No delay', '10 sec', '10 mins', '1 hour', '12 hours', '1 day', '3 days'])
    mail_addr = st.text_input("Enter Your Mail")
    btn2 = st.button('Run Tracker continously')


    if (amz_urls or flip_urls or myn_urls) and btn2 and mail_addr:
        if time_gap == '10 sec':
            wait = 10
        elif time_gap == '10 mins':
            wait = 60 * 10
        elif time_gap == '1 hour':
            wait = 60 * 60
        elif time_gap == '12 hours':
            wait = 60 * 60 * 12
        elif time_gap == '1 day':
            wait = 60 * 60 * 24
        elif time_gap == '3 day':
            wait = 60 * 60 * 24 * 3
        elif time_gap == 'No delay':
            wait = 0
        else:
            wait = 5

        dfs = []
        while True:
            if amz_urls:
                details = sc.extract_amazon_data(amz_urls)
                details['date'] = datetime.utcnow()
                product = Products(name=details['name'],
                                   price=details['price'],
                                   deal=details['deal'],
                                   url=details['url'],
                                   date=details['date'],
                                   website=details['website'])
                dfs.append(details)
                sess.add(product)
                sess.commit()
            if flip_urls:
                details = sc.extract_flipkart_data(flip_urls)
                details['date'] = datetime.utcnow()
                product = Products(name=details['name'],
                                   price=details['price'],
                                   deal=details['deal'],
                                   url=details['url'],
                                   date=details['date'],
                                   website=details['website'])
                dfs.append(details)
                sess.add(product)
                sess.commit()
            if myn_urls:
                details = sc.extract_myntra_data(myn_urls)
                details['date'] = datetime.utcnow()
                product = Products(name=details['name'],
                                   price=details['price'],
                                   deal=details['deal'],
                                   url=details['url'],
                                   date=details['date'],
                                   website=details['website'])
                dfs.append(details)
                sess.add(product)
                sess.commit()

            data = pd.DataFrame(dfs)
            data['date'] = pd.to_datetime(data['date'])
            fig = px.line(data_frame=data, x=data.index,
                          y=data['price'], line_group='name', color='website')
            plot_area.subheader('graphical output')
            plot_area.plotly_chart(fig)
            data_area.write(data)
            if mail_addr and data.shape[0] >= 12:
                lowest_value = 0
                amzdata = data[data.website == 'amazon']
                flipkartdata = data[data.website == 'flipkart']
                myntradata = data[data.website == 'myntra']
                if amz_urls:
                    if amzdata.iloc[-1]['price'] < amzdata.iloc[-2]['price']:
                        if sendMail(mail_addr, amz_urls, product_name, amzdata.iloc[-1]['price'], amzdata.iloc[-1]['website']):
                            st.success(
                                'Price fell at amazon , mail notification sent to {mail_addr}')
                if flip_urls:
                    if flipkartdata.iloc[-1]['price'] < flipkartdata.iloc[-2]['price']:
                        if sendMail(mail_addr, flip_urls, product_name, flipkartdata.iloc[-1]['price'], flipkartdata.iloc[-1]['website']):
                            st.success(
                                'Price fell at flipkart , mail notification sent to {mail_addr}')

                if myn_urls:
                    if myntradata.iloc[-1]['price'] < myntradata.iloc[-2]['price']:
                        if sendMail(mail_addr, myn_urls, product_name, myntradata.iloc[-1]['price'], myntradata.iloc[-1]['website']):
                            st.success(
                                'Price fell at myntra , mail notification sent to {mail_addr}')

            time.sleep(wait)

    op = st.sidebar.checkbox("show tracked product data manually")
    if op:
        try:
            df = pd.read_sql('products', engine)
            st.write(df)
        except Exception as e:
            st.error('No tracking data available')


if selOpt == choices[0]:
    intro()
elif selOpt == choices[1]:
    searchProduct()
