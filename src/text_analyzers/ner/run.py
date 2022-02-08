from pathlib import Path

from src.config import ner_logger
from src.queues.queues_config import routing_config
from src.text_analyzers.ner.runner import (
    NerAnalyzer,
    NerPostprocessor,
    NerPreprocessor,
    NerResultPublisher,
)
from src.text_analyzers.runner import Runner

if __name__ == "__main__":
    preprocessor = NerPreprocessor()
    analyzer = NerAnalyzer.load(
        Path("weights/ner/navec_news_v1_1B_250K_300d_100q.tar"),
        Path("weights/ner/slovnet_ner_news_v1.tar"),
    )
    postprocessor = NerPostprocessor()
    result_publisher = NerResultPublisher(url="http://app:8000/named_entity/add/")

    ner_runner = Runner(preprocessor, analyzer, postprocessor, result_publisher)

    ner_logger.info("Successfully loaded")
    ner_runner.start_consuming(routing_config.ner_queue.queue)
