import PIL
import json_repair
from gemini import GeminiAPI

# IMAGE_PROMPT = """Parse this receipt for cooking ingredients and return
# the contents in JSON format. Ignore ALL non-food items.

# [
#     {
#         "ingredient": "Cabbage",
#         "quantity": "1"
#     },
#     {
#         "ingredient": "...",
#         "quantity": "#"
#     }
# ]"""

IMAGE_PROMPT = "What do you see?"


class ReceiptParser:
    gemini_api: GeminiAPI

    def __init__(self, gemini_api_key: str):
        self.gemini_api = GeminiAPI(gemini_api_key)

    def parse_receipt(self, receipt: PIL.ImageFile) -> list[dict[str, str]]:
        """
        Sends a receipt to Google Gemini, returns the parsed data.

        Parameters:
            recipt: An image object given by PIL.Image.open.
        """
        response = self.gemini_api.image_response(
            prompt=IMAGE_PROMPT, image=receipt)

        return json_repair.loads(response)


if __name__ == "__main__":
    import load_env
    import os

    receipt_parser = ReceiptParser(os.environ["GOOGLE_GEMINI_API_KEY"])

    import requests
    from PIL import Image
    from io import BytesIO

    response = requests.get("https://i.redd.it/kp1udlgk5zv91.jpg")

    image = Image.open(BytesIO(response.content))

    parsed_receipt = receipt_parser.parse_receipt(image)
    print(parsed_receipt)
