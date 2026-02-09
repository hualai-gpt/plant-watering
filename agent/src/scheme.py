from pydantic import BaseModel, Field

class PlantInfo(BaseModel):
    plant_name: str = Field(..., description="The name of the plant identified in the video.")
    is_watering: str = Field(..., description="Whether a watering action is happening in the video (e.g., pouring water, spraying, water flowing). Return '1' if watering is occurring, '0' otherwise.")
