from pydantic import BaseModel, Field

class PlantInfo(BaseModel):
    plant_name: str = Field(..., description="The name of the plant identified in the video.")
    is_watering: str = Field(..., description="Whether the plant needs watering right now based on visual signs (e.g., drooping leaves, dry soil). Return '1' for yes, '0' for no.")
