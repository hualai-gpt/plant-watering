import os
from strands import Agent
from strands.models.gemini import GeminiModel
from dotenv import load_dotenv
from .scheme import PlantInfo

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
    You are a professional bot for plant watering analysis.
    Please analyze the plant in the image and provide professional watering suggestions.
    
    Follow the following steps to complete the task:
    1. Identify the plant, growth stage, growth status, etc.
    2. Determine the plant's water needs: high (loves moisture), medium, or low (drought-tolerant/succulent).
    3. Provide a watering schedule (time of day, frequency in days) and appropriate water amount in ml.
    4. Consider the soil moisture preference (e.g., keep moist vs let dry completely).

"""

def create_agent():
    # 创建 Agent
    agent = Agent(
        model=model, 
        system_prompt=system_prompt,
        structured_output_model=PlantInfo
    )
    return agent
