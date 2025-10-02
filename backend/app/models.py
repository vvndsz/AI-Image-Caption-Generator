from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List
from datetime import datetime

class ToneEnum(str, Enum):
    formal = "formal"
    casual = "casual"
    humorous = "humorous"
    poetic = "poetic"
    technical = "technical"
    marketing = "marketing"
    storytelling = "storytelling"

class CaptionRequest(BaseModel):
    tone: ToneEnum = Field(default=ToneEnum.casual)
    additional_context: Optional[str] = None
    max_length: Optional[int] = Field(default=50, ge=10, le=200)

class CaptionResponse(BaseModel):
    caption: str
    tone: ToneEnum
    confidence: float
    processing_time: float
    timestamp: datetime
    image_id: str

class BatchCaptionRequest(BaseModel):
    images: List[str]  # Base64 encoded images
    tone: ToneEnum = Field(default=ToneEnum.casual)

class SocialMediaIntegration(BaseModel):
    platform: str
    caption: str
    hashtags: List[str]
    scheduled_time: Optional[datetime] = None