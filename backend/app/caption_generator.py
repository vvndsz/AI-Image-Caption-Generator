import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import time
import hashlib
import json
from typing import Optional, Dict, Any
import redis
import logging
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptionGenerator:
    def __init__(self):
        self.device = torch.device(settings.device if torch.cuda.is_available() else "cpu")
        self.processor = None
        self.model = None
        self.redis_client = None
        self._initialize_model()
        self._initialize_cache()
    
    def _initialize_model(self):
        """Initialize the BLIP model for image captioning"""
        try:
            logger.info(f"Loading model: {settings.model_name}")
            self.processor = BlipProcessor.from_pretrained(settings.model_name)
            self.model = BlipForConditionalGeneration.from_pretrained(
                settings.model_name
            ).to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def _initialize_cache(self):
        """Initialize Redis cache for storing generated captions"""
        try:
            self.redis_client = redis.from_url(settings.redis_url)
            self.redis_client.ping()
            logger.info("Redis cache initialized")
        except Exception as e:
            logger.warning(f"Redis not available: {e}. Continuing without cache.")
            self.redis_client = None
    
    def _get_image_hash(self, image: Image.Image) -> str:
        """Generate a hash for the image for caching purposes"""
        img_bytes = image.tobytes()
        return hashlib.md5(img_bytes).hexdigest()
    
    def _get_cached_caption(self, image_hash: str, tone: str) -> Optional[str]:
        """Retrieve cached caption if available"""
        if not self.redis_client:
            return None
        
        try:
            cache_key = f"caption:{image_hash}:{tone}"
            cached = self.redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Cache retrieval error: {e}")
        
        return None
    
    def _cache_caption(self, image_hash: str, tone: str, caption_data: Dict[str, Any]):
        """Cache the generated caption"""
        if not self.redis_client:
            return
        
        try:
            cache_key = f"caption:{image_hash}:{tone}"
            self.redis_client.setex(
                cache_key,
                settings.cache_ttl,
                json.dumps(caption_data)
            )
        except Exception as e:
            logger.warning(f"Cache storage error: {e}")
    
    def generate_base_caption(self, image: Image.Image) -> Dict[str, Any]:
        """Generate a base caption for the image using BLIP"""
        start_time = time.time()
        
        # Check cache first
        image_hash = self._get_image_hash(image)
        cached = self._get_cached_caption(image_hash, "base")
        if cached:
            logger.info("Using cached base caption")
            return cached
        
        # Prepare image for model
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        
        # Generate caption
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=settings.max_length,
                min_length=settings.min_length,
                num_beams=4,
                temperature=0.8,
                do_sample=False
            )
        
        # Decode caption
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        
        # Calculate confidence (using perplexity as a proxy)
        with torch.no_grad():
            outputs = self.model(**inputs, labels=output)
            confidence = torch.exp(-outputs.loss).item()
            confidence = min(confidence / 100, 1.0)  # Normalize to 0-1
        
        processing_time = time.time() - start_time
        
        result = {
            "caption": caption,
            "confidence": confidence,
            "processing_time": processing_time,
            "image_hash": image_hash
        }
        
        # Cache the result
        self._cache_caption(image_hash, "base", result)
        
        return result
    
    def generate_contextual_caption(
        self, 
        image: Image.Image, 
        context: str
    ) -> Dict[str, Any]:
        """Generate caption with additional context"""
        base_result = self.generate_base_caption(image)
        
        # Prepare contextual prompt
        prompt = f"{context}. "
        inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=settings.max_length,
                min_length=settings.min_length,
                num_beams=4,
                temperature=0.8
            )
        
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        
        return {
            **base_result,
            "caption": caption,
            "context": context
        }