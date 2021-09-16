import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image

st.set_page_config(layout="wide")

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
    Owner=st.sidebar.selectbox('Car type',('First Hand','Second Hand','Third Hand'))
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
