from collections import Counter, defaultdict
import os

import requests

from recommended_daily_nutrients import recommended_daily_nutrients

USDA_API_KEY = os.getenv("DEMO_KEY", "")
SEARCH_ENDPOINT = "https://api.nal.usda.gov/fdc/v1/foods/search"


class NutrientCalculator:
    def __init__(
        self,
        my_ingredients: defaultdict | None = None,
        target_ingredients: defaultdict | None = None,
    ):
        # the two ingredient tables
        self.my_ingredients = (
            defaultdict(float) if my_ingredients is None else my_ingredients
        )
        self.target_ingredients = (
            defaultdict(float) if target_ingredients is None else target_ingredients
        )
        # cache of food api infos
        self.nutrient_ingredient_map: dict[str, dict] = {}
        # what's currently selected:
        self.selected_nutrients: dict[str, int] = Counter()

    def _normalize_ingredient_names(self, ingredients):
        return {key.split(", ")[0]: value for key, value in ingredients.items()}

    def get_ingredients_for_nutrient(self, nutrient):
        nutrient = nutrient.lower()
        if nutrient in self.nutrient_ingredient_map:
            print(f"Found {nutrient} in cache")
            return self.nutrient_ingredient_map[nutrient]

        # not in cache, call the API
        params = {"query": nutrient, "api_key": USDA_API_KEY}
        response = requests.get(SEARCH_ENDPOINT, params=params)
        api_search_result = response.json()["foods"][0]
        ingredients_parsed = {
            val["nutrientName"]: {"value": val["value"], "unit": val["unitName"]}
            for val in api_search_result["foodNutrients"]
        }
        ingredients_normalized = self._normalize_ingredient_names(ingredients_parsed)
        self.nutrient_ingredient_map[nutrient] = ingredients_normalized
        return ingredients_normalized

    def add_nutrient(self, nutrient, amount):
        self.selected_nutrients[nutrient] += amount

    def remove_nutrient(self, nutrient, amount):
        self.selected_nutrients[nutrient] -= amount

    def update_ingredients(self):
        print("Updating ingredients")
        for nutrient, amount in self.selected_nutrients.items():
            ingredients = self.get_ingredients_for_nutrient(nutrient)
            for ingredient, details in ingredients.items():
                ingredient_amount = details["value"] * amount
                self.my_ingredients[ingredient] += ingredient_amount
                self.target_ingredients[ingredient] -= ingredient_amount
        # from pprint import pprint as pp
        # pp(self.my_ingredients)
        # pp(self.target_ingredients)
