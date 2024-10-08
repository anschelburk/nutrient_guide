# Information below is from the US Food and Drug Administration's
# daily nutrients that each person should consume:
# https://www.fda.gov/media/135301/download?attachment

recommended_daily_nutrients = {
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
    "Zinc": {"value": 11, "unit": "mg"},
}
recommended_daily_nutrients_empty = {
    key: {"value": 0, "unit": value["unit"]}
    for key, value in recommended_daily_nutrients.items()
}
