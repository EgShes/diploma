import asyncio
from typing import Dict, List

import aiohttp
from pydantic import parse_obj_as

from src.config import DispatcherConfig, RabbitConfig, dev_logger
from src.dispatcher.schemas import Message, Payload, SourceText
from src.queues.connector import RabbitConnector
from src.queues.queues_config import queues_config, routing_config


def create_message(content: List[Dict[str, str]]) -> Message:
    return Message(payload=Payload(source_texts=parse_obj_as(List[SourceText], content)))


async def dispatch(data_url: str, batch_size: int, exchange: str, routing_key: str, sleep: int):

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(data_url, params={"n": batch_size}) as resp:
                content = await resp.json()

                message = create_message(content)

                channel = RabbitConnector(RabbitConfig.url, queues_config).get_channel()
                channel.basic_publish(exchange, routing_key, message.json())
                dev_logger.debug(f"Published to {exchange} with key {routing_key}")

            await asyncio.sleep(sleep)


async def words_dispatcher():
    await dispatch(
        data_url="http://app:8000/word/for_processing",
        batch_size=DispatcherConfig.words_batch,
        exchange=routing_config.word_queue.exchange,
        routing_key=routing_config.word_queue.routing_key,
        sleep=DispatcherConfig.words_sleep,
    )


async def named_entity_dispatcher():
    await dispatch(
        data_url="http://app:8000/named_entity/for_processing",
        batch_size=DispatcherConfig.named_entities_batch,
        exchange=routing_config.ner_queue.exchange,
        routing_key=routing_config.ner_queue.routing_key,
        sleep=DispatcherConfig.named_entities_sleep,
    )


async def sentiment_dispatcher():
    await dispatch(
        data_url="http://app:8000/sentiment/for_processing",
        batch_size=DispatcherConfig.sentiments_batch,
        exchange=routing_config.sentiment_queue.exchange,
        routing_key=routing_config.sentiment_queue.routing_key,
        sleep=DispatcherConfig.sentiments_sleep,
    )
