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
    load_dotenv()
    key = os.environ["GOOGLE_API_KEY"]
    geminiapi = GeminiAPI(key)
    testimg = PIL.Image.open('testgemini.png')
    geminiapi.resimg(testimg,"what do u think about this?")
