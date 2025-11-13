import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler,LabelEncoder
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

raw_username = "VenkatRam"
raw_password = "Venkat@2004"  # The password with the special '@' character
cluster_address = "cluster0.ly8admn.mongodb.net"

username = quote_plus(raw_username)
password = quote_plus(raw_password)

uri = f"mongodb+srv://{username}:{password}@{cluster_address}/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['student']
collection = db['student_pred']


def load_model():
    with open('Student_lr_final_model.pkl','rb') as file:
        model,scaler,le = pickle.load(file)
    return model,scaler,le    

def preprocessing_input_data(data, scaler, le):
    # Create a copy of the dictionary to work with
    # This prevents changing the original user_data
    data_for_processing = data.copy()

    # Perform the label encoding on the copy
    data_for_processing['Extracurricular Activities'] = le.transform([data_for_processing['Extracurricular Activities']])[0]
    
    # Continue processing with the copy
    df = pd.DataFrame([data_for_processing])
    df_transformed = scaler.transform(df)
    
    return df_transformed

def predict_data(data):
    model,scaler,le = load_model()
    processed_data = preprocessing_input_data(data,scaler,le)
    prediction = model.predict(processed_data)
    return prediction 

def main():
    st.title('Student Perfomance Prediction')
    st.write('Enter your data to get a prediction for your perfomance')
    
    # --- Input Fields ---
    Hours_Studied = st.number_input("Hours Studied", min_value=1, max_value=10, value=5)
    Previous_Scores = st.number_input("Previous Score", min_value=40, max_value=100, value=70)
    Extra_curricular_activities = st.selectbox('Extra Curricular Activities', ['Yes', 'No'])
    Sleeping_hours = st.number_input("Sleeping Hours", min_value=4, max_value=10, value=7)
    Number_of_question_papers_solved = st.number_input('Number of question papers solved', min_value=4, max_value=10, value=7)
    
    # --- Prediction and Database Logic ---
    if st.button('Predict Your Score'):
        # 1. Collect user data into a dictionary
        user_data = {
            'Hours Studied': Hours_Studied,
            'Previous Scores': Previous_Scores,
            'Extracurricular Activities': Extra_curricular_activities,
            'Sleep Hours': Sleeping_hours,
            'Sample Question Papers Practiced': Number_of_question_papers_solved
        }

        # Use a spinner for better user experience while processing
        with st.spinner('Calculating your score...'):
            # 2. Get the prediction
            prediction_array = predict_data(user_data)
            
            # 3. Extract the single prediction value from the numpy array
            prediction_value = float(prediction_array[0])
            
            # 4. Display the result to the user
            st.success(f"Your Predicted Score Is: {prediction_value:.2f}") # Formatted to 2 decimal places

            # 5. Add the prediction result to the user_data dictionary
            #    This is the dictionary we will save to MongoDB
            data_to_save = user_data.copy() # Use a copy to be safe
            data_to_save['prediction'] = prediction_value
            
            # 6. Insert the combined data and prediction into the collection
            #    This fixes the np.int64 issue because we are converting it to float
            try:
                collection.insert_one(data_to_save)
                st.info("Prediction saved to the database successfully.")
            except Exception as e:
                st.error(f"Failed to save data to the database: {e}")

# This should remain the same
if __name__ == '__main__':
    main()