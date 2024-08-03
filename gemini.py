import google.generativeai as genai
import os
from PIL import Image, ImageFile

class GeminiAPI():
    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def resimg(self, prompt: str, img: ImageFile) -> str:
        """
        Sends an image object and prompt to Google Gemini, returns the response.
        
        Parameters:
            prompt: The prompt to send Gemini.
            imgobj: An image object given by PIL.Image.open
        """
        response = self.model.generate_content([prompt, img])
        return response.text

    def restxt(self, prompt: str) -> str:
        """
        Sends a prompt to Google Gemini, returns the response.

        Parameters:
            prompt: The prompt to send Gemini.
        """
        response = self.model.generate_content(prompt)
        return response.text


if __name__ == "__main__":
    from dotenv import load_dotenv    
    
    # Load environment variables from .env
    load_dotenv()
    
    gemini_api = GeminiAPI(os.environ["GOOGLE_GEMINI_API_KEY"])

    testimg = Image.open('testgemini.png')
    response = gemini_api.resimg(testimg,"what do u think about this?")
    print(response)
