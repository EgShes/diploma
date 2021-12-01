from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel

config_path = Path(__file__).resolve().parent / "queues_config.yml"


class BindingSchema(BaseModel):
    exchange: str
    queue: str
    routing_key: str


class ExchangeSchema(BaseModel):
    name: str
    durable: bool
    type: str


class QueueSchema(BaseModel):
    name: str
    durable: bool
    arguments: Optional[Dict[str, Any]]


class RabbitConfigSchema(BaseModel):
    exchanges: List[ExchangeSchema]
    queues: List[QueueSchema]
    bindings: List[BindingSchema]


class RouteParams(BaseModel):
    queue: str
    exchange: str
    routing_key: str


class RoutingConfig(BaseModel):
    ner_queue: RouteParams = RouteParams(queue="ner", exchange="input", routing_key="ner")
    sentiment_queue: RouteParams = RouteParams(queue="sentiment", exchange="input", routing_key="sentiment")
    word_queue: RouteParams = RouteParams(queue="word", exchange="input", routing_key="word")


with config_path.open("r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

queues_config = RabbitConfigSchema(**config)
routing_config = RoutingConfig()
