from enum import Enum

from pydantic import BaseModel


class SentimentType(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"
    speech = "speech"
    skip = "skip"


class Sentiment(BaseModel):
    probability: float
    type: SentimentType
