import streamlit as st
from elevenlabs import play, stream, save
import elevenlabs
from elevenlabs.client import ElevenLabs
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import ffmpeg
import base64

import io




initialize = True
os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
client = ElevenLabs(
    api_key= st.secrets["EL_KEY"]
    )


#with st.form('inputs'):
#    OAI_Key = st.text_input('OpenAI-Key', 'Hier OPEN-AI API Key einfuegen')
#    EL_Key = st.text_input('Elevenlabs-Key','Hier Elevenlabs API Key einfuegen')
#    submitAPI = st.form_submit_button ('OK')
#    if submitAPI:



st.title('MEM-Bot 1.0')
CHUNK_SIZE = 1024
with st.form('my form'):
    activetts = st.toggle("Read answer")
    text = st.text_area('Enter text:', placeholder='Frage stellen')
    submitted = st.form_submit_button('Submit')
    if submitted:
        if initialize:
            reader = SimpleDirectoryReader(input_dir="data", recursive=True)
            documents = reader.load_data()
            index = VectorStoreIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            initialize = False
        response = query_engine.query(str(text))
        print(response)
        st.text(response)
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
       
# Welcome to Streamlit!

#Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
#If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
#forums](https://discuss.streamlit.io).

#In the meantime, below is an example of what you can do with just a few lines of code:
