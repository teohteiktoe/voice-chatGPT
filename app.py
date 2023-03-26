#!/usr/bin/env python
# coding: utf-8

# In[5]:


from flask import Flask, request, render_template
import openai
import os 
import json


# Set up Flask app
app = Flask(__name__)

# Set OpenAI API key and model
openai.api_key = os.getenv('openai-key')

from google.cloud import speech_v1p1beta1 as speech

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_info(json.loads('/etc/secrets/gcred'))


client = speech.SpeechClient(credentials=credentials)

# Set up OpenAI input prompt
input_prompt = "Convert sound to text:"

#Define function to generate text from sound
def generate_text_from_sound(audio_file):
    #audio_file = open('audio_file.wav', 'rb').read()
    audio = speech.RecognitionAudio(content=audio_file)
    config = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        language_code='en-US'
    )
    response = client.recognize(config=config, audio=audio)
    #print(response)
    
    for result in response.results:
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
        r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", 
            "content": result.alternatives[0].transcript}],)
        text_output = r["choices"][0]["message"]["content"]
        return text_output

    
# Define Flask route for home page
@app.route("/")
def home():
    return render_template("index.html")

# Define Flask route for generating text from sound
@app.route("/sound-to-text", methods=["POST"])
def sound_to_text():
    audio_file = request.files["file"].read()
    audio_filename = "audio_file.mp3"
    with open(audio_filename, "wb") as f:
        f.write(audio_file)
    text_output = generate_text_from_sound(audio_file)
    if text_output:
      return text_output
    return "no sound captured"

# Run Flask app
if __name__ == "__main__":
    app.config['WTF_CSRF_SECRET_KEY'] = '12345678ertyu'
    app.run()


# In[ ]:




