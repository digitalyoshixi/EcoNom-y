import streamlit as st
import random
import math
from utils.database import get_supabase_api
from utils.recipes import AllRecipesAPI
from utils.auth import require_auth, is_logged_in
from utils.sidebar import show_sidebar
from utils.gemini import get_gemini_api

show_sidebar()

# Initialize APIs
require_auth()
supabaseAPI = get_supabase_api()
all_recipes_api = AllRecipesAPI()
gemini = get_gemini_api()

def display_recipe_info(recipe_information, recipe_image, recipe_rating):
    st.title(recipe_information["name"])
    st.image(recipe_image, use_column_width="always")

    with st.container():
        if recipe_rating:
            rating = ":star:" * math.floor(recipe_rating)
            st.write(f"Rating: {rating}")

    st.subheader("Ingredients")
    ingredients = recipe_information["ingredients"]
    ingredients_list = "\n\n".join(
        [f"{i + 1}. {ingredient}" for i, ingredient in enumerate(ingredients)]
    )
    st.write(ingredients_list)

    st.subheader("Steps")
    for i, step in enumerate(recipe_information["steps"]):
        st.write(f"{i + 1}. {step['task']}\n\n")
        if "picture" in step:
            st.image(step["picture"], use_column_width="always")

    return ingredients


def add_recipe_to_db(
    recipe_name, supabase_ingredients_list, recipe_image, recipe_url, username
):
    supabaseAPI.add_recipe(
        recipe_name,
        supabase_ingredients_list,
        recipe_image,
        100,
        recipe_url,
        username,
    )

import re

def multiply_numbers(string, multiplier):
    # Function to multiply a matched number by 2
    def double(match):
        return str(float(match.group()) * multipler)
    
    # Use regex to find all numbers and replace them with their doubled value
    return re.sub(r'\d+', double, string)




@st.dialog("Add a new recipe!")
def add_new_recipe():
    recipe_name = st.text_input("Recipe Name:")
    if recipe_name:
        search_response = all_recipes_api.search_recipe(recipe_name)
        if not search_response:
            st.error("Please try again")
            return

        first_result = search_response[0]
        recipe_information = all_recipes_api.get_recipe(first_result["url"])

        ingredients = display_recipe_info(
            recipe_information, first_result["image"], first_result["rate"]
        )
        ingredients_string = ", ".join(ingredients)

        with st.expander("Not happy with the ingredients?"):
            st.write("Previous ingredients")
            ingredients_string = st.text_input(
                value=ingredients_string, label="Change them here:"
            )
            # Apply multiplier effect
            muliplierframe = supabaseAPI.selectspecific(
                "recipes", "portionMultiplier", "recipeURL", first_result["url"]
            )
            multipler = 1
            if len(muliplierframe.data) != 0:
                multiplier = float(muliplierframe.data[0]["portionMultiplier"])/100 
            
            ingredients = multiply_numbers(ingredients_string, multiplier).split(",")
            # PROMPT = f"apply a {multiplier}x multiplier to each item quantity in the list and return them in JSON format. Dont give me any other text: {ingredients_string}"
            # resp = gemini.text_response(f"multiply all ingredients by {multiplier}x: {ingredients_string}")
            # print(resp)
            ingredients = ingredients_string.split(",")

        st.write("URL: ", first_result["url"])

        if st.button("Add this Recipe!", type="primary"):
            if not supabaseAPI.selectspecific(
                "recipes", "recipeURL", "recipeURL", first_result["url"]
            ).data:
                # get username from webtoken
                username = is_logged_in()
                add_recipe_to_db(
                    first_result["name"],
                    ingredients,
                    first_result["image"],
                    first_result["url"],
                    username,
                )
                st.session_state.urls.append(first_result["url"])
                st.session_state.images.append(first_result["image"])
            st.rerun()


@st.dialog("Here's a new recipe!")
def recommend_recipe():
    search_response = all_recipes_api.random_recipes()
    if not search_response:
        st.error("No recipes found.")
        return

    first_result = search_response[0]
    recipe_information = all_recipes_api.get_recipe(first_result["url"])

    ingredients = display_recipe_info(
        recipe_information, first_result["image"], first_result["rate"]
    )
    ingredients_string = ", ".join(ingredients)

    with st.expander("Not happy with the ingredients?"):
        st.write("Previous ingredients")
        ingredients_string = st.text_input(
            value=ingredients_string, label="Change them here:"
        )
        
        ingredients = ingredients_string.split(",")

    st.write("URL: ", first_result["url"])

    if st.button("Add this Recipe!", type="primary"):
        if not supabaseAPI.selectspecific(
            "recipes", "recipeURL", "recipeURL", first_result["url"]
        ).data:
            add_recipe_to_db(
                first_result["name"],
                ingredients,
                first_result["image"],
                first_result["url"],
            )
            st.session_state.urls.append(first_result["url"])
            st.session_state.images.append(first_result["image"])
        st.rerun()


@st.dialog("Let's do this!")
def make_the_meal(recipe_url, recipe_image_url):
    recipe_information = all_recipes_api.get_recipe(recipe_url)
    display_recipe_info(
        recipe_information, recipe_image_url, recipe_information.get("rate")
    )

    if st.button("Made the Meal!", type="primary"):
        st.subheader("Rate Your Meal!")
        feedback_options = [
            "way too little food! 😔",
            "not enough food but it's manageable.",
            "the perfect amount of food! 😁",
            "a little too much food.",
            "way too much food 😡",
        ]
        feedback = st.selectbox(
            "How filling was the meal for your family?", feedback_options
        )

        if feedback:
            old_value = supabaseAPI.selectspecific(
                "recipes", "portionMultiplier", "recipeURL", recipe_url
            ).data[0]["portionMultiplier"]
            supabaseAPI.update_cell(
                "recipes",
                "portionMultiplier",
                old_value,
                "portionMultiplier",
                old_value + 1,
            )
            feedback_index = feedback_options.index(feedback)
            if feedback_index == 0:
                supabaseAPI.update_cell(
                    "recipes",
                    "portionMultiplier",
                    old_value + 30,
                    "recipeURL",
                    recipe_url,
                )


def remove_recipe(recipe_url, recipe_image):
    st.session_state.urls.remove(recipe_url)
    st.session_state.images.remove(recipe_image)


def main():
    st.title("Meal Planner")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add Recipe", type="primary", use_container_width=True):
            add_new_recipe()
    with col2:
        if st.button("Recommend Recipe", type="primary", use_container_width=True):
            recommend_recipe()

    container = st.container()
    if "urls" not in st.session_state:
        st.session_state.urls = []
        st.session_state.images = []

    for i, (url, image) in enumerate(
        zip(st.session_state.urls, st.session_state.images)
    ):
        container.image(image, use_column_width="always")
        col1, col2 = container.columns(2)
        with col1:
            container.button(
                "Make Now",
                on_click=make_the_meal,
                key=random.randint(1, 10000000),
                use_container_width=True,
                type="primary",
                args=(url, image),
            )
        with col2:
            container.button(
                "Remove Recipe",
                on_click=remove_recipe,
                use_container_width=True,
                args=(url, image),
                key=random.randint(1, 1000000),
            )

    if not st.session_state.urls:
        st.write(":eyes: It's empty here... Add your first recipe to get started!")


if __name__ == "__main__":
    main()
