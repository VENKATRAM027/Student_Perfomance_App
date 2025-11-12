import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler,LabelEncoder


def load_model():
    with open('Student_lr_final_model.pkl','rb') as file:
        model,scaler,le = pickle.load(file)
    return model,scaler,le    

def preprocessing_input_data(data,scaler,le):
    data['Extracurricular Activities'] = le.transform([data['Extracurricular Activities']])[0]
    df = pd.DataFrame([data])
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

    Hours_Studied = st.number_input("Hours Studied",min_value = 1, max_value =10, value = 5)
    Previous_Scores = st.number_input("Previous Score",min_value = 40, max_value =100, value = 70)
    Extra_curricular_activities = st.selectbox('Extra Curricular Activities',['Yes','No'])
    Sleeping_hours = st.number_input("Sleeping Hours",min_value=4,max_value=10,value=7)
    Number_of_question_papers_solved = st.number_input('Number of question papers solved',min_value=4,max_value=10,value=7)

    if st.button('Predict Your Score'):
        user_data = {
            'Hours Studied' : Hours_Studied,
            'Previous Scores' : Previous_Scores,
            'Extracurricular Activities' : Extra_curricular_activities,
            'Sleep Hours'  : Sleeping_hours,
            'Sample Question Papers Practiced' : Number_of_question_papers_solved
        }

        prediction = predict_data(user_data)
        st.success(f"Your Prediction Result Is {prediction}")

if __name__ == '__main__':
    main()    