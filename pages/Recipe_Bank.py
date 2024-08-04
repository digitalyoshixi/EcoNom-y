#all imports
import streamlit as st
import random
from utils.recipes import AllRecipesAPI

#setting up subabase API
from utils.database import get_supabase_api
supabaseAPI = get_supabase_api()


all_recipes_api = AllRecipesAPI()


#function used to add a new recipe to the user's recipe bank
@st.dialog("Add a new recipe!")
def addNewRecipe():
    recipeName = st.text_input("Recipe Name:")
    
    if recipeName is not None:
        #Search for the recipe
        search_response = all_recipes_api.search_recipe(recipeName)

        if (recipeName != ""):
            try:
                first_result = search_response[0]
            except:
                pass
            recipe_name = first_result["name"]
            recipe_url = first_result['url']
            recipe_rating = first_result['rate']
            recipe_image = first_result['image']
            recipe_information = all_recipes_api.get_recipe(first_result['url'])

            st.title(recipe_name)
        
            st.image(recipe_image, use_column_width = "always")
            
            with st.container():
                if recipe_rating != None:
                    rating = ""
                    try:
                        for i in range(recipe_rating):
                            rating += ":star:"
                        st.write("Rating: " + rating)
                    except:
                        pass
            
            supabaseIngredientsList = []

            with st.container():
                st.subheader("Ingredients: ")
                ingredientsList = ""
                for i in range(len(recipe_information["ingredients"])):
                    supabaseIngredientsList.append(recipe_information["ingredients"][i])
                    ingredientsList += str(i+1) + ". " + recipe_information["ingredients"][i] + "\n\n"
                st.write(ingredientsList)

            ingredientsString = ", ".join(supabaseIngredientsList)
            
            with st.expander("Not happy with the ingredients?"):
                st.write("previous ingredients")
                ingredientsList = st.text_input(value = ingredientsString, label="Change them here: ")
                supabaseIngredientsList = ingredientsList.split(",")


            with st.container():
                st.subheader("Steps")
                for i in range(len(recipe_information["steps"])):
                    st.write(str(i+1) + ". " + recipe_information["steps"][i]["task"] + "\n\n")
                    if "picture" in recipe_information["steps"][i]:
                        st.image(recipe_information["steps"][i]['picture'], use_column_width = "always")
                
            st.write("URL: ", recipe_url)

            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                makeThis = st.button("Make this Recipe!", type="primary")
                if makeThis:
                   container.image(recipe_image, use_column_width = "always")
            with col2:
                add = st.button("Add this Recipe!", type="primary")

                #checks if user already added this recipe
                if add:
                    if supabaseAPI.selectspecific("recipes", "recipeURL", "recipeURL", recipe_url).count:
                        st.write("This recipe has already been added.")
                    else:
                        supabaseAPI.add_recipe(recipe_name, {"ingredients": supabaseIngredientsList}, recipe_image, 1, recipe_url)
                        st.session_state.recipes.append(recipe_image)
                        st.session_state.urls.append(recipe_url)
                        st.session_state.images.append(recipe_image)
                        st.rerun()

#function that recommends the user a new recipe 
@st.dialog("Here's a new recipe!")
def recommendRecipe():
    search_response = all_recipes_api.random_recipes()

    try:
        first_result = search_response[0]
    except:
        pass

    recipe_name = first_result["name"]
    recipe_url = first_result['url']
    recipe_rating = first_result['rate']
    recipe_image = first_result['image']
    recipe_information = all_recipes_api.get_recipe(first_result['url'])

    #checks if the random recipe already exists
    if supabaseAPI.selectspecific("recipes", "recipeURL", "recipeURL", recipe_url).count:
        st.rerun()

    st.title(recipe_name)

    st.image(recipe_image, use_column_width = "always")
    
    with st.container():
        if recipe_rating != None:
            rating = ""
            try:
                for i in range(recipe_rating):
                    rating += ":star:"
                st.write("Rating: " + rating)
            except:
                pass

    supabaseIngredientsList = []

    with st.container():
        st.subheader("Ingredients: ")
        ingredientsList = ""
        for i in range(len(recipe_information["ingredients"])):
            supabaseIngredientsList.append(recipe_information["ingredients"][i])
            ingredientsList += str(i+1) + ". " + recipe_information["ingredients"][i] + "\n\n"
        st.write(ingredientsList)

    ingredientsString = ", ".join(supabaseIngredientsList)
            
    with st.expander("Not happy with the ingredients?"):
        st.write("previous ingredients")
        ingredientsList = st.text_input(value = ingredientsString, label="Change them here: ")
        supabaseIngredientsList = ingredientsList.split(",")

    with st.container():
        st.subheader("Steps")
        steps = ""
        for i in range(len(recipe_information["steps"])):
            st.write(str(i+1) + ". " + recipe_information["steps"][i]["task"] + "\n\n")
            if "picture" in recipe_information["steps"][i]:
                st.image(recipe_information["steps"][i]['picture'], use_column_width = "always")
        
    st.write("URL: ", recipe_url)
    print(recipe_name)

    col1, col2 = st.columns(2)
    with col1:
        makeThis = st.button("Make this Recipe!", type="primary")
        if makeThis:
            container.image(recipe_image, use_column_width = "always")
    with col2:
        add = st.button("Add this Recipe!", type="primary")
        if add:
            supabaseAPI.add_recipe(recipe_name, {"ingredients": supabaseIngredientsList}, recipe_image, 1, recipe_url)
            st.session_state.recipes.append(recipe_image)
            st.session_state.urls.append(recipe_url)
            st.session_state.images.append(recipe_image)
            print(recipe_name)
            st.rerun()

@st.dialog("Lets do this!")
def makeTheMeal(recipeURL, recipeImageURL):
    search_response = all_recipes_api.get_recipe(recipeURL)
    print(search_response)
    recipe_name = search_response["name"]

    st.title(recipe_name)
    st.image(recipeImageURL, use_column_width = "always")
    
    with st.container():
        st.subheader("Ingredients: ")
        ingredientsList = ""
        for i in range(len(search_response["ingredients"])):
            ingredientsList += str(i+1) + ". " + search_response["ingredients"][i] + "\n\n"
        st.write(ingredientsList)

    with st.container():
        st.subheader("Steps")
        steps = ""
        for i in range(len(search_response["steps"])):
            st.write(str(i+1) + ". " + search_response["steps"][i]["task"] + "\n\n")
            if "picture" in search_response["steps"][i]:
                st.image(search_response["steps"][i]['picture'])

    st.write("URL: ", recipeURL)
    
    st.button("Made the Meal!", type = "primary")

col1, col2 = st.columns(2, gap="large")
with col1:
    if st.button("Add Recipe", type = "primary"):
        addNewRecipe()
with col2:
    if st.button("Recommend Recipe", type = "primary"):
        recommendRecipe()

container = st.container(border = True)
with container:
    if "recipes" not in st.session_state:
        st.session_state.recipes = []
        st.session_state.urls = []
        st.session_state.images = []

    for i in range(len(st.session_state.recipes)):
        container.image(st.session_state.recipes[i], use_column_width = "always")
        container.button("Make Now", on_click = makeTheMeal, key= random.randint(1,10000000), use_container_width=True, args=(st.session_state.urls[i],st.session_state.images[i]))

    if len(st.session_state.recipes) == 0:
        st.write(":eyes:" + " Its empty here... Add your first recipe to get started!")