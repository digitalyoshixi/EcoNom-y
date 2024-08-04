import random
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

    def random_recipes(self) -> list[dict]:
        """
        Fetches a list of recipies for a random cuisine.

        Same response format as search_recipe.
        """
        return self.recipe_scraper.random_recipes()

    def get_recipe(self, recipe_url: str) -> dict:
        """
        Gets the data from a recipe given an AllRecipes URL.

        Parameters:
            recipe_url: A link to a recipe from AllRecipes.
        """
        return self.recipe_scraper.get(recipe_url)
