# Nutrient Guide

Copyright © 2024 Anschel Burk. All rights not explicitly granted in this project's license reserved.

## 1. Description

A simple, interactive guide, powered by USDA data, that gives personalized guidance for making healthy meals.

This app is powered by [Streamlit](https://streamlit.io/), and uses data from the [USDA FoodData Central database](https://fdc.nal.usda.gov/). Originally developed as a capstone project in the [Pybites Python Developer Mindset (PDM) Program](https://pybit.es/catalogue/the-pdm-program/), this project is under active development.

## 2. License

Copyright © 2024 Anschel Burk. All rights not explicitly granted in this project's license reserved.

### 2A. License Notice: Streamlit

This application is powered by [Streamlit](https://streamlit.io/), which is licensed under the Apache License 2.0. For details, please see [Streamlit's license](https://github.com/streamlit/streamlit/blob/develop/LICENSE).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

### 2B. This Project's License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See this project's [LICENSE.txt](LICENSE.txt) file for the specific language governing permissions and limitations under the License.

## 3. Features

- **Ingredient Search:** Allows users to search for an ingredient, using the [USDA's FoodData Central database](https://fdc.nal.usda.gov/)
- **Ingredients List:** Allows users to create a custom list of ingredients they find.
- **"Nutrients I Have" Section:** Allows users to see a list of the nutrients collectively provided by their ingredients list.
- **"Nutrients I Need" Section:** Allows users to see any remaining nutrients they need to meet the USDA's daily nutrient recommendations.

## 4. Installation & Dependencies

#### 1. Clone this repository.

HTTPS:
```
git clone https://github.com/anschelburk/nutrient-guide.git
```

SSH:
```
git clone git@github.com:anschelburk/nutrient-guide.git
```

#### 2. Create a virtual environment, activate it, and install this project's dependencies.

Windows (PowerShell):
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux & MacOS:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Obtain a USDA API key.

Users can obtain a unique USDA API key by completing a short form, on [this page](https://fdc.nal.usda.gov/api-key-signup.html). This API key enables the user to make 1,000 database requests per hour. Alternatively, users can simply use the string `'DEMO_KEY'` as their API key, for a more limited number of hourly and daily database requests that does not require registration. (Using `'DEMO_KEY'` grants a user 30 requests per IP address per hour; 50 requests per IP address per day).

For more information on how these two options compare, please see the "Web Service Rate Limits" section of the [this page](https://api.data.gov/docs/developer-manual/).

For instructions on how to add your API key to your local repo's environment variables for this project, please see [**Step 4**](#4-configure-environment-variables).

#### 4. Configure environment variables.

This app uses the `python-decouple` library to manage environment variables, using a local `.env` file which must be configured prior to use.

After cloning this repository, copy the included `.env_template`, and name the copy `.env`. You'll find that the file contains a single line:

```
API_KEY = 
```

Next to the `=`, write your API code - either the one you received by registering, or the string `'DEMO_KEY'`, as a string.

For example, if you had the following API key:

```
abcdefghijklmnop1234567890
```

Then, your `.env` file should look like this:

```
API_KEY = 'abcdefghijklmnop1234567890'
```

For information and instructions on obtaining an API key, please see [**Step 3**](#3-obtain-a-usda-api-key).

#### 5. Run the app, and enjoy!

Activate the app by running the following command from the project directory:

```
streamlit run nutrient_guide.py
```

Enjoy!