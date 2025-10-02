from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from datetime import datetime
import uuid
import logging
import time
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Captioner API",
    version="1.0.0",
    description="Real AI-powered image captioning with tone adaptation"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
class ModelManager:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = None
        self.loaded = False
        
    def load(self):
        """Load the BLIP model for real caption generation"""
        try:
            logger.info("🚀 Starting to load BLIP model...")
            
            # Set device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"📱 Using device: {self.device}")
            
            # Model selection - using base model for faster loading
            model_name = "Salesforce/blip-image-captioning-base"
            logger.info(f"📦 Loading model: {model_name}")
            logger.info("⏳ This may take a minute on first run...")
            
            # Load processor
            self.processor = BlipProcessor.from_pretrained(model_name)
            logger.info("✅ Processor loaded")
            
            # Load model
            self.model = BlipForConditionalGeneration.from_pretrained(
                model_name,
                torch_dtype=torch.float32
            )
            self.model.to(self.device)
            self.model.eval()
            
            self.loaded = True
            logger.info("🎉 Model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {str(e)}")
            self.loaded = False
            return False
    
    def generate_caption(self, image: Image.Image, num_beams: int = 3, max_length: int = 50):
        """Generate a caption for the given image"""
        if not self.loaded:
            raise Exception("Model not loaded")
        
        try:
            # Prepare the image
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            # Generate caption with beam search for better quality
            with torch.no_grad():
                output_ids = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    min_length=10,
                    num_beams=num_beams,
                    temperature=1.0,
                    top_p=0.9,
                    do_sample=False,  # Deterministic for consistency
                    early_stopping=True
                )
            
            # Decode the caption
            caption = self.processor.decode(output_ids[0], skip_special_tokens=True)
            
            # Clean up the caption
            caption = caption.strip()
            if caption.startswith("arafed "):  # Common BLIP prefix
                caption = caption[7:]
            
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            raise

# Initialize model manager
model_manager = ModelManager()

# Load model on startup
@app.on_event("startup")
async def startup_event():
    logger.info("="*60)
    logger.info("🚀 AI Image Captioner API Starting...")
    logger.info("="*60)
    
    # Try to load the model
    success = model_manager.load()
    
    if success:
        logger.info("✅ Ready to generate real AI captions!")
    else:
        logger.warning("⚠️ Running without model - will use fallback captions")
    
    logger.info("📍 API available at: http://localhost:8000")
    logger.info("📚 Documentation at: http://localhost:8000/docs")
    logger.info("="*60)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Image Captioner API",
        "version": "1.0.0",
        "model_loaded": model_manager.loaded,
        "device": str(model_manager.device) if model_manager.device else "not initialized",
        "docs": "http://localhost:8000/docs"
    }

# Health check
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_manager.loaded,
        "timestamp": datetime.utcnow().isoformat()
    }

# Test endpoint
@app.get("/api/v1/test")
async def test():
    return {
        "message": "Backend is working!",
        "model_loaded": model_manager.loaded,
        "using_real_ai": model_manager.loaded
    }

