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
    Please analyze the plant in the video to determine if it needs watering immediately.
    
    Follow the following steps to complete the task:
    1. Identify the plant name.
    2. Analyze visual signs of water stress (e.g., drooping/wilting leaves, dry/cracked soil color, shriveled leaves for succulents).
    3. Determine if the plant needs water RIGHT NOW.
    4. Return "1" if it clearly needs water, or "0" if it looks healthy/hydrated or if you are unsure.

"""

def create_agent():
    # 创建 Agent
    agent = Agent(
        model=model, 
        system_prompt=system_prompt,
        structured_output_model=PlantInfo
    )
    return agent
