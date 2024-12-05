from fastapi import FastAPI
import os
from dotenv import load_dotenv
from domain.weather import weather_router

load_dotenv()
app = FastAPI()
app.include_router(weather_router.router)

API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise Exception("API key not found. Please set it in the .env file.")
BASE_URL = "http://api.weatherapi.com/v1/current.json"
