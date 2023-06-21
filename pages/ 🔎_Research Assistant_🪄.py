
#1. search relevant articles on the internet
#2. Use llm to choose the best article, return a url
#3. Get content from each article and make a summar
#4. Turn each summary into an abstracted but actionalble twitter thread

import os 
from dotenv import find_dotenv, load_dotenv
import requests
import json
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import openai
import streamlit as st

load_dotenv(find_dotenv())
SERPAPI_API_KEY= os.getenv("SERPAPI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

#1. search relevant articles on the internet         
def search(query):
    """
    Search relevant articles on the internet using SERPER API (https://serper.dev/); a google search API
    Create a list of query relevant articles.
    """
    
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': SERPAPI_API_KEY, 
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()

    print("search results: ", response_data)
    return response_data

#2. Use llm to choose the best article, return a url
def find_best_article_urls(response_data, query):
    """
    Use llm to choose the best article, return a url
    """
    #turn json into a string, need a string to input into LLM
    response_str = json.dumps(response_data)

    #create llm to choose best articles
    llm = OpenAI(model_name="gpt-4", temperature=0.7)

    #can edit this template to refine the types of summaries you get
    template = """
    You are a world class journalist and researcher. You are extremely talented at finding the most relevant articles related to a specific topic {response_str}
    Above is the list of search results for the query {query}.
    Please choose the best 3 articles from the list, return ONLY an array of urls, do not include anything else. 
    """
    prompt_template = PromptTemplate(
        input_variables= ["response_str", "query"], template=template)

    #Create an llm chain (a sequesnce of steps that combines primatives and LLM model to process user input, generate propmts and leverage OpenAI model)
    article_picker_chain= LLMChain(llm=llm, prompt=prompt_template, verbose=True)
        
    urls = article_picker_chain.predict(response_str=response_str, query=query)

    #convert string to list
    url_list = json.loads(urls)
    print(url_list)

    return url_list

#3. Get content from each article and make a summary
def get_content_from_urls(urls):
    """
    Use langchain to extract content from prioritized URLS
    """
    #use unstructuredURLloader
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    return data

def summarize(data, query):
    """
    Split up the injected text and summarize it using 
    """
    #token limit for gpt-3.5 is 4000 so keep chunks below with a margin!
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=3000, chunk_overlap =200, length_function=len)
    text = text_splitter.split_documents(data)

    llm = OpenAI(model_name="gpt-4", temperature=0.7)

    
    #!!!!fine tune results by editing this template prompt
    template = """
    {text}
    You are a world class journalist and researcher. You will summarize the text above to create an engaging twitter thread about {query}.
    Please follow all of the following rules:
    1/ Make sure the content is engaging and informative with verifiable data
    2/ Make sure the content is not too long, it should not be longer than 3-5 tweets
    3/ The content should address the {query} topic very well
    4/ The content needs to be written so that it is easy to read and understand 
    5/ The content needs to be viral, it should get at least 1500 likes
    6/ The content needs to give the reader actionable advice and insights
  
    SUMMARY:
    """

    prompt_template = PromptTemplate(input_variables=["text", "query"], template=template)
    
    summarizer_chain= LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    
    #for each chunk in text array run the summarizer chain and add results into an array of summaries
    summaries = []
    for chunk in enumerate(text):
        summary = summarizer_chain.predict(text=chunk[1], query=query)
        summaries.append(summary)

    print(summaries)
    return summaries


#4. Turn each summary into an abstracted but actionalble twitter thread

def generate_thread(summaries, query):
    """
    Create summary threads of intial summaries.
    """

    #turn array of summaries into a string
    summaries_str = str(summaries)

    #create an LLM
    llm = OpenAI(model_name="gpt-4", temperature=0.7)

    #!!!!fine tune results by editing this template prompt
    template = """
    {summaries_str}

    You are a world class journalist and twitter influencer. The text above is some context about {query}.
    Please write a viral twitter thread about {query} using the test above.
    Please follow all of the following rules:
    1/ The thread needs to be engaging and informative with verifiable data
    2/ The thread needs to be around 3-5 tweets
    3/ The thread needs should address the {query} topic very well
    4/ The thread needs to be written so that it is easy to read and understand 
    5/ The thread needs to be viral, it should get at least 1500 likes
    6/ The thread needs to give the reader actionable advice and insights

    TWITTER THREAD:
    """

    
    prompt_template = PromptTemplate(input_variables=["summaries_str", "query"], template=template)
    
    twitter_thread_chain= LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    twitter_thread = twitter_thread_chain.predict(summaries_str=summaries_str, query=query)

    return twitter_thread


#streamlit UI
def main():
    st.set_page_config(page_title="Generate actionable ideas", page_icon="🔎", layout="wide")

    st.header("🔎 Define a topic, get actionable insights 🪄")
    query = st.text_input("Enter a research question")

    if query: 
        with st.spinner("Scouring the internet..."):
            print(query)
            st.write("...to generating research summaries concerning: ", query)
            
            #run through functions with query
            search_results = search(query)
            urls = find_best_article_urls(search_results, query)
            data = get_content_from_urls(urls)
            summaries = summarize(data, query)
            thread = generate_thread(summaries, query)

            #display outputs via expandable ui elements for review
            with st.expander("Web search results"):
                st.info(search_results)
            with st.expander("Most relevant urls"):
                st.info(urls)
            # with st.expander("Scraped data"):
            #     st.info(data)
            # with st.expander("Site summaries"):
            #     st.info(summaries)
            with st.expander("Actionable insights"):
                st.info(thread)

if __name__ == '__main__':
    main()