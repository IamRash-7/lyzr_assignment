from lyzr import ChatBot, VoiceBot
from config import WEAVIATE_API_KEY, WEAVIATE_URL, OPENAI_API_KEY

voicebot_manager = VoiceBot(api_key=OPENAI_API_KEY)


######################################
# ADDITIONAL - YOUTUBE CHATBOT

chatbot_manager = None
def initialize_chatbot(urls):
    vector_store_params = {
        "vector_store_type": "WeaviateVectorStore",
        "url": WEAVIATE_URL,
        "api_key": WEAVIATE_API_KEY,
        "index_name": "Youtube"
    }

    global chatbot_manager
    chatbot_manager = ChatBot.youtube_chat(
        urls=urls,
        vector_store_params=vector_store_params
    )