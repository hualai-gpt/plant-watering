from pydantic import BaseModel, Field
from typing import List

class WateringSchedule(BaseModel):
    time: str = Field(..., description="watering time, HH:MM")
    frequency_days: int = Field(..., description="watering frequency in days (e.g., 1 for daily, 2 for every other day)")
    amount_ml: int = Field(..., description="amount of water in milliliters")

class PlantInfo(BaseModel):
    plant_name: str = Field(..., description="plant name")
    plant_water_type: str = Field(..., description="plant water needs type: high-water, medium-water, low-water (drought-tolerant)")
    soil_moisture_pref: str = Field(..., description="preferred soil moisture condition (e.g. moist, dry between waterings)")
    watering_schedule: List[WateringSchedule] = Field(..., description="recommended watering schedule")