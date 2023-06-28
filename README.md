# LLM Playground

## Introduction
------------
 This is a collection of baisc AI apps built with Streamlit. 
 It provides some examples of what LLMs can do!

### 🔎 Research Assistant 🪄

What it does: 
Ask a research question, get a thread of actionable article summaries source from filtered Google searches.  


### 🎙️ Keynote Talk Generator

What it does: 
Ask a question, get a tight keynote presentation outline with topics summaries from Wikipedia. 


### 💬 Chat with Reports

What it does: 
Upload PDF reports and chat with them to better understand their context. 


### 🖼️ Utopian Narratives 🗣️

What it does: 
Upload a picture, get a short utopian audio story inspired by the scene. 

How it works:
------------
1. Convert an image to text using the Salesforce BLIP image captioning model.
2. Generate a short sci-fi love story based on a given scenario using the GPT-3.5 turbo language model.
3. Translate the generated text story into audio using the ESPnet Kan-Bayashi LJ Speech VITS model.
4. Create a web interface using Streamlit to upload an image, process it, generate a story, and play the audio.


# Dependencies 
----------------------------
Install:

1. Clone the repository to your local machine.

2. Create VM and install dependencies from .yml

Using `micromamba`:
``` bash
cd llm-playground
micromamba env create -f environment.yml
micromamba activate ai-labs
```

3. Create a `.env` file in the root directory of the project. Inside the file, add your OpenAI API key:

```makefile
OPENAI_API_KEY= "your_api_key_here"
HUGGINGFACEHUB_API_TOKEN= "your_api_key_here"
SERPAPI_API_KEY = "your_api_key_here"
```

## Usage
-----
Steps:

1. Ensure that you have installed the required dependencies and added the API keys to the `.env` file.

2. Run the `Welcome.py` file using the Streamlit CLI. Execute the following command:
   ```
   streamlit run Welcome.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Have fun!

