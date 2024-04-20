import streamlit as st
import openai
import os
import pandas as pd
import numpy as np
from dotenv import dotenv_values
import openpyxl
from openai import OpenAI

#
# the sentiment func
def gpt_classify_sentiment(prompt, emotions):
    system_prompt = f'''
    You are an emotionally intelligent assistant.
    Classify the sentiment of the user's text with only ONE OF THE FOLLOWING: {emotions}.
    '''
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content':system_prompt},
            {'role': 'user', 'content':prompt}
            ],
        #max_tokens=20,
        temperature=0
        )
    r = response.choices[0].message.content
    if r =='':
        r = 'N/A'
    return r


def setup_streamlit():
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title('Zero-Shot Sentiment Analysis')
    with col2:
        st.image('ai.png', width=70)
    with st.form(key='my_form'):
        default_emotions = "positive, negative, neutral"
        emotions = st.text_input('emotions', value=default_emotions)
        text = st.text_area(label='Text to classify')
        submit_button = st.form_submit_button(label='Check')
        if submit_button:
            emotions = gpt_classify_sentiment(text, emotions)
            result = f"{text}  =>  {emotions}\n"
            st.write(result)

#
# text = 'AI will take over the world'
# result = gpt_classify_sentiment(text, emotions)
# print(result)

if __name__ == '__main__':
    #
    # setup client
    config = dotenv_values(f"{os.path.expanduser('~')}/.env")
    os.environ['OPENAI_API_KEY'] = config["OPENAI_API_KEY"]
    openai.api_key = os.environ['OPENAI_API_KEY'].strip()
    try:
        assert openai.api_key.startswith('sk-')
    except AssertionError as ae:
        print(f'{ae} Invalid OpenAI API key')
    client = OpenAI()
    #
    #
    #
    setup_streamlit()