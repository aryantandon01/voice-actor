from flask import Flask, render_template, request, send_file
from gtts import gTTS
from transformers import pipeline
from pydub import AudioSegment
import os
#fewr 
app = Flask(__name__)

# Initialize a text-generation pipeline (using GPT-2 as an example)
text_generator = pipeline("text-generation", model="gpt2")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get user inputs
    script = request.form['script']
    style = request.form['style']
    
    # Generate or enhance script (optional)
    if style == "expand":
        script = text_generator(script, max_length=100, num_return_sequences=1)[0]['generated_text']
    
    # Convert text to speech
    tts = gTTS(script, lang='en')
    audio_file = "static/output.mp3"
    tts.save(audio_file)
    
    # Add optional background music (basic example)
    if request.form.get('music') == "yes":
        bg_music = AudioSegment.from_file("static/background.mp3")
        voiceover = AudioSegment.from_file(audio_file)
        combined = voiceover.overlay(bg_music)
        combined.export(audio_file, format="mp3")
    
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
