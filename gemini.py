import google.generativeai as genai
import os
from PIL import Image, ImageFile

class GeminiAPI():
    def __init__(self, api_key: str) -> None:
        # Configure Gemini with API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def resimg(self, prompt: str, img: ImageFile) -> str:
        """
        Sends an image object and prompt to Google Gemini, returns the response.
        
        Parameters:
            prompt: The prompt to send Gemini.
            imgobj: An image object given by PIL.Image.open
        """
        # assuming imgobj is created like img =('image.jpg')
        response = self.model.generate_content([prompt, img])
        
        return response.text

    def restxt(self, prompt):
        response = self.model.generate_content(prompt)
        print(response)


if __name__ == "__main__":
    from dotenv import load_dotenv    
    
    # Load environment variables from .env
    load_dotenv()
    
    gemini_api = GeminiAPI(os.environ["GOOGLE_GEMINI_API_KEY"])

    testimg = Image.open('testgemini.png')
    response = gemini_api.resimg(testimg,"what do u think about this?")
    print(response)
