import asyncio

from src.dispatcher.tasks import (
    named_entity_dispatcher,
    sentiment_dispatcher,
    words_dispatcher,
)


async def main():
    tasks = [words_dispatcher(), named_entity_dispatcher(), sentiment_dispatcher()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
