import streamlit as st
import json
from utils import (
    get_stock_price,
    calculate_SMA,
    calculate_EMA,
    calculate_RSI,
    calculate_MACD,
    plot_stock_price,
    get_latest_news,
    functions
)
from openai_functions import get_openai_response, client

available_functions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price,
    'get_latest_news': get_latest_news
}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title('Stock Analysis Chatbot Assistant')

user_input = st.text_input('Your input:')



if user_input:
    try:
        st.session_state['messages'].append({'role': 'user', 'content': f'{user_input}'})
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=st.session_state['messages'],
            functions=functions,
            function_call='auto'
        )
        response_message = response.choices[0].message
        print(response_message)
        
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price']:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}
            else:
                args_dict = {'ticker': function_args.get('ticker')}
            
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**args_dict)

            if function_name == 'plot_stock_price':
                st.image('stock.png')
            else:
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {
                        'role': 'function',
                        'name': function_name,
                        'content': function_response
                    }
                )
                second_response = client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=st.session_state['messages']
                )
                st.text_area("Response:", second_response.choices[0].message.content, height=200)
                st.session_state['messages'].append({'role': 'assistant', 'content': second_response.choices[0].message.content})
        else:
            st.text_area("Response:", response_message.content, height=200)
            st.session_state['messages'].append({'role': 'assistant', 'content': response_message.content})
    except Exception as e:
        st.text_area("Error occurred:", str(e), height=200)