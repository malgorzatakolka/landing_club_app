import pandas as pd
import os
from pycaret.classification import load_model, predict_model
import streamlit as st

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT",
        "DC", "DE", "FL", "GA", "HI", "ID", "IL",
        "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE",
        "NV", "NH", "NJ", "NM", "NY", "NC", "ND", 
        "OH", "OK", "OR", "PA", "RI", "SC", "SD",
        "TN", "TX", "UT", "VT", "VA", "WA", "WV", 
        "WI", "WY"]

titles = ['Debt consolidation',
        'Credit card refinancing',
        'Other',
        'Business',
        'Medical expenses',
        'Major purchase',
        'Home buying',
        'Home improvement',
        'Moving and relocation',
        'Car financing',
        'Vacation']
st.set_page_config(
    page_title="Landing club loans' predictions",
     page_icon='💵')

def main():

    style = """<div style='background-color:pink; text-align:center;'>
              <h1 style='color:black'>Landing Club loans' predictions</h1>
       </div>"""
    st.markdown(style, unsafe_allow_html=True)

    model1 = load_model("reject_accept_api")
    model2 = load_model("grade_classification")
    model3 = load_model("interest_rate")

    st.write("")
    st.write('**Fill in to predict loan eligibility**')
    left, right = st.columns((2,2))
    amount = left.slider('Amount', 1, 40000)
    risk_score = right.slider('Risk score', 1, 999)
    dti = left.slider('Debt_to_income ratio', 0, 100)
    state = right.selectbox('State',
                                     states)
    emp_length = left.slider('Employment length',
                                       0.5, 60.0)
 
    
    accept_data = pd.DataFrame([{'amount': amount,
                          'risk_score': risk_score,
                          'dti': dti,
                          'state': state,
                          'emp_length': emp_length}])

    button = st.button('Predict application')
    
    if button:
        
        # make prediction
        predictions = predict_model(model1, data=accept_data)
        if predictions["prediction_label"].iloc[0] == 0:
            st.error(f'Not qualified for loan with prediction score {predictions["prediction_score"].iloc[0]}')

        else:
            st.success(f'Qualifies for loan with prediction score {predictions["prediction_score"].iloc[0]}')


    st.write("")
    st.write("**Fill in to predict grade and interest rate of application**")
    left, right = st.columns((2,2))
    pub_rec = left.slider('Public record', 0.0, 4.0)
    revol_bal = right.slider('Revolving balance', 0.0, 600000.0)
    revol_util = left.slider('Revolving utilised', 0.0, 135.0)
    total_acc = right.slider('Total number of credit lines', 0.0, 96.0)
    term = left.selectbox('Term', [3, 5])
    home_ownership = right.selectbox('Home ownership', ['OWN', 'RENT', 'MORTGAGE', 'ANY'])
    annual_inc = left.slider('Annual income', 10000.0, 1656000.0)
    delinq_2yrs = right.slider('Deliquency in last 2 yrs', 0.0, 12.0)
    earliest_cr_line = left.slider('Earliest credit line', 1960, 2018)
    verification_status = right.selectbox('Verification status', [0, 1])
    title = left.selectbox('Title', titles)
    button_1 = st.button('Predict interest rate and grade')


    
    grade_rate_data = pd.DataFrame([{'amount': amount,
                         'pub_rec': pub_rec, 
                         'revol_bal': revol_bal,
                         'revol_util': revol_util, 
                         'total_acc': total_acc, 
                         'term': term,
                        'emp_length': emp_length, 
                        'home_ownership': home_ownership, 
                        'annual_inc': annual_inc, 
                        'verification_status': verification_status,
                        'state': state, 
                        'dti': dti, 
                        'delinq_2yrs': dti, 
                        'earliest_cr_line': earliest_cr_line, 
                        'risk_score': risk_score,
                        'title': title}])
            
    if button_1:
        grade_prediction = predict_model(model2, data=grade_rate_data)
        rate_prediction = predict_model(model3, data=grade_rate_data )
        st.success(f'Predicted grade: {grade_prediction["prediction_label"].iloc[0]}')
        st.success(f'Predicted interest rate: {rate_prediction["prediction_label"].iloc[0]}%')
main()