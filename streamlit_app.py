import streamlit as st
from elevenlabs import play, stream
from elevenlabs.client import ElevenLabs
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import ffmpeg
import base64
from pydub import AudioSegment
from pydub.playback import play
import io



os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
client = ElevenLabs(
    api_key= st.secrets["EL_KEY"]
    )


#with st.form('inputs'):
#    OAI_Key = st.text_input('OpenAI-Key', 'Hier OPEN-AI API Key einfuegen')
#    EL_Key = st.text_input('Elevenlabs-Key','Hier Elevenlabs API Key einfuegen')
#    submitAPI = st.form_submit_button ('OK')
#    if submitAPI:



st.title('MEM-Bot')

with st.form('my form'):
    text = st.text_area('Enter text:', placeholder='Frage stellen')
    submitted = st.form_submit_button('Submit')
    if submitted:
        reader = SimpleDirectoryReader(input_dir="data", recursive=True)
        documents = reader.load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(str(text))
        print(response)
        st.text(response)

        audio = client.generate(
            text=str(response),
            voice = "Rachel",
            model = "eleven_multilingual_v2",
        )
        song = AudioSegment.from_file(audio, format="mp3")
        play(song)
       
# Welcome to Streamlit!

#Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
#If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
#forums](https://discuss.streamlit.io).

#In the meantime, below is an example of what you can do with just a few lines of code:
