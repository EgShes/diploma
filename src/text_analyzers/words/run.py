from pathlib import Path

from src.config import words_logger
from src.text_analyzers.runner import Runner
from src.text_analyzers.words.runner import (
    WordAnalyzer,
    WordPostprocessor,
    WordPreprocessor,
    WordResultPublisher,
    WordTextProvider,
)

if __name__ == "__main__":

    preprocessor = WordPreprocessor()
    analyzer = WordAnalyzer.load(Path("weights/words/mystem-3.1-linux-64bit.tar.gz"))
    postprocessor = WordPostprocessor()
    text_provider = WordTextProvider(url="http://app:8000/text/read")
    result_publisher = WordResultPublisher(url="http://app:8000/word/add")

    runner = Runner(preprocessor, analyzer, postprocessor, text_provider, result_publisher)

    words_logger.info("Successfully loaded")
    runner.run()
