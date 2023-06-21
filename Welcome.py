import streamlit as st
st.set_page_config(
    page_title="Home",
    page_icon="👾",
)
st.write("### 👋🏼 LLM Playground 🔮")
st.markdown(
    """
    This is a collection of mini AI apps built with Streamlit.
    It provides some examples of what LLMs can do!

     **👈 Select demos from the sidebar** 

    ##### 🔎 Research Assistant 🪄
    * Ask a research question, get a thread of actionable article summaries source from filtered Google searches. 
    


    ##### 🎙️ Keynote Talk Generator
    * Ask a question, get a tight keynote presentation outline with topics summaries from Wikipedia. 

    

    ##### 💬 Chat with Reports
    * Upload PDF reports and chat with them to better understand their context.

    
    
    ##### 🖼️ Utopian Narratives 🗣️
    * Upload a picture, get a short utopian audio story inspired by the scene. 

    
    ### Tools used:

    - Streamlit [documentation](https://docs.streamlit.io)
    - OpenAI API [documentation](https://platform.openai.com/docs/introduction)
    - Langchain [documentation](https://python.langchain.com/en/latest/)
    - Llama Index [documentation](https://gpt-index.readthedocs.io/en/latest/)
    - HuggingFace Transformers[Docs](https://huggingface.co/docs/transformers/installation)
    - FAISS [documentation](https://github.com/facebookresearch/faiss)
    - Serper [documenation](https://serper.dev/)

    """
)


#  ##### URL Summary
#     * A sample app for summarizing URL content using LangChain and OpenAI. Upload a URL and summarize the content on the website. 
#     * References: [Blog](https://alphasec.io/blinkist-for-urls-with-langchain-and-openai) | [Source Code](https://github.com/alphasecio/langchain-examples/blob/main/url-summary)

    