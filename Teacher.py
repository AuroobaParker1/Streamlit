import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Drive
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Try to open the Google Sheet
try:
    sheet = gc.open('Data Gathered')
except gspread.exceptions.SpreadsheetNotFound:
    # If the sheet doesn't exist, create a new one
    sheet = gc.create('Data Gathered')

# Get the first worksheet
worksheet = sheet.get_worksheet(0)

# Read data from Google Sheets
try:
    df = pd.DataFrame(worksheet.get_all_records())
    print("DAta",df)
except gspread.exceptions.APIError:
    df = pd.DataFrame(columns=['Question', 'Markscheme 1', 'Markscheme 2'])

num_sets = st.number_input('How many sets of inputs do you want to enter?', min_value=1, value=1)

for i in range(num_sets):
    st.write(f"Set {i+1}")
    question = st.text_area(f'Enter question for Set {i+1} here:', key=f'question_{i}')
    markscheme_1 = st.text_area(f'Enter markscheme 1 for Set {i+1} here:', key=f'markscheme_1_{i}')
    markscheme_2 = st.text_area(f'Enter markscheme 2 for Set {i+1} here:', key=f'markscheme_2_{i}')

    if st.button(f'Submit Set {i+1}'):
        new_data = {'Question': [question], 'Markscheme 1': [markscheme_1], 'Markscheme 2': [markscheme_2]}
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)

        # Save the DataFrame to Google Sheets
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
