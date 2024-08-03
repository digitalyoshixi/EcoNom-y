import google.generativeai as genai
import os
    

class GeminiAPI():
    def __init__(self, key):
        self.key = key
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def resimg(self, imgobj):
        print("")

    def restxt(self, text):
        response = self.model.generate_content(text)
        print(response)


if __name__ == "__main__":
    from dotenv import load_dotenv    
    load_dotenv()
    key = os.environ["GOOGLE_API_KEY"]
    geminiapi = GeminiAPI(key)
    geminiapi.restxt("can u twerk")
