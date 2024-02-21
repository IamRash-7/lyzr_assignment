from flask import Blueprint, request, render_template
from app.chatbot_config import initialize_chatbot
from app import UPLOAD_FOLDER
import os

api_blueprint = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'mp3'}

@api_blueprint.route('/', methods=['GET'])
def home():
    return {"Message":"Welcome to the app"}

# MP3 TO TEXT

# Check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text using VoiceBot
def extract_text(file_path):
    from app.chatbot_config import voicebot_manager
    transcript = voicebot_manager.transcribe(file_path)
    return transcript

# Save and delete the uploaded file
def save_and_extract_data(mp3_file):
    file_path = os.path.join(UPLOAD_FOLDER, mp3_file.filename)
    mp3_file.save(file_path)

    text_result = extract_text(file_path)

    os.remove(file_path)

    return text_result

# API Endpoint
@api_blueprint.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('upload.html', error='No selected file')
        
        if not allowed_file(file.filename):
            return render_template('upload.html', error='Invalid File Type')

        if file:
            try:
                text_result = save_and_extract_data(file)
            except:
                return render_template('upload.html', error='Error in initialization of Voicebot')
            return render_template('upload.html', text_result=text_result)

    return render_template('upload.html')

##########################################
# ADDITIONAL
# YOUTUBE CHATBOT

VIDEO_LINK = None

@api_blueprint.route('/youtube_chatbot', methods=['POST', 'GET'])
def ask_question():
    if request.method == 'POST':
        video_link = [request.form.get('video_link')]
        question = request.form.get('question')

        if not video_link or not question:
            return render_template('youtube_chatbot.html', error='Please provide both video link and question.')
        
        try:
            global VIDEO_LINK
            if(VIDEO_LINK != video_link):
                VIDEO_LINK = video_link
                chatbot_manager = initialize_chatbot(VIDEO_LINK)
        except:
            return render_template('youtube_chatbot.html', error='Error while Intializing')
        
        try:
            from app.chatbot_config import chatbot_manager
            chatbot_response = chatbot_manager.chat(question)
        except:
            return render_template('youtube_chatbot.html', error='Error while chat')
        
        return render_template('youtube_chatbot.html', chatbot_response=chatbot_response)
        
    
    return render_template('youtube_chatbot.html')