import streamlit as st
import pandas as pd
import openpyxl
from github import Github

g = Github("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")


repo = g.get_repo("AuroobaParker1/Streamlit")


file = repo.get_contents("output.xlsx")

try:
    df = pd.read_excel(file)
except FileNotFoundError:
    df = pd.DataFrame()

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

            print(answer)
            repo.update_file(file.path, "Update from Streamlit", df.to_excel('output.xlsx', index=False, engine='openpyxl').getValue(), file.sha)

   