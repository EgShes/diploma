from pathlib import Path

from src.text_analyzers.runner import Runner
from src.text_analyzers.sentiment.runner import (
    SentimentAnalyzer,
    SentimentPostprocessor,
    SentimentPreprocessor,
    SentimentResultPublisher,
    SentimentTextProvider,
)

if __name__ == "__main__":

    preprocessor = SentimentPreprocessor()
    analyzer = SentimentAnalyzer.load(Path("weights/sentiment/fasttext-social-network-model.bin"))
    postprocessor = SentimentPostprocessor()
    text_provider = SentimentTextProvider(url="http://app:8000/text")
    result_publisher = SentimentResultPublisher(url="http://app:8000/sentiment")

    runner = Runner(preprocessor, analyzer, postprocessor, text_provider, result_publisher)

    runner.run()
