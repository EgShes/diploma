import logging
from pathlib import Path

from src.text_analyzers.ner.runner import (
    NerAnalyzer,
    NerPostprocessor,
    NerPreprocessor,
    NerResultPublisher,
    NerTextProvider,
)
from src.text_analyzers.runner import Runner

if __name__ == "__main__":
    preprocessor = NerPreprocessor()
    analyzer = NerAnalyzer.load(
        Path("weights/ner/navec_news_v1_1B_250K_300d_100q.tar"),
        Path("weights/ner/slovnet_ner_news_v1.tar"),
    )
    postprocessor = NerPostprocessor()
    text_provider = NerTextProvider(url="http://app:8000/text")
    result_publisher = NerResultPublisher(url="http://app:8000/named_entity")

    ner_runner = Runner(preprocessor, analyzer, postprocessor, text_provider, result_publisher)

    logging.info("Working")
    ner_runner.run()
