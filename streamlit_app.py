import streamlit as st
from elevenlabs import play, stream
from elevenlabs.client import ElevenLabs
import os
import ffmpeg
os.environ['OPENAI_API_KEY'] = ""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
client = ElevenLabs(
    api_key=""
)
st.title('MEM-Bot')
with st.form('my form'):
    text = st.text_area('Enter text:', 'Hier Anfrage zum MEM-Studiengang stellen')
    submitted = st.form_submit_button('Submit')
    if submitted:
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(text)
        st.text_area('Output:', response)
        audio = client.generate(
            text=str(response),
            voice = "Rachel",
            model = "eleven_multilingual_v2",
        )
        stream (audio)

# Welcome to Streamlit!

#Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
#If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
#forums](https://discuss.streamlit.io).

#In the meantime, below is an example of what you can do with just a few lines of code:
