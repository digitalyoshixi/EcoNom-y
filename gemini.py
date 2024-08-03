import google.generativeai as genai
import os
import PIL.Image

class GeminiAPI():
    def __init__(self, key):
        self.key = key
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def resimg(self, prompt, img):
        # assuming imgobj is created like img = PIL.Image.open('image.jpg')
        response = self.model.generate_content([prompt, img])
        print(response)

    def restxt(self, prompt):
        response = self.model.generate_content(prompt)
        print(response)


if __name__ == "__main__":
    from dotenv import load_dotenv    
    
    # Load environment variables from .env
    load_dotenv()
    
    gemini_api = GeminiAPI(os.environ["GOOGLE_GEMINI_API_KEY"])

    testimg = PIL.Image.open('testgemini.png')
    gemini_api.resimg(testimg,"what do u think about this?")
