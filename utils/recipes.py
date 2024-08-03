import random


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

    def get_random_cuisine(self) -> list[str, str]:
        """
        Returns a random cuisine, and the link to the AllRecipes page for it.
        """
        soup = self.recipe_scraper._fetch_page(
            "https://www.allrecipes.com/cuisine-a-z-6740455")

        cuisines = soup.select("a.mntl-link-list__link")
        random_cuisine = random.choice(cuisines)

        return random_cuisine.text, random_cuisine['href']

    def random_recipes(self) -> list[dict]:
        _cuisine, cuisine_link = self.get_random_cuisine()
        soup = self.recipe_scraper._fetch_page(cuisine_link)
        return self.recipe_scraper._extract_articles(soup)

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
