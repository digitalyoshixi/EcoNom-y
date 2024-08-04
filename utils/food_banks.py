import requests
import streamlit as st
import pandas as pd


class FoodBanks:
    def __init__(self):
        self.session = requests.Session()

    def locate_food_banks(self, location: str) -> dict:
        response = requests.post(
            'https://www.dailybread.ca/wp-content/plugins/lb-0-dailybread2023/shortcode-map-ajax.php',
            headers={
                "Referer": "https://www.dailybread.ca/need-food/programs-by-location/"},
            data={
                "loc": location,
                "mode": "driving,transit,walking",
                "ref": "1"},
        )

        json_response = response.json()

        # Convert entire food bank database to dictionary
        food_banks = {}
        for food_bank in json_response['aall']:
            food_banks[food_bank['nrow']] = food_bank

        closest_food_banks = []
        for food_bank in json_response['aclosest']:
            food_bank_id = food_bank["nrow"]
            food_bank_information = food_banks[food_bank_id]

            # Add distance from location
            food_bank_information["distance"] = food_bank["ndist_est"]
            food_bank_information["km_distance"] = food_bank["cdist"]

            # Append food bank to closest food banks list
            closest_food_banks.append(food_bank_information)

        closest_food_banks.sort(key=lambda food_bank: food_bank['distance'])

        loc_lat, loc_long = json_response['flat'], json_response['flng']

        return {
            "location": {
                "lat": loc_lat,
                "long": loc_long},
            "closest_food_banks": closest_food_banks}


if __name__ == "__main__":
    food_banks = FoodBanks()
    query = food_banks.locate_food_banks("Toronto Metropolitian University")
    print(
          query['closest_food_banks'][0])

