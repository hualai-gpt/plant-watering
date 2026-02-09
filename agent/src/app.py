import requests
from agent import create_agent

agent = create_agent()

from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()
@app.entrypoint
def agent_invocation(payload):
    """Handler for agent invocation"""
    print("payload:\n*******\n", payload)
    user_message = payload.get("user_message", "")
    image_url = payload.get("image_url", "")

    # Input Sanitization
    if isinstance(user_message, str):
        user_message = user_message.strip()
    else:
        user_message = ""

    if isinstance(image_url, str):
        image_url = image_url.strip()
        if image_url and not (image_url.startswith("http://") or image_url.startswith("https://")):
             return {"error": "Invalid image URL. Must start with http:// or https://"}
    else:
        image_url = ""


    content = []

    if not user_message and not image_url:
        return {"error": "please provide image or text description"}

    if user_message:
        content.append({"text": user_message})

    if image_url:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                return {"error": f"Invalid content type: {content_type}. Please provide a valid image URL."}

            image_bytes = response.content
            content.append({
                "image": {
                    "format": "jpeg",
                    "source": {
                        "bytes": image_bytes,
                    },
                },
            })
        except Exception as e:
            return {"error": f"Failed to download image: {str(e)}"}
    
    result = agent(content)
    print(type(result))
    print("result:\n*******\n", result)
    return result

app.run()