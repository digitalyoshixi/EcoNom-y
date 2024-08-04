import streamlit as st
import random
from utils.database import get_supabase_api
from utils.recipes import AllRecipesAPI
from utils.show_sidebar import show_sidebar

show_sidebar()

supabaseAPI = get_supabase_api()
all_recipes_api = AllRecipesAPI()


# function used to add a new recipe to the user's recipe bank
@st.dialog("Add a new recipe!")
def addNewRecipe():
    recipeName = st.text_input("Recipe Name:")

    if recipeName is not None:
        # Search for the recipe
        search_response = all_recipes_api.search_recipe(recipeName)

        if recipeName != "":
            try:
                first_result = search_response[0]
            except:
                st.error("Please try again")
            recipe_name = first_result["name"]
            recipe_url = first_result["url"]
            recipe_rating = first_result["rate"]
            recipe_image = first_result["image"]
            recipe_information = all_recipes_api.get_recipe(first_result["url"])

            st.title(recipe_name)

            st.image(recipe_image, use_column_width="always")

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
                    supabaseIngredientsList.append(recipe_information["ingredients"][i])
                    ingredientsList += (
                        str(i + 1)
                        + ". "
                        + recipe_information["ingredients"][i]
                        + "\n\n"
                    )
                st.write(ingredientsList)

            ingredientsString = ", ".join(supabaseIngredientsList)

            with st.expander("Not happy with the ingredients?"):
                st.write("previous ingredients")
                ingredientsList = st.text_input(
                    value=ingredientsString, label="Change them here: "
                )
                supabaseIngredientsList = ingredientsList.split(",")

            with st.container():
                st.subheader("Steps")
                for i in range(len(recipe_information["steps"])):
                    st.write(
                        str(i + 1)
                        + ". "
                        + recipe_information["steps"][i]["task"]
                        + "\n\n"
                    )
                    if "picture" in recipe_information["steps"][i]:
                        st.image(
                            recipe_information["steps"][i]["picture"],
                            use_column_width="always",
                        )

            st.write("URL: ", recipe_url)

            add = st.button("Add this Recipe!", type="primary")
            if add:
                # checks if user already added this recipe
                if (
                    len(
                        supabaseAPI.selectspecific(
                            "recipes", "recipeURL", "recipeURL", recipe_url
                        ).data
                    )
                    != 0
                ):
                    supabaseAPI.add_recipe(
                        recipe_name,
                        {"ingredients": supabaseIngredientsList},
                        recipe_image,
                        100,
                        recipe_url,
                    )
                    st.session_state.urls.append(recipe_url)
                    st.session_state.images.append(recipe_image)
                    st.rerun()
                else:
                    st.session_state.urls.append(recipe_url)
                    st.session_state.images.append(recipe_image)
                    st.rerun()


# function that recommends the user a new recipe
@st.dialog("Here's a new recipe!")
def recommendRecipe():
    search_response = all_recipes_api.random_recipes()

    try:
        first_result = search_response[0]
    except:
        pass

    recipe_name = first_result["name"]
    recipe_url = first_result["url"]
    recipe_rating = first_result["rate"]
    recipe_image = first_result["image"]
    recipe_information = all_recipes_api.get_recipe(first_result["url"])

    st.title(recipe_name)

    st.image(recipe_image, use_column_width="always")

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
            ingredientsList += (
                str(i + 1) + ". " + recipe_information["ingredients"][i] + "\n\n"
            )
        st.write(ingredientsList)

    ingredientsString = ", ".join(supabaseIngredientsList)

    with st.expander("Not happy with the ingredients?"):
        st.write("previous ingredients")
        ingredientsList = st.text_input(
            value=ingredientsString, label="Change them here: "
        )
        supabaseIngredientsList = ingredientsList.split(",")

    with st.container():
        st.subheader("Steps")
        steps = ""
        for i in range(len(recipe_information["steps"])):
            st.write(
                str(i + 1) + ". " + recipe_information["steps"][i]["task"] + "\n\n"
            )
            if "picture" in recipe_information["steps"][i]:
                st.image(
                    recipe_information["steps"][i]["picture"], use_column_width="always"
                )

    st.write("URL: ", recipe_url)

    add = st.button("Add this Recipe!", type="primary")
    if add:
        if (
            supabaseAPI.selectspecific(
                "recipes", "recipeURL", "recipeURL", recipe_url
            ).count
            == 0
        ):
            supabaseAPI.add_recipe(
                recipe_name,
                {"ingredients": supabaseIngredientsList},
                recipe_image,
                100,
                recipe_url,
            )
            st.session_state.urls.append(recipe_url)
            st.session_state.images.append(recipe_image)
            st.rerun()
        else:
            st.session_state.urls.append(recipe_url)
            st.session_state.images.append(recipe_image)
            st.rerun()


