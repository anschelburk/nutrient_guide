import pytest

from nutrient_calculator import NutrientCalculator


@pytest.fixture
def ncalc():
    ncalc = NutrientCalculator()

    ncalc.nutrient_ingredient_cache = {
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


def test_api_response(ncalc):
    # note that we call the api here, for unit testing you might want to "mock"
    # the api to not make a call over the network
    ncalc.get_ingredients_for_nutrient("ORANGE")
    assert len(ncalc.nutrient_ingredient_cache) == 4
    assert "orange" in ncalc.nutrient_ingredient_cache
    assert ncalc.nutrient_ingredient_cache["orange"] == {
        "Carbohydrate": {"unit": "G", "value": 90.5},
        "Energy": {"unit": "KCAL", "value": 381},
        "Protein": {"unit": "G", "value": 4.76},
        "Sodium": {"unit": "MG", "value": 381},
        "Total Sugars": {"unit": "G", "value": 90.5},
        "Total lipid (fat)": {"unit": "G", "value": 0.0},
    }


def test_nutrient_calculator(ncalc):
    ncalc.update_ingredients()
    assert ncalc.my_ingredients["Vitamin A"]["value"] == 4
    assert ncalc.my_ingredients["Vitamin C"]["value"] == 25
    assert ncalc.my_ingredients["Iron"]["value"] == 16
    assert ncalc.target_ingredients["Vitamin A"]["value"] == 896  # 900 - 4
    assert ncalc.target_ingredients["Vitamin C"]["value"] == 65  # 90 - 25
    assert ncalc.target_ingredients["Iron"]["value"] == 2  # 18 - 16


def test_nutrient_calculator_change_quantity_banana(ncalc):
    ncalc.remove_nutrient("banana", 1)
    ncalc.add_nutrient("banana", 2)
    ncalc.update_ingredients()
    assert ncalc.my_ingredients["Vitamin A"]["value"] == 4
    assert ncalc.my_ingredients["Vitamin C"]["value"] == 30
    assert ncalc.my_ingredients["Iron"]["value"] == 17
    assert ncalc.target_ingredients["Vitamin A"]["value"] == 896  # 900 - 4
    assert ncalc.target_ingredients["Vitamin C"]["value"] == 60  # 90 - 30
    assert ncalc.target_ingredients["Iron"]["value"] == 1  # 18 - 17


def test_nutrient_calculator_change_quantity_apples_multi_times(ncalc):
    ncalc.add_nutrient("apple", 1)
    ncalc.add_nutrient("apple", 2)
    ncalc.add_nutrient("apple", 2)
    ncalc.remove_nutrient("apple", 3)
    ncalc.add_nutrient("apple", 3)
    ncalc.update_ingredients()
    assert ncalc.my_ingredients["Vitamin A"]["value"] == 14
    assert ncalc.my_ingredients["Vitamin C"]["value"] == 30
    assert ncalc.my_ingredients["Iron"]["value"] == 16
    assert ncalc.target_ingredients["Vitamin A"]["value"] == 886  # 900 - 14
    assert ncalc.target_ingredients["Vitamin C"]["value"] == 60  # 90 - 30
    assert ncalc.target_ingredients["Iron"]["value"] == 2  # 18 - 16