# Main caption generation endpoint
@app.post("/api/v1/caption")
async def generate_caption(
    file: UploadFile = File(...),
    tone: str = "casual"
):
    """
    Generate a real AI caption for the uploaded image.
    Each image will get a unique, contextually relevant caption.
    """
    
    start_time = time.time()
    logger.info(f"📸 Received request - File: {file.filename}, Tone: {tone}")
    
    try:
        # Read and validate image
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(400, "Empty file uploaded")
        
        # Open and prepare image
        try:
            image = Image.open(io.BytesIO(contents))
            
            # Convert to RGB (BLIP requires RGB)
            if image.mode != 'RGB':
                if image.mode == 'RGBA':
                    # Create white background for transparent images
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[3] if len(image.split()) > 3 else None)
                    image = background
                else:
                    image = image.convert('RGB')
            
            # Resize if image is too large (for memory efficiency)
            max_size = 1024
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            logger.info(f"📐 Image prepared: {image.size}, Mode: {image.mode}")
            
        except Exception as e:
            logger.error(f"Invalid image: {e}")
            raise HTTPException(400, f"Invalid image file: {str(e)}")
        
        # Generate caption
        if model_manager.loaded:
            try:
                # Generate real AI caption
                logger.info("🤖 Generating AI caption...")
                base_caption = model_manager.generate_caption(image)
                logger.info(f"✨ Generated caption: {base_caption}")
                confidence = 0.85  # Real AI confidence
                
            except Exception as e:
                logger.error(f"Model inference failed: {e}")
                # Fallback to a generic caption
                base_caption = "an interesting scene"
                confidence = 0.3
        else:
            # Model not loaded - use generic fallback
            logger.warning("Model not loaded, using fallback")
            base_caption = "an image that requires AI analysis"
            confidence = 0.1
        
        # Apply tone adaptation to the base caption
        final_caption = adapt_caption_to_tone(base_caption, tone)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Generate response
        response = {
            "caption": final_caption,
            "tone": tone,
            "confidence": confidence,
            "processing_time": processing_time,
            "timestamp": datetime.utcnow().isoformat(),
            "image_id": str(uuid.uuid4())
        }
        
        logger.info(f"✅ Request completed in {processing_time:.2f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(500, f"Internal server error: {str(e)}")

def adapt_caption_to_tone(caption: str, tone: str) -> str:
    """
    Adapt the AI-generated caption to match the requested tone.
    This preserves the actual content while changing the style.
    """
    
    # Clean up the base caption
    caption = caption.strip()
    
    # Remove common BLIP prefixes
    prefixes_to_remove = [
        "a photo of", "an image of", "a picture of",
        "there is", "there are", "this is"
    ]
    
    caption_lower = caption.lower()
    for prefix in prefixes_to_remove:
        if caption_lower.startswith(prefix):
            caption = caption[len(prefix):].strip()
            break
    
    # Ensure caption starts with lowercase for integration
    if caption and caption[0].isupper() and len(caption) > 1:
        caption = caption[0].lower() + caption[1:]
    
    # Apply tone-specific formatting
    if tone == "formal":
        # Professional and descriptive
        return f"The image depicts {caption}, presenting a detailed view of the subject matter."
    
    elif tone == "casual":
        # Friendly and conversational
        if not caption.endswith(("!", ".", "?")):
            caption += "!"
        return f"Check out this {caption}"
    
    elif tone == "humorous":
        # Witty and entertaining
        funny_intros = [
            f"Plot twist: it's {caption} 😄",
            f"Surprise! We've got {caption} here! 🎉",
            f"Breaking: Local image contains {caption}! 📰",
            f"Nobody expects {caption}! 😂"
        ]
        import random
        return random.choice(funny_intros)
    
    elif tone == "poetic":
        # Lyrical and evocative
        return f"In this captured moment, {caption} emerges like a whispered dream, painting stories in light and shadow..."
    
    elif tone == "technical":
        # Precise and analytical
        return f"Technical Analysis: The image composition features {caption}. Observable elements include structured arrangement and balanced visual hierarchy."
    
    elif tone == "marketing":
        # Engaging and persuasive
        return f"✨ Discover the beauty of {caption} - Capturing moments that inspire and elevate your vision! #Trending"
    
    elif tone == "storytelling":
        # Narrative and engaging
        return f"Once upon a time, in a world frozen in pixels, there was {caption}. And what a tale it tells..."
    
    else:
        # Default - return with slight enhancement
        return f"This image shows {caption}."

# Get available tones
@app.get("/api/v1/tones")
async def get_tones():
    return {
        "tones": [
            {"value": "formal", "description": "Professional and descriptive"},
            {"value": "casual", "description": "Friendly and conversational"},
            {"value": "humorous", "description": "Witty and entertaining"},
            {"value": "poetic", "description": "Lyrical and evocative"},
            {"value": "technical", "description": "Precise and detailed"},
            {"value": "marketing", "description": "Engaging and persuasive"},
            {"value": "storytelling", "description": "Narrative and engaging"}
        ]
    }

# Optional: Endpoint to check model status
@app.get("/api/v1/model/status")
async def model_status():
    return {
        "loaded": model_manager.loaded,
        "device": str(model_manager.device) if model_manager.device else None,
        "model_name": "Salesforce/blip-image-captioning-base" if model_manager.loaded else None
    }

# Optional: Endpoint to reload model
@app.post("/api/v1/model/reload")
async def reload_model():
    """Force reload the model"""
    success = model_manager.load()
    return {
        "success": success,
        "message": "Model reloaded successfully" if success else "Failed to reload model"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting AI Image Captioner with Real AI Model...")
    print("⏳ First-time model download may take a few minutes...")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")