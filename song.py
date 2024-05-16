import streamlit as st
import json
import requests

st.title('Song Popularity prediction')
st.subheader('Group 1')
st.subheader('Charlie Jiang')
st.subheader('Kousik Kalyan Guptha Yakkali')
st.subheader('Shuvam Chatterjee')
st.subheader('Saahithi Chippa')

yesOrNoKeys = ['licensed', 'official_video']
with open('input_options.json') as f:
    side_bar_options = json.load(f)
    options = {}
    for key, value in side_bar_options.items():
        if key in yesOrNoKeys:
            options[key] = st.sidebar.selectbox(key, value)
        else:
            min_val, max_val = value
            min_val = float(min_val)
            max_val = float(max_val)
            current_value = float((min_val + max_val)/2)
            step_size = 1.0
            options[key] = st.sidebar.slider(key, min_val, max_val, current_value, step_size)


st.write(options)

if st.button('Predict'):
    # Prepare payload for prediction
    payload = json.dumps({'dataframe_records': [[item for item in options.values()]]})

    # Send request to the model server
    response = requests.post(
        url=f"http://104.131.17.187:5002/invocations",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    # Get regression prediction from the response
    regression_prediction = response.json().get('predictions')[0]

    # Display regression prediction
    st.title(f'Song popularity by like: {regression_prediction:.2f}')