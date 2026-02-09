import os
from strands import Agent
from strands.models.gemini import GeminiModel
from dotenv import load_dotenv
from scheme import PlantInfo

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# 创建 Gemini 模型实例
model = GeminiModel(
    client_args={"api_key": api_key},
    model_id="gemini-3-flash-preview",
    params={
        "temperature": 0.1,
        # "response_mime_type": "application/json"
    }
)

system_prompt = """
    You are a professional video analysis bot for plant care.
    Your task is to analyze the video and detect if a "watering action" is taking place.
    
    Follow these steps:
    1. Check if there is a plant in the video.
        - If NO plant is visible, set plant_name to "None" and is_watering to "0".
        - If a plant is visible, identify its name.
    2. Watch for specific actions: someone pouring water from a can/bottle/cup, using a spray bottle, water flowing from a hose/tap into the pot, or water clearly entering the soil/substrate.
    3. Return "1" ONLY if you see the active process of watering happening.
    4. Return "0" if:
        - No plant is visible.
        - The video just shows a static plant.
        - A person just touching/pruning the plant without water.
        - The soil is just wet but no active watering is occurring.

"""

def create_agent():
    # 创建 Agent
    agent = Agent(
        model=model, 
        system_prompt=system_prompt,
        structured_output_model=PlantInfo
    )
    return agent
