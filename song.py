import streamlit as st
import json
import requests

# Title and group members
st.title('Song Popularity Prediction')
st.subheader('Group 1')
st.subheader('Charlie Jiang')
st.subheader('Kousik Kalyan Guptha Yakkali')
st.subheader('Shuvam Chatterjee')
st.subheader('Saahithi Chippa')

# Load options from JSON file
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
            current_value = float((min_val + max_val) / 2)
            step_size = 1.0
            options[key] = st.sidebar.slider(key, min_val, max_val, current_value, step_size)

st.write(options)

if st.button('Predict'):
    # Prepare payload for prediction
    payload = json.dumps({'dataframe_records': [list(options.values())]})

    try:
        # Send request to the model server
        response = requests.post(
            url=f"http://104.131.17.187:5002/invocations",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        
        # Check the response status
        if response.status_code == 200:
            response_json = response.json()
            
            # Debugging: Print the JSON response to see its structure
            st.write(response_json)
            
            # Check if the 'predictions' key exists in the response
            if 'predictions' in response_json:
                regression_prediction = response_json['predictions'][0]
                st.title(f'Song popularity by like: {regression_prediction:.2f}')
            else:
                st.error("The response does not contain 'predictions'")
        elif response.status_code == 404:
            st.error("Endpoint not found. Please check the URL and try again.")
        else:
            st.error(f"Failed to get a valid response. Status code: {response.status_code}")
            st.write(response.text)  # Print the response content for debugging

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

    # Print the URL being used
    st.write(f"Request URL: http://104.131.17.187:5002/invocations")
