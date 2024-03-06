import os
import requests

daily_values = {
    "Added sugars": {"value": 50, "unit": "g"},
    "Biotin": {"value": 30, "unit": "mcg"},
    "Calcium": {"value": 1300, "unit": "mg"},
    "Chloride": {"value": 2300, "unit": "mg"},
    "Choline": {"value": 550, "unit": "mg"},
    "Cholesterol": {"value": 300, "unit": "mg"},
    "Chromium": {"value": 35, "unit": "mcg"},
    "Copper": {"value": 0.9, "unit": "mg"},
    "Dietary Fiber": {"value": 28, "unit": "g"},
    "Fat": {"value": 78, "unit": "g"},
    "Folate/Folic Acid": {"value": 400, "unit": "mcg DFE"},
    "Iodine": {"value": 150, "unit": "mcg"},
    "Iron": {"value": 18, "unit": "mg"},
    "Magnesium": {"value": 420, "unit": "mg"},
    "Manganese": {"value": 2.3, "unit": "mg"},
    "Molybdenum": {"value": 45, "unit": "mcg"},
    "Niacin": {"value": 16, "unit": "mg NE"},
    "Pantothenic Acid": {"value": 5, "unit": "mg"},
    "Phosphorus": {"value": 1250, "unit": "mg"},
    "Potassium": {"value": 4700, "unit": "mg"},
    "Protein": {"value": 50, "unit": "g"},
    "Riboflavin": {"value": 1.3, "unit": "mg"},
    "Saturated fat": {"value": 20, "unit": "g"},
    "Selenium": {"value": 55, "unit": "mcg"},
    "Sodium": {"value": 2300, "unit": "mg"},
    "Thiamin": {"value": 1.2, "unit": "mg"},
    "Total carbohydrate": {"value": 275, "unit": "g"},
    "Vitamin A": {"value": 900, "unit": "mcg RAE"},
    "Vitamin B6": {"value": 1.7, "unit": "mg"},
    "Vitamin B12": {"value": 2.4, "unit": "mcg"},
    "Vitamin C": {"value": 90, "unit": "mg"},
    "Vitamin D": {"value": 20, "unit": "mcg"},
    "Vitamin E": {"value": 15, "unit": "mg alpha-tocopherol"},
    "Vitamin K": {"value": 120, "unit": "mcg"},
    "Zinc": {"value": 11, "unit": "mg"}
}

# json_data = [{'nutrientId': 1087, 'nutrientName': 'Calcium, Ca', 'nutrientNumber': '301', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5300, 'indentLevel': 1, 'foodNutrientId': 3145990, 'percentDailyValue': 0}, {'nutrientId': 1089, 'nutrientName': 'Iron, Fe', 'nutrientNumber': '303', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.23, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5400, 'indentLevel': 1, 'foodNutrientId': 3145991, 'percentDailyValue': 2}, {'nutrientId': 1093, 'nutrientName': 'Sodium, Na', 'nutrientNumber': '307', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5800, 'indentLevel': 1, 'foodNutrientId': 3145992, 'percentDailyValue': 0}, {'nutrientId': 1104, 'nutrientName': 'Vitamin A, IU', 'nutrientNumber': '318', 'unitName': 'IU', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 65.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 7500, 'indentLevel': 1, 'foodNutrientId': 3145993, 'percentDailyValue': 2}, {'nutrientId': 1162, 'nutrientName': 'Vitamin C, total ascorbic acid', 'nutrientNumber': '401', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 3.1, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 6300, 'indentLevel': 1, 'foodNutrientId': 3145994, 'percentDailyValue': 8}, {'nutrientId': 1253, 'nutrientName': 'Cholesterol', 'nutrientNumber': '601', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 15700, 'indentLevel': 1, 'foodNutrientId': 3145995, 'percentDailyValue': 0}, {'nutrientId': 1258, 'nutrientName': 'Fatty acids, total saturated', 'nutrientNumber': '606', 'unitName': 'G', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 9700, 'indentLevel': 1, 'foodNutrientId': 3145996, 'percentDailyValue': 0}, {'nutrientId': 1003, 'nutrientName': 'Protein', 'nutrientNumber': '203', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 600, 'indentLevel': 1, 'foodNutrientId': 4587770, 'percentDailyValue': 0}, {'nutrientId': 1005, 'nutrientName': 'Carbohydrate, by difference', 'nutrientNumber': '205', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 14.3, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 1110, 'indentLevel': 2, 'foodNutrientId': 4587771, 'percentDailyValue': 7}, {'nutrientId': 1008, 'nutrientName': 'Energy', 'nutrientNumber': '208', 'unitName': 'KCAL', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 52.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 300, 'indentLevel': 1, 'foodNutrientId': 4587772, 'percentDailyValue': 0}, {'nutrientId': 2000, 'nutrientName': 'Total Sugars', 'nutrientNumber': '269', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 10.4, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 1510, 'indentLevel': 3, 'foodNutrientId': 4587773, 'percentDailyValue': 0}, {'nutrientId': 1079, 'nutrientName': 'Fiber, total dietary', 'nutrientNumber': '291', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 3.2, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 1200, 'indentLevel': 3, 'foodNutrientId': 4587774, 'percentDailyValue': 20}, {'nutrientId': 1092, 'nutrientName': 'Potassium, K', 'nutrientNumber': '306', 'unitName': 'MG', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 110, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5700, 'indentLevel': 1, 'foodNutrientId': 4587775, 'percentDailyValue': 5}, {'nutrientId': 1257, 'nutrientName': 'Fatty acids, total trans', 'nutrientNumber': '605', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 15400, 'indentLevel': 1, 'foodNutrientId': 4587776, 'percentDailyValue': 0}, {'nutrientId': 1004, 'nutrientName': 'Total lipid (fat)', 'nutrientNumber': '204', 'unitName': 'G', 'derivationCode': 'LCSL', 'derivationDescription': 'Calculated from a less than value per serving size measure', 'derivationId': 73, 'value': 0.65, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 800, 'indentLevel': 1, 'foodNutrientId': 6376585, 'percentDailyValue': 0}]

