from pydantic import BaseModel, Field

class PlantInfo(BaseModel):
    plant_name: str = Field(..., description="The name of the plant identified in the video. If no plant is visible, return 'None'.")
    is_watering: str = Field(..., description="Whether a watering action is happening in the video (e.g., pouring water, spraying). Return '1' if watering is occurring, '0' otherwise.")
