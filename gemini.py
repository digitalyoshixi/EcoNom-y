import google.generativeai as genai

from google.colab import userdata
GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def imagenanalysis(inp):
    print("balls")

def textanalysis(inp):
    print("balls")