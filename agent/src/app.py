import os
import requests
import tempfile
import cv2
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

    content_list = []
    
    if not video_url:
        return {"error": "please provide video_url"}
    
    tmp_path = None
    
    try:
        # 1. Download Video
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # Use a temporary file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_path = tmp_file.name
        
        # Download in chunks to handle large files
        print(f"Downloading video to {tmp_path}...")
        with requests.get(video_url, headers=headers, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(tmp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
        # 2. Extract Frames with OpenCV
        cap = cv2.VideoCapture(tmp_path)
        
        if not cap.isOpened():
            # If OpenCV fails to open, try fallback or just return error
            raise ValueError(f"Could not open video file at {tmp_path}")

        # Get FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        # Handle cases where FPS is not correctly read
        if fps <= 0:
            print("Warning: FPS is 0 or invalid, falling back to 30.")
            fps = 30.0
            
        print(f"Video FPS: {fps}")
        
        # Calculate interval to get ~1 frame per second
        frame_interval = int(round(fps))
        if frame_interval < 1:
            frame_interval = 1
        
        print(f"Extraction Interval: {frame_interval}")
        
        frame_idx = 0
        extracted_count = 0
        MAX_FRAMES = 60  # Limit to 60 seconds/frames
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Extract 1 frame every second
            if frame_idx % frame_interval == 0:
                # Resize to reduce token usage
                height, width = frame.shape[:2]
                if width > 512:
                    scale = 512 / width
                    frame = cv2.resize(frame, (int(width*scale), int(height*scale)))

                # Encode frame to JPEG
                success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
                
                if success:
                    frame_bytes = buffer.tobytes()
                    content_list.append({
                        "image": {
                            "format": "jpeg",
                            "source": {
                                "bytes": frame_bytes
                            }
                        }
                    })
                    extracted_count += 1
            
            frame_idx += 1
            
            if extracted_count >= MAX_FRAMES:
                print(f"Max frame limit reached ({MAX_FRAMES} frames). Stopping extraction.")
                break
        
        cap.release()
        print(f"Total extracted frames: {len(content_list)}")

        if not content_list:
             return {"error": "Failed to extract any frames from video"}

        # 3. Invoke Agent with Image Frames
        result = agent(content_list)
        print("result:\n*******\n", result)
        
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
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
