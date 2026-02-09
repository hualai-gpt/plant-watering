import os
import requests
import tempfile
import time
from agent import create_agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

agent = create_agent()
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload):
    """Handler for agent invocation"""
    print("payload:\n*******\n", payload)
    
    video_url = payload.get("video_url", "")
    
    # Input Sanitization
    if isinstance(video_url, str):
        video_url = video_url.strip()
        if video_url and not (video_url.startswith("http://") or video_url.startswith("https://")):
             return {"error": "Invalid video URL. Must start with http:// or https://"}
    else:
        video_url = ""

    content = []
    
    if not video_url:
        return {"error": "please provide video_url"}
    
    tmp_path = None
    
    try:
        if video_url:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            # Download video to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_path = tmp_file.name
                # Download inside the file context to ensure it's written
                with requests.get(video_url, headers=headers, stream=True, timeout=120) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            tmp_file.write(chunk)
            
            print(f"Video downloaded to {tmp_path}")

            # Read video bytes
            with open(tmp_path, "rb") as f:
                video_bytes = f.read()

            # Construct content for Strands Agent (using bytes, NOT Gemini file upload)
            content.append({
                "video": {
                    "format": "mp4",
                    "source": {
                        "bytes": video_bytes
                    }
                }
            })

        # Invoke agent
        # Note: Strands Agent usually takes a list of content blocks directly for the user message
        result = agent(content)
        print("result:\n*******\n", result)
        
        return result

    except Exception as e:
        print(f"Processing failed: {e}")
        # Return error structure that matches expected output or at least doesn't crash the lambda handler
        return {"error": f"Failed to process request: {str(e)}"}
        
    finally:
        # Clean up local temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception as e:
                print(f"Failed to delete temp file {tmp_path}: {e}")

app.run()
