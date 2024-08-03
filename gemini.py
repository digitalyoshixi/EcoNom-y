import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
key = os.environ["GOOGLE_API_KEY"]
print(key)


# GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)


def imagenanalysis(inp):
    print("balls")

def textanalysis(inp):
    print("balls")