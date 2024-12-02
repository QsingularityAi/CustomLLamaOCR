import chainlit as cl
from groq import Groq
from PIL import Image
import io
import base64
import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

async def encode_image_to_base64(image_data) -> str:
    """Convert image data to base64 string."""
    try:
        # Process image with PIL
        with Image.open(io.BytesIO(image_data)) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img, mask=img.split()[1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as JPEG
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=95)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return img_str
    except Exception as e:
        raise Exception(f"Error encoding image: {str(e)}")

async def process_image(image_data) -> Optional[str]:
    """Process image using Groq's Llama Vision model."""
    try:
        if image_data is None:
            raise ValueError("No image data provided")
            
        # Convert image to base64
        base64_image = await encode_image_to_base64(image_data)
        
        # Prepare the message for Groq API
        message_content: List[Dict[str, Any]] = [
            {
                "type": "text",
                "text": "Analyze the text in the provided image. Extract all readable content and present it in a structured Markdown format that is clear, concise, and well-organized."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]

        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[{
                "role": "user",
                "content": message_content
            }],
            max_tokens=1000,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

async def show_actions():
    """Display action buttons."""
    actions = [
        cl.Action(name="upload", label="Upload Image 📁", value="upload"),
        cl.Action(name="extract", label="Extract Text 🔍", value="extract")
    ]
    await cl.Message(content="Select an action:", actions=actions).send()

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    await cl.Message(
        content="👋 Welcome to Llama OCR! Upload an image and click Extract Text to process it."
    ).send()
    
    await show_actions()

@cl.action_callback("upload")
async def on_upload(action):
    """Handle image upload."""
    files = await cl.AskFileMessage(
        content="Please upload an image file",
        accept=["image/jpeg", "image/png", "image/jpg"],
        max_size_mb=5,
        timeout=180,
    ).send()
    
    if files and len(files) > 0:
        uploaded_file = files[0]
        try:
            # Read the binary content of the file
            with open(uploaded_file.path, 'rb') as f:
                file_content = f.read()
            
            # Store the image data in the session
            cl.user_session.set("uploaded_image", file_content)
            
            # Display the uploaded image
            elements = [
                cl.Image(name="uploaded_image", 
                        display="inline", 
                        content=file_content)
            ]
            
            await cl.Message(
                content=f"✅ Image '{uploaded_file.name}' uploaded successfully! Click 'Extract Text' to process it.",
                elements=elements
            ).send()
            
        except Exception as e:
            await cl.Message(content=f"❌ Error uploading image: {str(e)}").send()
            # Show actions only on error
            await show_actions()

@cl.action_callback("extract")
async def on_extract(action):
    """Handle text extraction from the uploaded image."""
    image_data = cl.user_session.get("uploaded_image")
    
    if not image_data:
        await cl.Message(content="❌ Please upload an image first!").send()
        await show_actions()
        return
        
    try:
        # Show processing message
        await cl.Message(content="🔄 Processing image...").send()
        
        # Process the image using the raw bytes
        result = await process_image(image_data)
        
        # Send results with text only
        await cl.Message(content="✅ Text extracted successfully!").send()
        await cl.Message(content=result).send()
        
        # Show actions after completing the full cycle
        await show_actions()
        
    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
        await show_actions()

if __name__ == "__main__":
    cl.run()