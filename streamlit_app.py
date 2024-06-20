import streamlit as st
from elevenlabs import play, stream, save
import elevenlabs
from elevenlabs.client import ElevenLabs
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import ffmpeg
import base64

import io



#Variables: Initialize -> read Docs only at 1st time, API Keys
initialize = True
os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
client = ElevenLabs(
    api_key= st.secrets["EL_KEY"]
    )

#Title and Logo of MEM Bot
col1, col2 = st.columns(2)
st.logo('https://www.hs-pforzheim.de/typo3conf/ext/wr_hspfo/Resources/Public/Images/logo.svg')
with col1:
    st.title('MEM-Bot 1.0')
with col2:
    st.image('MemBot-Logo.png')
CHUNK_SIZE = 1024

#Chat functionality

activetts = st.toggle("Read answer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("Assistant"):
        if initialize:
            reader = SimpleDirectoryReader(input_dir="data", recursive=True)
            documents = reader.load_data()
            index = VectorStoreIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            initialize = False
        response = query_engine.query(str(prompt))
        st.session_state.messages.append({"role": "Assistant", "content": response})
        if activetts:
            audio = client.generate(
                text=str(response),
                voice = "PFBcP8jRKW2qht5HPwFt",
                model = "eleven_multilingual_v2",
                output_format="mp3_44100_128"
            )
            save(audio, "output.mp3")
    
    # Read the audio file into bytes
            with open("output.mp3", "rb") as file:
                audio_data = file.read()
    
            # Use Streamlit to play the audio
            st.audio(audio_data, format="audio/mp3", autoplay=True)
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                st.markdown(message["content"])
       
# Welcome to Streamlit!

#Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
#If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
#forums](https://discuss.streamlit.io).

#In the meantime, below is an example of what you can do with just a few lines of code:
