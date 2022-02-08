from pathlib import Path

from src.config import words_logger
from src.queues.queues_config import routing_config
from src.text_analyzers.runner import Runner
from src.text_analyzers.words.runner import (
    WordAnalyzer,
    WordPostprocessor,
    WordPreprocessor,
    WordResultPublisher,
)

if __name__ == "__main__":

    preprocessor = WordPreprocessor()
    analyzer = WordAnalyzer.load(Path("weights/words/mystem-3.1-linux-64bit.tar.gz"))
    postprocessor = WordPostprocessor()
    result_publisher = WordResultPublisher(url="http://app:8000/word/add/")

    runner = Runner(preprocessor, analyzer, postprocessor, result_publisher)

    words_logger.info("Successfully loaded")
    runner.start_consuming(routing_config.word_queue.queue)
