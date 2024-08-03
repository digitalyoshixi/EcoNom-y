# -*- coding: utf-8 -*-

import requests
import random
import lxml
import cchardet
from bs4 import BeautifulSoup


class AllRecipes:
    BASE_URL = "https://allrecipes.com/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Cookie': 'euConsent=true',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}

    def _fetch_page(self, url, params=None):
        response = self.session.get(url, params=params)
        return BeautifulSoup(response.text, 'lxml')

    def _parse_article(self, article):
        data = {}
        try:
            data["name"] = article.find(
                "span", {
                    "class": "card__title"}).get_text(
                strip=True)
            if len(data["name"]) > 80:
                data["name"] = data["name"][:80] + "..."
            data["url"] = article['href']
            data["rate"] = len(article.find_all("svg", {"class": "icon-star"}))
            if article.find_all("svg", {"class": "icon-star-half"}):
                data["rate"] += 0.5
            data["image"] = article.find('img').get(
                'data-src') or article.find('img').get('src')
        except Exception:
            pass
        return data

    def _extract_articles(self, soup):
        articles = soup.find_all("a", {"class": "mntl-card-list-items"})
        articles = [a for a in articles if a["href"].startswith(
            "https://www.allrecipes.com/recipe/")]
        return [self._parse_article(article) for article in articles]

    def search(self, search_string):
        url = f"{self.BASE_URL}search"
        soup = self._fetch_page(url, params={"q": search_string})
        return self._extract_articles(soup)

    def homepage(self):
        pages = [
            "/recipes/84/healthy-recipes",
            "/recipes/76/appetizers-and-snacks",
            "/",
            "/recipes/17562/dinner"
        ]
        soup = self._fetch_page(self.BASE_URL + random.choice(pages))
        return self._extract_articles(soup)

    @staticmethod
    def _get_name(soup):
        return soup.select("h1.article-heading")[0].get_text(strip=True)

    @staticmethod
    def _get_rating(soup):
        return float(soup.select(
            "div.mm-recipes-review-bar__rating")[0].get_text(strip=True))

    @staticmethod
    def _get_ingredients(soup):
        return [li.get_text().strip() for li in soup.select(
            "ul.mm-recipes-structured-ingredients__list")[0].find_all("li")]

    @staticmethod
    def _get_steps(soup):
        steps = []
        for index, step in enumerate(soup.select(
                "div.mm-recipes-steps__content")[0].select("li")):
            task = step.find("p").text.strip()
            img_element = step.find("img")

            step_data = {
                "task": task,
                "step": str(
                    index + 1)}

            if img_element:
                step_data['picture'] = img_element['data-src']

            steps.append(step_data)

        return steps

    @staticmethod
    def _get_times_data(soup):
        information_dict = {}
        for item in soup.select("div.mm-recipes-details__item"):
            label = item.find(
                "div", {
                    "class": "mm-recipes-details__label"}).text.strip()
            value = item.find("div", {"class": "mm-recipes-details__value"})
            information_dict[label] = value.get_text(
                strip=True) if value else ""
        return information_dict

    def _get_prep_time(self, times_data):
        return times_data.get("Prep Time:", "")

    def _get_cook_time(self, times_data):
        return times_data.get("Cook Time:", "")

    def _get_total_time(self, times_data):
        return times_data.get("Total Time:", "")

    def _get_nb_servings(self, times_data):
        return times_data.get("Servings:", "")

    @staticmethod
    def _get_description(soup):
        return soup.select("p.article-subheading")[0].text

    def get(self, url):
        soup = self._fetch_page(url)
        times_data = self._get_times_data(soup)

        elements = [
            {"name": "name", "default_value": ""},
            {"name": "ingredients", "default_value": []},
            {"name": "steps", "default_value": []},
            {"name": "rating", "default_value": None},
            {"name": "prep_time", "default_value": ""},
            {"name": "cook_time", "default_value": ""},
            {"name": "total_time", "default_value": ""},
            {"name": "nb_servings", "default_value": ""},
            {"name": "description", "default_value": ""},
        ]

        data = {"url": url}
        for element in elements:
            try:
                if element["name"] in [
                    "prep_time",
                    "cook_time",
                    "total_time",
                        "nb_servings"]:
                    data[element["name"]] = getattr(
                        self, f"_get_{element['name']}")(times_data)
                else:
                    data[element["name"]] = getattr(
                        self, f"_get_{element['name']}")(soup)
            except Exception:
                data[element["name"]] = element["default_value"]

        return data
