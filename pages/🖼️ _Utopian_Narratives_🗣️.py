
from dotenv import find_dotenv,load_dotenv
from transformers import pipeline


from langchain import PromptTemplate, LLMChain, OpenAI
import requests
import os
import streamlit as st

load_dotenv(find_dotenv())
HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACEHUB_API_TOKEN")


def img2text(url):
    """
    Caption the image using the BLIP from Salesforce on Hugging Face
    """
    image_to_text = pipeline("image-to-text", model = "Salesforce/blip-image-captioning-large")
    text = image_to_text(url)[0]["generated_text"]
    
    print(text)
    return text


def generate_story(scenario):
    """
    Create a templated prompt for GPT-3.5 turbo
    """

    template = """
    You are a story teller;
    You can generate a short utopian sci-fi story based on a simple narrative, the story should be no more than 200 words;

    CONTEXT: {scenario}
    STORY:
    """

    prompt = PromptTemplate(template =template, input_variables=["scenario"])

    story_llm = LLMChain(llm=OpenAI(model_name="gpt-4", temperature = 0.9), prompt=prompt, verbose =True)

    story = story_llm.predict(scenario=scenario)

    print(story)
    return story


def text2speech(message):
    
    """
    Translate text story into audio
    """
    import requests
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}

    payloads = {
        "inputs": message
    }
    
    response = requests.post(API_URL, headers=headers, json=payloads)
    with open('audio.flac','wb') as file:
        file.write(response.content)


def main():
    
    st.set_page_config(page_title="Utopian dreams ", page_icon="🎧")
    
    st.header("Turn an image 🖼️ to an audio story🗣️")
    uploaded_file = st.file_uploader("Upload an image...", type = "png")

    if uploaded_file is not None:
        with st.spinner("Generating an awesome audio story..."):
            bytes_data = uploaded_file.getvalue()
            with open(uploaded_file.name, "wb") as file:
                file.write(bytes_data)
            st.image(uploaded_file, caption= 'Uploaded image.', use_column_width= True)
            scenario = img2text(uploaded_file.name)
            story = generate_story(scenario)
            text2speech(story)

            with st.expander("scenario"):
                st.write(scenario)
            with st.expander("story"):
                st.write(story)

            st.audio("audio.flac")


if __name__ == "__main__":
    main()
