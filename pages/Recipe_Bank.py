import streamlit as st
import random
from utils.recipes import AllRecipesAPI

@st.dialog("Add a new recipe!")
def addNewRecipe():
    recipeName = st.text_input("Recipe Name:")
    if recipeName is not None:
    #Search for the recipe
        all_recipes_api = AllRecipesAPI()
        search_response = all_recipes_api.search_recipe("recipeName")

        first_result = search_response[0]
        recipe_name = first_result["name"]
        recipe_url = first_result['url']
        recipe_rating = first_result['rate']
        recipe_image = first_result['image']

        print(first_result)
        print(f"{recipe_name=}, {recipe_url=}, {recipe_rating=}, {recipe_image=}")

        recipe_information = all_recipes_api.get_recipe(first_result['url'])
        print(recipe_information)
    

@st.dialog("Here's a new recipe!")
def recommendRecipe():
    pass

@st.dialog("Lets do this!")
def makeTheMeal(recipeName, ingredients):
    st.title(recipeName)
    st.write(ingredients)
    st.button("Made the Meal!", type = "primary")

col1, col2 = st.columns(2)
with col1:
    if st.button("Add Recipe", type = "primary"):
        addNewRecipe()
with col2:
    if st.button("Recommend Recipe", type = "primary"):
        recommendRecipe()

container = st.container(border = True)
with container:
    with st.container():
        meals = ["https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=600"]
        for i in range(len(meals)):
            st.image(meals[i], use_column_width = "always")
            st.button("Make Now", on_click = makeTheMeal, key= random.randint(1,10000000), use_container_width=True, args=("apple","banana"))



# with container:
#     col1, col2 = st.columns(2)
#     with col1:
#         with st.container():
#             meals = ["https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.pexels.com/photos/958545/pexels-photo-958545.jpeg?auto=compress&cs=tinysrgb&w=600"]
#             for i in range(len(meals)):
#                 image = Image.open(urlopen(meals[i]))
#                 new_image = image.resize((600, 400))
#                 st.image(new_image)
#                 st.button("Make Now", on_click = addNewRecipe, key= random.randint(1,10000000), use_container_width=True)
#     with col2:
#         with st.container():
#             meal = ["https://images.pexels.com/photos/1640774/pexels-photo-1640774.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.pexels.com/photos/699953/pexels-photo-699953.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.pexels.com/photos/1633525/pexels-photo-1633525.jpeg?auto=compress&cs=tinysrgb&w=600"]
#             for i in range(len(meals)):
#                 image = Image.open(urlopen(meal[i]))
#                 new_image = image.resize((600, 400))
#                 st.image(new_image)
#                 st.button("Make Now", on_click=addNewRecipe, key= random.randint(1,100000000), use_container_width=True)
