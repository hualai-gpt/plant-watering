from pydantic import BaseModel
from strands.models.gemini import GeminiModel
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

class Weather(BaseModel):
    time: str
    weather: str

# 创建 Gemini 模型实例
model = GeminiModel(
    client_args={"api_key": api_key},
    model_id="gemini-3-pro-preview",
    params={
        "temperature": 0.1,
        "response_mime_type": "application/json"
    }
)

async def main():
    async for event in model.structured_output(
        Weather, 
        [{"role": "user", "content": [{"text": "The time is 12:00 and the weather is sunny"}]}]
    ):
        result = event["output"]  # Weather 实例
        print(result)
        return result

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)