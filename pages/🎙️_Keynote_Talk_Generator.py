#Import necessary libraries and set the OpenAI API key.
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

import streamlit as st 
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

#app framework
st.set_page_config(page_title="Keynote Generator", page_icon="🗣️")
st.title('🎙️ Define a topic, get a script')
prompt = st.text_input("Enter a topic you'd like to give a lecture about.")


#prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = 'Write me a innovative keynote presentation title about {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'],
    template = 'Write a lecture script based on this TITLE: {title} while leveraging this wikipedia research:{wikipedia_research}'
)

#memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

                                  
#LLMs
llm = OpenAI(model_name="gpt-4", temperature=0.9)
#llm = OpenAI(temperature = 0.9)
title_chain = LLMChain(llm=llm, prompt = title_template, verbose = True, output_key = 'title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt = script_template, verbose = True, output_key = 'script', memory=script_memory)

wiki= WikipediaAPIWrapper()

#show something to the screen if there's a prompt
if prompt:
    with st.spinner("Generating awesome keynote content..."):
        title = title_chain.run(prompt)
        wiki_research = wiki.run(prompt)
        script = script_chain.run(title=title, wikipedia_research=wiki_research)
        st.write (title)
        

        with st.expander('Talk title'):
            st.info(title_memory.buffer)

        with st.expander('Talk script'):
            st.info(script_memory.buffer)

        with st.expander('Idea sources'):
            st.info(wiki_research)

