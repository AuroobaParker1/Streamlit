import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Drive
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
try:
    sheet = gc.open('Data Gathered')
except gspread.exceptions.SpreadsheetNotFound:
    # If the sheet doesn't exist, create a new one
    sheet = gc.create('Data Gathered')

# Get the first worksheet
worksheet = sheet.get_worksheet(0)

# Read data from Google Sheets
try:
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except gspread.exceptions.APIError:
    df = pd.DataFrame(columns=['Question'])

questions = df['Question'].tolist()

students = df.columns.difference(['Question']).tolist()

student_name = st.text_input('Enter your ERP:')

if student_name:
    for i, question in enumerate(questions):
        st.write(f"Question {i + 1}: {question}")
        answer = st.text_area(f'Enter your answer to Question {i + 1} here:', key=f'answer_{i}')

        if st.button(f'Submit Answer to Question {i + 1}'):
            if student_name not in students:
                students.append(student_name)

            if student_name in df.columns:
                df[student_name].iloc[i] = answer
            else:
                new_col = pd.Series(index=df.index, dtype=object)
                new_col.iloc[i] = answer
                df[student_name] = new_col

            # Save the DataFrame to Google Sheets
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
