import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from chat_with_pdfs.htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf_docs):
    """
    Loops through each pdf, extracts the text, and concats the raw text into the text variable  
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        #loop through each page of a pdf
        for page in pdf_reader.pages:
            #extract text
            text += page.extract_text()
    return text


def get_text_chunks(text):
    """
    Implement a new instance of Langchain's Character Text Splitter class.
    Define its parameters - separate by single line breaks, 1000 character chunks, 
    overlap by 20% to enable meaning connection

    """
    text_splitter = CharacterTextSplitter(
        separator = "/n", 
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    """
    Create vector database using FAISS. 
    FAISS is just like Pinecone/Chroma except that it runs locally and stores 
    generated vector embeddings locally. They are deleted whey you stop the program.
    Not persistant!
    """
    #embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    """
    Takes the history of the conversation and generates the next part of the conversation. 
    Check https://python.langchain.com/en/latest/modules/memory/types/buffer.html for 
    refresher on how Langchain enables conversational memory.
    Check https://python.langchain.com/en/latest/modules/chains/index_examples/chat_vector_db.html allows 
    you to chat with vector store with memory.

    """
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key = 'chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm, 
        retriever = vectorstore.as_retriever(), 
        memory = memory
    )
    return conversation_chain


def handle_userinput(user_question):
    '''
    I'm still confused about how this works. 
    '''
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 ==0: 
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Reports", page_icon="💬")

    st.write(css, unsafe_allow_html=True)

    #if application not in session state it will reinitialize it. 
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("💬 Learn more about your prospects by chatting with their publications.")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        with st.spinner("Generating response..."):
            handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload multiple PDFs here and click on 'Analyze' button", accept_multiple_files=True)
        if st.button("Analyze"):
            with st.spinner("Analyzing Docs"):
                #get the raw PDF text
                raw_text = get_pdf_text(pdf_docs)

                #get the text chunks
                text_chunks = get_text_chunks(raw_text)

                #create vector store with embeddings
                vectorstore = get_vectorstore(text_chunks)

                #create conversation chain, Streamlit has the tendency to reload all variables when you interact with it
                #Session State lets Streamlit know to keep this variable persistant, Important because we want to maintain 
                #langchain's memory of the conversation
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()
