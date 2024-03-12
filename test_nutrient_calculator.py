from collections import defaultdict

import pytest

from nutrient_calculator import NutrientCalculator


@pytest.fixture
def ncalc():
    ncalc = NutrientCalculator()

    ncalc.nutrient_ingredient_map = {
        "apple": {
            "Vitamin C": {"value": 1, "unit": "mg"},
            "Vitamin A": {"value": 2, "unit": "mg"},
        },
        "banana": {
            "Vitamin B": {"value": 3, "unit": "mg"},
            "Vitamin C": {"value": 5, "unit": "mg"},
            "Iron": {"value": 1, "unit": "mg"},
        },
        "hot dog": {
            "Vitamin C": {"value": 1, "unit": "mg"},
            "Iron": {"value": 4, "unit": "mg"},
        },
    }

    nutrients = {"apple": 2, "banana": 4, "hot dog": 4}
    for nutrient, amount in nutrients.items():
        ncalc.add_nutrient(nutrient, amount)
    ncalc.remove_nutrient("hot dog", 1)

    return ncalc


def test_nutrient_calculator(ncalc):
    ncalc.update_ingredients()

    assert ncalc.my_ingredients == defaultdict(
        float, {"Vitamin C": 25.0, "Vitamin A": 4.0, "Vitamin B": 12.0, "Iron": 16.0}
    )
    assert ncalc.target_ingredients == defaultdict(
        float,
        {"Vitamin C": -25.0, "Vitamin A": -4.0, "Vitamin B": -12.0, "Iron": -16.0},
    )


def test_api_response(ncalc):
    # note that we call the api here, for unit testing you might want to "mock"
    # the api to not make a call over the network
    ncalc.get_ingredients_for_nutrient("ORANGE")
    assert len(ncalc.nutrient_ingredient_map) == 4
    assert "orange" in ncalc.nutrient_ingredient_map
    assert ncalc.nutrient_ingredient_map["orange"] == {
        "Carbohydrate": {"unit": "G", "value": 90.5},
        "Energy": {"unit": "KCAL", "value": 381},
        "Protein": {"unit": "G", "value": 4.76},
        "Sodium": {"unit": "MG", "value": 381},
        "Total Sugars": {"unit": "G", "value": 90.5},
        "Total lipid (fat)": {"unit": "G", "value": 0.0},
    }
