import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import pickle
from PIL import Image

#connecting the app to the database

conn=sqlite3.connect('Data.db')
c=conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT, password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO usertable(username,password) VALUES (?,?)',(username,password))
    conn.commit()
def login_user(username,password):
    c.execute('SELECT * FROM usertable WHERE username=? AND password=?',(username,password))
    data=c.fetchall()
    return data

st.set_page_config(layout="wide")

#Find price app function
def find_price():

    image=Image.open('sedan-sport-car-blank-price-260nw-391583524.jpg')
    st.image(image,width=500)

    st.header('Car Resale Value Calculator')

    st.write("""
    This app Predicts the resale price of a car
    """)

    expander_bar = st.expander("About")
    expander_bar.markdown("""
    * **Python libraries:** pandas, PIL, streamlit, numpy, scikit-learn, random_forest_regressor.
    * **Data source:** [CarDekho.com on Kaggle](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho/version/3).
    * **Credit:** Made by Shivam Pandey
    """)

    st.sidebar.header('User Input Features')

    def user_input_features():
        present_price=st.sidebar.slider('Present Price',0.32,92.6,10.5)
        kms_driven=st.sidebar.slider('Kilometers Driven',500,500000,100000)
        Owner=st.sidebar.slider('Car type 0:1st Hand,1:2nd Hand,2:3rd Hand ',0,2,1)
        Years_old=st.sidebar.slider('Years Old',2,17,8)
        Fuel_type=st.sidebar.selectbox('Fuel Type',('Petrol','Diesel','CNG'))
        Seller_type=st.sidebar.selectbox('Seller Type',('Individual','Dealer'))
        transmission_type=st.sidebar.selectbox('Transmission Type',('Manual','Automatic'))
        data={'Present_Price':present_price,
            'Kms_Driven':kms_driven, 
            'Owner':Owner,
            'Years_old':Years_old,
            'Fuel_Type':Fuel_type,
            'Seller_type':Seller_type,
            'Transmission':transmission_type 
            }
        df=pd.DataFrame(data,index=[0])    
        return df
    input_df=user_input_features()
    cars=pd.read_csv('car data.csv')
    cars.drop(['Car_Name','Year'],axis=1,inplace=True)
    cars=cars.iloc[:,1:]
    df=pd.concat([input_df,cars],axis=0)

    final_df=pd.get_dummies(df,drop_first=True)
    final_df=final_df[:1]

    st.subheader('User Input features')
    st.write(input_df)

    load_reg=pickle.load(open('random_forest_regressor.pkl','rb'))
    prediction=load_reg.predict(final_df)

    st.subheader('The price at which you can sell your car:')
    st.subheader(str(round(prediction[0],2))+' lakhs')
    


#Main app 

st.title('Car Price Predictor')

image=Image.open('sedan-sport-car-blank-price-260nw-391583524.jpg')
st.image(image,width=500)

menu=['Home','Login Page','Sign up']
choice=st.sidebar.selectbox("Menu",menu)

if(choice=="Home"):
    st.markdown("""
    * Welcome to Car Resale Value Calculator App
    * To access the Calculator please Login using the login option in sidebar(if you don't have an account please sign up)
    * If you dont know how to run the app access the **How to run section** 
    """)

elif (choice=="Login Page"):
    username=st.sidebar.text_input("Username")
    password=st.sidebar.text_input("password",type='password')

    if(st.sidebar.checkbox("login")):

        create_table()
        result=login_user(username,password)
        if(result):
            st.success("Logged in as {}".format(username))

            task=st.selectbox("Task",["App info","Find Price","How to use the calculator","Contacts"])

            if(task=="App info"):

                st.header('Car Resale Value Calculator')

                st.write("""
                This app Predicts the resale price of a car
                """)

                expander_bar = st.expander("About")
                expander_bar.markdown("""
                * **Python libraries:** pandas, PIL, streamlit, numpy, scikit-learn, random_forest_regressor.
                * **Data source:** [CarDekho.com on Kaggle](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho/version/3).
                * **Credit:** Made by Shivam Pandey
                """)

            elif(task=="Find Price"):

                find_price()

            elif(task=="Contacts"):
                st.subheader("This app was Created by Shivam Pandey")

            elif(task=='How to use the calculator'):
                st.markdown("""
                * In the task option select Find price.
                * Go to the sidebar and Provide all the values required
                * **Present Price:** Refers to the present showroom price of the car
                * **KMs Driven:** Enter the number of Kilometers Driven
                * **Car Type:** Enter whether your car is first,second or third hand.
                * **Years Old:** Enter how many years old your car is.
                * **Fuel Type:** Enter the fuel type of your Car.
                * **Seller Type:** Enter Seller Type of your car.
                * **Transmission Type:** Enter the transmission type of your car.
                """)            
        else:
            st.warning("Incorrext username/password")
elif(choice=='Sign up'):
    st.subheader('Create New account')
    new_user=st.text_input("Enter Your Username")
    new_pass=st.text_input("Enter your password",type='password')

    if st.button('Sign Up'):
        create_table()
        add_userdata(new_user,new_pass)
        st.success("Signed UP successfully")
        st.info("Go to login page")

elif (choice=="sign up"):
    st.subheader('Create New account')

            
