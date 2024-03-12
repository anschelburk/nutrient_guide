from copy import deepcopy
from collections import Counter
import os

import requests

from recommended_daily_nutrients import (
    recommended_daily_nutrients,
    recommended_daily_nutrients_empty,
)

USDA_API_KEY = os.getenv("DEMO_KEY", "")
SEARCH_ENDPOINT = "https://api.nal.usda.gov/fdc/v1/foods/search"


class NutrientCalculator:

    def __init__(self):
        self.nutrient_ingredient_cache: dict[str, dict] = {}
        self.selected_nutrients: dict[str, int] = Counter()
        self._reset_ingredients()

    def _reset_ingredients(self):
        mine = deepcopy(recommended_daily_nutrients_empty)
        target = deepcopy(recommended_daily_nutrients)
        self.my_ingredients, self.target_ingredients = mine, target

    def _normalize_ingredient_names(self, ingredients):
        return {key.split(", ")[0]: value for key, value in ingredients.items()}

    def get_ingredients_for_nutrient(self, nutrient):
        nutrient = nutrient.lower()
        if nutrient in self.nutrient_ingredient_cache:
            return self.nutrient_ingredient_cache[nutrient]

        # only call API if not already in cache
        params = {"query": nutrient, "api_key": USDA_API_KEY}
        response = requests.get(SEARCH_ENDPOINT, params=params)
        api_search_result = response.json()["foods"][0]
        ingredients_parsed = {
            val["nutrientName"]: {"value": val["value"], "unit": val["unitName"]}
            for val in api_search_result["foodNutrients"]
        }
        ingredients_normalized = self._normalize_ingredient_names(ingredients_parsed)
        self.nutrient_ingredient_cache[nutrient] = ingredients_normalized
        return ingredients_normalized

    def add_nutrient(self, nutrient, amount):
        self.selected_nutrients[nutrient] += amount

    def remove_nutrient(self, nutrient, amount):
        self.selected_nutrients[nutrient] -= amount

    def update_ingredients(self):
        self._reset_ingredients()
        for nutrient, amount in self.selected_nutrients.items():
            ingredients = self.get_ingredients_for_nutrient(nutrient)
            for ingredient, details in ingredients.items():
                ingredient_amount = details["value"] * amount
                if ingredient not in self.my_ingredients:
                    self.my_ingredients[ingredient] = {"value": 0, "unit": details["unit"]}
                if ingredient not in self.target_ingredients:
                    self.target_ingredients[ingredient] = {"value": 0, "unit": details["unit"]}
                self.my_ingredients[ingredient]["value"] += ingredient_amount
                self.target_ingredients[ingredient]["value"] -= ingredient_amount
