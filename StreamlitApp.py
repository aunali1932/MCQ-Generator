import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGENERATOR import generate_evaluate_chain
from src.mcqgenerator.logger_ import logging

RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

# with open('D:\practise\MCQ Generator\Response.json','r') as file:
#     RESPONSE_JSON = json.load(file)

st.title("Mcq Generator With LangChain")

with st.form("user_inputs"):

    uploaded_files = st.file_uploader("Upload a PDF or Txt")

    mcq_count = st.number_input("No of Mcqs", min_value=4,max_value=50)

    subject= st.text_input("Subject: ",max_chars=20)

    tone = st.text_input("Complexity of Questions", max_chars=20, placeholder="Simple")

    button= st.form_submit_button("Create Mcq")

    if button and uploaded_files and mcq_count and subject and tone is not None :
        logging.info("Button Working...")
        with st.spinner("loading..."):
            try:
                logging.info("File Read succesfull")
                text = read_file(uploaded_files)

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text" : text,
                            "number": mcq_count,
                            "subject" : subject,
                            "tone" :tone,
                            "response_json" : json.dumps(RESPONSE_JSON)
                        }
                    )
                    print(f"Tokens: {cb.total_tokens}")
                    print(f"Prompt Tokens: {cb.prompt_tokens}")
                    print(f"Completion Tokens: {cb.completion_tokens}")
                    print(f"Cost: {cb.total_cost}")
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                
                logging.info("Printing Table")
                if isinstance(response,dict):
                    quiz= response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df =pd.DataFrame(table_data)
                            df.index += 1
                            st.table (df)
                            st.text_area(label="Review", value = response["review"])
                        else:
                            st.error("Error in table data")

                    else:
                        st.write(response)





