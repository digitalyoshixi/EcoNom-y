import streamlit as st
import pandas as pd
from utils.food_banks import FoodBanks

food_banks = FoodBanks()


def receive_address(address):
    query = food_banks.locate_food_banks(address)

    closest_food_banks = query["closest_food_banks"]
    location = query["location"]

    if not closest_food_banks:
        return st.error("No food banks found. Please refine your query.")

    latitudes = []
    longitudes = []
    colours = []

    # Extract data for the table
    table_data = []
    for food_bank in closest_food_banks:
        latitudes.append(food_bank["flat"])
        longitudes.append(food_bank["flng"])
        colours.append("#ff000088")
        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={food_bank['flat']},{food_bank['flng']}"
        table_data.append(
            {
                "Distance": food_bank["km_distance"],
                "Name": food_bank["cname"],
                "Address": f'<a href="{google_maps_link}" target="_blank">{food_bank["caddress"]}</a>',
            }
        )

    latitudes.append(location["lat"])
    longitudes.append(location["long"])
    colours.append("#0000ff88")

    map_df = pd.DataFrame(
        {"latitudes": latitudes, "longitudes": longitudes, "colours": colours}
    )

    # Create the map and address columns
    col1, col2 = st.columns([3, 1])

    # Display the map
    col1.map(
        map_df, latitude="latitudes", longitude="longitudes", color="colours", zoom=13
    )

    # Create a DataFrame for the table and display it
    table_df = pd.DataFrame(table_data)

    col2.container.height(200)
    col2.write(table_df)

    # Custom CSS to left-align table headers
    st.markdown(
        """
    <style>
        th {
            text-align: left !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Display the table with clickable links
    st.subheader("Closest Food Banks")
    st.markdown(table_df.to_html(escape=False), unsafe_allow_html=True)


st.title("Food Banks Nearby")
st.subheader("Donate unwanted ingredients")

# Input for user to enter their location
address = st.text_input("Enter your location:")

# Button to submit the location
if st.button("Submit"):
    if address:
        receive_address(address)
    else:
        st.error("Please enter a valid address.")
