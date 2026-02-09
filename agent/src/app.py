import os
import requests
import tempfile
import time
import google.generativeai as genai
from agent import create_agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Configure GenAI directly for file upload since video usually requires File API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

agent = create_agent()
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload):
    """Handler for agent invocation"""
    print("payload:\n*******\n", payload)
    
    video_url = payload.get("video_url", "")
    user_message = payload.get("user_message", "")
    
    # Input Sanitization
    if isinstance(video_url, str):
        video_url = video_url.strip()
        if video_url and not (video_url.startswith("http://") or video_url.startswith("https://")):
             return {"error": "Invalid video URL. Must start with http:// or https://"}
    else:
        video_url = ""

    content = []
    
    if user_message:
        content.append(user_message)
    
    if not video_url and not user_message:
        return {"error": "please provide video_url or user_message"}
    
    tmp_path = None
    video_file = None
    
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

            # Upload to Gemini File API
            video_file = genai.upload_file(path=tmp_path)
            print(f"Video uploaded to Gemini: {video_file.uri}")
            
            # Wait for processing
            while video_file.state.name == "PROCESSING":
                print("Waiting for video processing...")
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed in Gemini")

            # Append video file to content
            content.append(video_file)

        # Invoke agent
        result = agent(content)
        print("result:\n*******\n", result)
        
        # Clean up remote file after use
        if video_file:
            try:
                genai.delete_file(video_file.name)
                print(f"Deleted remote file {video_file.name}")
            except Exception as e:
                print(f"Failed to delete remote file {video_file.name}: {e}")
                
        return result

    except Exception as e:
        print(f"Processing failed: {e}")
        return {"error": f"Failed to process request: {str(e)}"}
        
    finally:
        # Clean up local temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception as e:
                print(f"Failed to delete temp file {tmp_path}: {e}")

app.run()