json_data = [
    {'nutrientId': 1087, 'nutrientName': 'Calcium, Ca', 'nutrientNumber': '301', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5300, 'indentLevel': 1, 'foodNutrientId': 3145990, 'percentDailyValue': 0},
    {'nutrientId': 1089, 'nutrientName': 'Iron, Fe', 'nutrientNumber': '303', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.23, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5400, 'indentLevel': 1, 'foodNutrientId': 3145991, 'percentDailyValue': 2},
    {'nutrientId': 1093, 'nutrientName': 'Sodium, Na', 'nutrientNumber': '307', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5800, 'indentLevel': 1, 'foodNutrientId': 3145992, 'percentDailyValue': 0},
    {'nutrientId': 1104, 'nutrientName': 'Vitamin A, IU', 'nutrientNumber': '318', 'unitName': 'IU', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 65.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 7500, 'indentLevel': 1, 'foodNutrientId': 3145993, 'percentDailyValue': 2},
    {'nutrientId': 1162, 'nutrientName': 'Vitamin C, total ascorbic acid', 'nutrientNumber': '401', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 3.1, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 6300, 'indentLevel': 1, 'foodNutrientId': 3145994, 'percentDailyValue': 8},
    {'nutrientId': 1253, 'nutrientName': 'Cholesterol', 'nutrientNumber': '601', 'unitName': 'MG', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 15700, 'indentLevel': 1, 'foodNutrientId': 3145995, 'percentDailyValue': 0},
    {'nutrientId': 1258, 'nutrientName': 'Fatty acids, total saturated', 'nutrientNumber': '606', 'unitName': 'G', 'derivationCode': 'LCCD', 'derivationDescription': 'Calculated from a daily value percentage per serving size measure', 'derivationId': 75, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 9700, 'indentLevel': 1, 'foodNutrientId': 3145996, 'percentDailyValue': 0},
    {'nutrientId': 1003, 'nutrientName': 'Protein', 'nutrientNumber': '203', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 600, 'indentLevel': 1, 'foodNutrientId': 4587770, 'percentDailyValue': 0},
    {'nutrientId': 1005, 'nutrientName': 'Carbohydrate, by difference', 'nutrientNumber': '205', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 14.3, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 1110, 'indentLevel': 2, 'foodNutrientId': 4587771, 'percentDailyValue': 7},
    {'nutrientId': 1008, 'nutrientName': 'Energy', 'nutrientNumber': '208', 'unitName': 'KCAL', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 52.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 300, 'indentLevel': 1, 'foodNutrientId': 4587772, 'percentDailyValue': 0},
    {'nutrientId': 2000, 'nutrientName': 'Total Sugars', 'nutrientNumber': '269', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 10.4, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 1510, 'indentLevel': 3, 'foodNutrientId': 4587773, 'percentDailyValue': 0},
    {'nutrientId': 1079, 'nutrientName': 'Fiber, total dietary', 'nutrientNumber': '291', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 3.2, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 1200, 'indentLevel': 3, 'foodNutrientId': 4587774, 'percentDailyValue': 20},
    {'nutrientId': 1092, 'nutrientName': 'Potassium, K', 'nutrientNumber': '306', 'unitName': 'MG', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 110, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 5700, 'indentLevel': 1, 'foodNutrientId': 4587775, 'percentDailyValue': 5},
    {'nutrientId': 1257, 'nutrientName': 'Fatty acids, total trans', 'nutrientNumber': '605', 'unitName': 'G', 'derivationCode': 'LCCS', 'derivationDescription': 'Calculated from value per serving size measure', 'derivationId': 70, 'value': 0.0, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 15400, 'indentLevel': 1, 'foodNutrientId': 4587776, 'percentDailyValue': 0},
    {'nutrientId': 1004, 'nutrientName': 'Total lipid (fat)', 'nutrientNumber': '204', 'unitName': 'G', 'derivationCode': 'LCSL', 'derivationDescription': 'Calculated from a less than value per serving size measure', 'derivationId': 73, 'value': 0.65, 'foodNutrientSourceId': 9, 'foodNutrientSourceCode': '12', 'foodNutrientSourceDescription': "Manufacturer's analytical; partial documentation", 'rank': 800, 'indentLevel': 1, 'foodNutrientId': 6376585, 'percentDailyValue': 0}
]

def get_search_results_data(searchbar_input):
        return(requests.get(
            search_endpoint,
            params={"query": searchbar_input, "api_key": DEMO_KEY}
        ))

DEMO_KEY = os.getenv('DEMO_KEY', "")
search_endpoint = 'https://api.nal.usda.gov/fdc/v1/foods/search'

search = 'apple'
results_nutrients = get_search_results_data(search).json().get('foods')[0].get('foodNutrients')

def format_json_data_as_dict(data):
    json_data_formatted_dict = {}
    for item in data:
        nutrient_name_json = item['nutrientName']
        nutrient_amount_json = item['value']
        nutrient_unit_json = item['unitName']
        json_data_formatted_dict[nutrient_name_json] = {
            'value': nutrient_amount_json,
            'unit': nutrient_unit_json
        }
    return(json_data_formatted_dict)

json_data_formatted = format_json_data_as_dict(json_data)

print(json_data_formatted)