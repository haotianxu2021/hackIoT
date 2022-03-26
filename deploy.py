import tensorflow as tf
model = tf.keras.models.load_model('batt.h5')
import streamlit as st
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
if st.session_state.email:
    st.write('You sign in as', email)
    file = st.camera_input("Take a Picture")
    #file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

    if file is None:
        st.text("Please upload an image file")
    else:
        image = Image.open(file)
        st.image(image, use_column_width=True)
        res = import_and_predict(image, model)
        if res[0][0]>res[0][1] and res[0][0]>res[0][2]:
            st.write("9V Battery")
        elif res[0][1]>res[0][0] and res[0][1]>res[0][2]:
            st.write("AA Battery")
        else:
            st.write("Button Battery")
