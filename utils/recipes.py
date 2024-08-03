
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


if __name__ != "__main__":
    from .allrecipes import AllRecipes
else:
    from allrecipes import AllRecipes

    all_recipes_api = AllRecipesAPI()
    print(all_recipes_api.search_recipe('hotdog') != [])
    print(all_recipes_api.get_recipe(
        "https://www.allrecipes.com/recipe/16729/old-fashioned-potato-salad/") != {})
