import tensorflow as tf
model = tf.keras.models.load_model('batt.h5')
import streamlit as st
import mysql.connector
from PIL import Image, ImageOps
st.set_page_config(
     page_title="Used Battery Collector",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.google.com',
         'Report a bug': "https://mail.google.com/mail",
         'About': "# There is nothing here."
     }
 )

def import_and_predict(img, model):
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = tf.image.resize(img, [256, 256])
    img = tf.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return prediction

if 'account' not in st.session_state:
     st.session_state.account = dict()
st.write("""
         # Battery type Classification
         """
         )
st.write("This is a simple image classification web app to classify battery type")
email = st.text_input("Enter your email:", "trojan@usc.edu")
if 'email' not in st.session_state:
    st.session_state.email = False
press = st.button('Submit')
if press:
    st.session_state.email = True
    # myObj = {"action":"registration","email":email};
if st.session_state.email:
    st.write('You sign in as', email)
    if email not in st.session_state.account.keys():
          st.session_state.account[email] = 0
    
    
    file = st.camera_input("Take a Picture")
    #file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

    if file is None:
        st.text("Please upload an image file")
    else:
        # myObj = {"action":"photo","email":email};
        
        image = Image.open(file)
        st.image(image, use_column_width=True)
        res = import_and_predict(image, model)
          
        if res[0][0]>res[0][1] and res[0][0]>res[0][2]:
            st.write("It is a 9V Battery")
            st.session_state.account[email] += 3
            st.write("You got 3 MRC credits! Your current MRC balance is", st.session_state.account[email])
        elif res[0][1]>res[0][0] and res[0][1]>res[0][2]:
            st.write("It is AA Battery")
            st.session_state.account[email] += 2
            st.write("You got 2 MRC credits! Your current MRC balance is", st.session_state.account[email])
        else:
            st.write("It is Button Battery")
            st.session_state.account[email] += 1
            st.write("You got 1 MRC credit! Your current MRC balance is", st.session_state.account[email])
