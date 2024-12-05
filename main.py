from fastapi import FastAPI
from domain.weather import weather_router


app = FastAPI()
app.include_router(weather_router.router)
