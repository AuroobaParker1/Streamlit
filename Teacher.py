import streamlit as st
import pandas as pd

# Load existing data from the Excel file, if any
try:
    df = pd.read_excel('output.xlsx')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Question', 'Markscheme 1', 'Markscheme 2'])

num_sets = st.number_input('How many sets of inputs do you want to enter?', min_value=1, value=1)

for i in range(num_sets):
    st.write(f"Set {i+1}")
    question = st.text_area(f'Enter question for Set {i+1} here:', key=f'question_{i}')
    markscheme_1 = st.text_area(f'Enter markscheme 1 for Set {i+1} here:', key=f'markscheme_1_{i}')
    markscheme_2 = st.text_area(f'Enter markscheme 2 for Set {i+1} here:', key=f'markscheme_2_{i}')
    # response = st.text_area(f'Enter response for Set {i+1} here:', key=f'response_{i}')

    if st.button(f'Submit Set {i+1}'):
        new_data = {'Question': [question], 'Markscheme 1': [markscheme_1], 'Markscheme 2': [markscheme_2]}
        df = pd.concat([df,pd.DataFrame(new_data)], ignore_index=True)

        # Save the DataFrame to an Excel file
        df.to_excel('output.xlsx', index=False)
