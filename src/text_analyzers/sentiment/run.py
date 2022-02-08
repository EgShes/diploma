from pathlib import Path

from src.queues.queues_config import routing_config
from src.text_analyzers.runner import Runner
from src.text_analyzers.sentiment.runner import (
    SentimentAnalyzer,
    SentimentPostprocessor,
    SentimentPreprocessor,
    SentimentResultPublisher,
)

if __name__ == "__main__":

    preprocessor = SentimentPreprocessor()
    analyzer = SentimentAnalyzer.load(Path("weights/sentiment/fasttext-social-network-model.bin"))
    postprocessor = SentimentPostprocessor()
    result_publisher = SentimentResultPublisher(url="http://app:8000/sentiment/add/")

    runner = Runner(preprocessor, analyzer, postprocessor, result_publisher)
    runner.start_consuming(routing_config.sentiment_queue.queue)
