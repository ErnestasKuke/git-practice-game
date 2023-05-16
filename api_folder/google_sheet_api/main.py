from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()


GENDER = "MALE"
WEIGHT_KG = "60"
HEIGHT = "160.5" #entered random height in cm
AGE = "50"

APP_ID = os.getenv("app_id")
API_KEY = os.getenv("app_key")
auth_token = os.getenv("AUTH_TOKEN") 

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_input = input("Tell which exercise you did today?: ")

header = {
    "x-app-id": APP_ID,
    'x-app-key': API_KEY
}

parameters = {
    'query': exercise_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=header)
response.raise_for_status()
result = response.json()

sheet_endpoint = "https://api.sheety.co/96e58537f8c3bdf408f6495ca70fde31/apiProject/workouts"

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_header = {
    "Authorization": auth_token
}


for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=sheety_header)
print(sheet_response.text)