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
openai.api_key = "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"

from google.cloud import speech_v1p1beta1 as speech

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_info({
  "type": "service_account",
  "project_id": "learn-terraform-in-gcp-379009",
  "private_key_id": "d25af69f617f30ec46ba00fb30955a76f1eb2d11",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCerbeY/sIFRspK\nvOruY+cesTSu0ur3kr9Y13cOqSE3nM1oL/zWranj6iqjhQorjiAg1yf1R+xLn5pJ\nf97wzlCR6q1DsvQh4A1XvcFMJEYtXTO7hbtoCJAF/E75FjLzrehIZCvGkc2T7gHQ\nKsvmgs7CTA7kGvB79+0oEaRjo+8DPDCnTQR2NfZB4eeA5bvMWmLEZ4pDO0czD/3s\nui7Led/GpMq5OrMPXnjgouqWbj1ZPyouAk/I14VAPBoULYxRfRq0cON4XSH+dP9r\neLJPiYOigsPeUomKA8aYBKuYSp5VIjQSm8EvQEKtfJjuyJWKf1ZL0gVX8tcjDaS5\n4QfjGf7ZAgMBAAECggEABPVox18usPuFVtCQhuKYVl0zSENPFG2BjUUuc0bVwucj\nhB37yLmklXq72mBN8Q5/8obGuOOGftZ9+84DKYNJAUZUI8lz15soz5UedUKs7r36\n3+FN+fJKjeVUknQfI35Lw/ddZtcnlXfalqa/uHReAbRewsIUwcr9nkLu4C4/SdqL\nCafgYf96lZOygHhY87ZmTl10EgYg0eW7tKM4i8hBH8YqR90pjtzz8IqDtPZpDb4V\ndRSHCoxI3hceLZtBWYEa0upFGmH0GVou4D+bns8wYea9Nj68mIlu1aAYJzwpScgc\nRGccjS1QHHweKq+Rbx1J6+5rdG3YjJyyBofdF82AAQKBgQDYfwBVymwqGf56c+07\n54wJE+AZtBD2naxwfoNiOhnysjQNuQBqBoV1YRXsOluHmqDYKp1/dBmju5X4PypU\n3V1Wk7itE/o9wmv+Z9wIVdGILsBmqUA1AaoXMMbnD21quBxhMwceyHBctpF+u/Dv\nZGcBMOQgy/Yt6HVt/KF8/x4x7QKBgQC7oe9tb845hhpqh51SYuMZGA8in+P1lJHa\nIlkmsUZQE4d7P0wbiAipz752bM71ObnrniVMclN0OKaZPdVY29E5oBU1z4EU0j/5\ntc0uLF4VUN55lZP5n5jDhWALnlMi3tkRTyiD3ZQ8vWPFWSAiUEEz8+L4MNMJ6/Bi\nVgMW7qjTHQKBgC75f40d2tJXyYuwU61H1G6zzVBGbdfU5nGSQdeyW6b5W6oOljRr\nLdIGOseC8hE+T+AXfw0El/ua3DN9ISZA0dvTOaL0TrvPz7bnuipk1I4D9uNPngri\nTZGyl7XS9x7My/ubItRfEWJMis1A4kpPMrpjbVxgZQ4Y/kHbKv8ALAERAoGAXK5c\nif4UK63mFoDuYOefraGIuF2qSIAem1UkHEysoplC7soRWfgT721Cc1TD1bWx9ISl\nf+Fo/5uMD13PqJjL/F7qmy3oYNSJ7Vq0Av6/amALxJryAPeoicuz6YlHH45cQoSL\nSreEpYwXYD/p84kY7ASoNFhJpjj5AFnkJMu2cLECgYAVKokDiw07Yts6v+anjBhQ\nUx3raxc+vMXhQr0jlCpHM1EjHIdFM+fYUNy7cKUjAGJCRg16qR1FTq0CijowvW56\nzzTjrIFJM5K1NB4P/iRO/Jdc5VhKCQnsDMI/QWmuGTSvXkZ4DkwCZJEzxVLp88kV\nV0bEPeucMV0xSAttzCzltQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "cloud-speed@learn-terraform-in-gcp-379009.iam.gserviceaccount.com",
  "client_id": "107857206846080315893",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-speed%40learn-terraform-in-gcp-379009.iam.gserviceaccount.com"
})

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




