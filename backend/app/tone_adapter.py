import openai
from typing import Dict, Any, Optional
import logging
from .config import settings
from .models import ToneEnum

logger = logging.getLogger(__name__)

class ToneAdapter:
    def __init__(self):
        self.use_openai = settings.use_openai_for_tone and settings.openai_api_key
        if self.use_openai:
            openai.api_key = settings.openai_api_key
        
        self.tone_templates = {
            ToneEnum.formal: {
                "prefix": "The image depicts",
                "style": "professional and descriptive",
                "example": "The image depicts a serene landscape featuring..."
            },
            ToneEnum.casual: {
                "prefix": "Check out this",
                "style": "friendly and conversational",
                "example": "Check out this awesome sunset over the mountains!"
            },
            ToneEnum.humorous: {
                "prefix": "Plot twist:",
                "style": "witty and entertaining",
                "example": "Plot twist: The cat is actually the one training the human!"
            },
            ToneEnum.poetic: {
                "prefix": "In this moment captured,",
                "style": "lyrical and evocative",
                "example": "In this moment captured, nature's symphony plays..."
            },
            ToneEnum.technical: {
                "prefix": "Analysis:",
                "style": "precise and detailed",
                "example": "Analysis: The composition features a rule-of-thirds layout..."
            },
            ToneEnum.marketing: {
                "prefix": "Discover",
                "style": "engaging and persuasive",
                "example": "Discover the perfect blend of style and comfort..."
            },
            ToneEnum.storytelling: {
                "prefix": "Once upon a time,",
                "style": "narrative and engaging",
                "example": "Once upon a time, in a garden where colors danced..."
            }
        }
    
    def adapt_caption_with_llm(
        self, 
        base_caption: str, 
        tone: ToneEnum
    ) -> str:
        """Use OpenAI API to adapt caption to specified tone"""
        if not self.use_openai:
            return self.adapt_caption_with_rules(base_caption, tone)
        
        try:
            prompt = f"""
            Transform this image caption to have a {tone.value} tone.
            Original caption: "{base_caption}"
            
            Guidelines for {tone.value} tone:
            - Style: {self.tone_templates[tone]['style']}
            - Example start: {self.tone_templates[tone]['example']}
            
            Provide only the adapted caption, nothing else.
            """
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative caption writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self.adapt_caption_with_rules(base_caption, tone)
    
    def adapt_caption_with_rules(
        self, 
        base_caption: str, 
        tone: ToneEnum
    ) -> str:
        """Rule-based caption adaptation without LLM"""
        template = self.tone_templates.get(tone, self.tone_templates[ToneEnum.casual])
        
        # Remove common starting words
        cleaned_caption = base_caption.lower()
        for word in ["a", "an", "the", "this"]:
            if cleaned_caption.startswith(word + " "):
                base_caption = base_caption[len(word)+1:]
                break
        
        if tone == ToneEnum.formal:
            return f"{template['prefix']} {base_caption}."
        
        elif tone == ToneEnum.casual:
            # Add excitement
            if not base_caption.endswith(("!", "?")):
                base_caption += "!"
            return f"{template['prefix']} {base_caption}"
        
        elif tone == ToneEnum.humorous:
            # Add humor elements
            humor_additions = [
                "Plot twist: ",
                "Meanwhile, ",
                "Spoiler alert: ",
                "Breaking news: "
            ]
            import random
            prefix = random.choice(humor_additions)
            return f"{prefix}{base_caption} 😄"
        
        elif tone == ToneEnum.poetic:
            # Make it more lyrical
            words = base_caption.split()
            if len(words) > 3:
                return f"{template['prefix']} {' '.join(words[:3])},\n" \
                       f"Where {' '.join(words[3:])} unfolds..."
            return f"{template['prefix']} {base_caption}..."
        
        elif tone == ToneEnum.technical:
            return f"{template['prefix']} {base_caption}. " \
                   f"Technical details: Composition analysis pending."
        
        elif tone == ToneEnum.marketing:
            return f"✨ {template['prefix']} {base_caption} - " \
                   f"Your perfect choice awaits!"
        
        elif tone == ToneEnum.storytelling:
            return f"{template['prefix']} there was {base_caption}. " \
                   f"And the story continues..."
        
        return base_caption
    
    def generate_hashtags(self, caption: str, tone: ToneEnum) -> list:
        """Generate relevant hashtags based on caption and tone"""
        # Extract key words (simple implementation)
        words = caption.lower().split()
        
        # Filter common words
        common_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at"}
        keywords = [w.strip(".,!?") for w in words if w not in common_words][:5]
        
        # Tone-specific hashtags
        tone_tags = {
            ToneEnum.formal: ["#professional", "#business"],
            ToneEnum.casual: ["#daily", "#life"],
            ToneEnum.humorous: ["#funny", "#lol"],
            ToneEnum.poetic: ["#poetry", "#artistic"],
            ToneEnum.technical: ["#tech", "#analysis"],
            ToneEnum.marketing: ["#product", "#trending"],
            ToneEnum.storytelling: ["#story", "#narrative"]
        }
        
        hashtags = [f"#{kw}" for kw in keywords[:3]]
        hashtags.extend(tone_tags.get(tone, []))
        
        return hashtags[:5]  # Limit to 5 hashtags