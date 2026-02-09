# import agent from ../src/agent.py
import sys
import os
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import create_agent

if __name__ == "__main__":
    agent = create_agent()
    
    # # 读取图片(local path)
    # with open("2.jpg", "rb") as f:
    #     image_bytes = f.read()
    
    # image url -->> image_bytes
    image_url = "https://cdn-cms.pgimgs.com/static/2021/01/CH_indoor-plants-2.jpg"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers)
    response.raise_for_status()
    image_bytes = response.content

    content = [
        {"text": "竹子"},
        {
            "image": {
                "format": "jpeg",
                "source": {
                    "bytes": image_bytes,
                },
            },
        }
    ]
    result = agent(content)
    print(result)