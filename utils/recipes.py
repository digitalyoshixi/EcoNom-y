from .allrecipes import AllRecipes


class AllRecipesAPI:
    def __init__(self):
        self.recipe_scraper = AllRecipes()

    def search_recipe(self, query: str) -> list[dict]:
        """
        Searches for recipes from AllRecipes based on a query.

        Parameters:
            query: A search query for recipies.
        """
        return self.recipe_scraper.search(query)

    def get_recipe(self, recipe_url: str) -> dict:
        """
        Gets the data from a recipe given an AllRecipes URL.

        Parameters:
            recipe_url: A link to a recipe from AllRecipes.
        """
        return self.recipe_scraper.get(recipe_url)


if __name__ == "__main__":
    all_recipes_api = AllRecipesAPI()
    search_response = all_recipes_api.search_recipe("Potato Salad")

    first_result = search_response[0]
    recipe_name = first_result["name"]
    recipe_url = first_result['url']
    recipe_rating = first_result['rate']
    recipe_image = first_result['image']

    print(first_result)
    print(f"{recipe_name=}, {recipe_url=}, {recipe_rating=}, {recipe_image=}")

    recipe_information = all_recipes_api.get_recipe(first_result['url'])
    print(recipe_information)