@st.dialog("Lets do this!")
def makeTheMeal(recipeURL, recipeImageURL):
    search_response = all_recipes_api.get_recipe(recipeURL)
    recipe_name = search_response["name"]

    st.title(recipe_name)
    st.image(recipeImageURL, use_column_width="always")

    with st.container():
        st.subheader("Ingredients: ")
        ingredientsList = ""
        for i in range(len(search_response["ingredients"])):
            ingredientsList += (
                str(i + 1) + ". " + search_response["ingredients"][i] + "\n\n"
            )
        st.write(ingredientsList)

    with st.container():
        st.subheader("Steps")
        steps = ""
        for i in range(len(search_response["steps"])):
            st.write(str(i + 1) + ". " + search_response["steps"][i]["task"] + "\n\n")
            if "picture" in search_response["steps"][i]:
                st.image(search_response["steps"][i]["picture"])

    st.write("URL: ", recipeURL)

    done = st.button("Made the Meal!", type="primary")
    if done:
        with st.container():
            st.subheader("Rate Your Meal!")
            option = [
                "How filling was the meal for your family?",
                "way too little food!" + "😔",
                "not enough food but it's manageable.",
                "the perfect amount of food!" + "😁",
                "a little too much food.",
                "way too much food" + "😡",
            ]
            feedback = st.selectbox(
                "How filling was the meal for your family?", option, index=None
            )
        # SELECT <column> from <table> where <eqcol> = <eqval>
        print(supabaseAPI.select("recipes", "*"))
        oldvalue = supabaseAPI.selectspecific(
            "recipes", "portionMultiplier", "recipeURL", recipeURL
        )
        print(oldvalue)
        oldvalue = oldvalue.data[0]["portionMultiplier"]
        supabaseAPI.update_cell(
            "recipes", "imageURL", oldvalue, "portionMultiplier", oldvalue + 1
        )

        if option.index(feedback) == 0:
            supabaseAPI.update_cell(
                "recipes", "imageURL", oldvalue, "portionMultiplier", oldvalue + 30
            )
        elif option.index(feedback) == 1:
            pass
        elif option.index(feedback) == 2:
            pass
        elif option.index(feedback) == 3:
            pass
        elif option.index(feedback) == 4:
            pass


def removeRecipe(recipeURL, recipeImage):
    st.session_state.urls.remove(recipeURL)
    st.session_state.images.remove(recipeImage)


col1, col2 = st.columns(2)
with col1:
    if st.button("Add Recipe", type="primary", use_container_width=True):
        addNewRecipe()
with col2:
    if st.button("Recommend Recipe", type="primary", use_container_width=True):
        recommendRecipe()

container = st.container(border=True)
with container:
    if "urls" not in st.session_state:
        st.session_state.urls = []
        st.session_state.images = []

    for i in range(len(st.session_state.urls)):
        container.image(st.session_state.images[i], use_column_width="always")

        col1, col2 = st.columns(2)
        with col1:
            container.button(
                "Make Now",
                on_click=makeTheMeal,
                key=random.randint(1, 10000000),
                use_container_width=True,
                type="primary",
                args=(st.session_state.urls[i], st.session_state.images[i]),
            )

        with col2:
            container.button(
                "Remove Recipe",
                on_click=removeRecipe,
                use_container_width=True,
                args=(st.session_state.urls[i], st.session_state.images[i]),
                key=random.randint(1, 1000000),
            )

    if len(st.session_state.urls) == 0:
        st.write(":eyes:" + " Its empty here... Add your first recipe to get started!")
