import google.generativeai as genai
import os
    

class GeminiAPI():
    def __init__(self, key):
        self.key = key
    
    def recimg(self, imgobj):
        GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)


if __name__ == "__main__":
    from dotenv import load_dotenv    
    load_dotenv()
    key = os.environ["GOOGLE_API_KEY"]
    geminiapi = GeminiAPI(key)
