import src.text_analyzers.sentiment.runner as runner_module
from src.text_analyzers.common import Meta
from src.text_analyzers.sentiment.schemas import SentimentType


def test_preprocessor_init(sentiment_preprocessor):
    pass


def test_analyzer_init(sentiment_analyzer):
    pass


def test_postprocessor_init(sentiment_postprocessor):
    pass


def test_publisher_init(sentiment_publisher):
    pass


def test_runner_init(sentiment_runner):
    pass


def test_analyze(sentiment_runner, analyzer_input):
    processed = sentiment_runner.analyze_text(analyzer_input)
    assert isinstance(processed.probability, float)
    assert isinstance(processed.type, SentimentType)


def test_publish(monkeypatch, requests_mock, sentiment_publisher, sentiment_runner, analyzer_input):
    monkeypatch.setattr(runner_module, "requests", requests_mock)

    result = sentiment_runner.analyze_text(analyzer_input)
    sentiment_publisher.publish(result, Meta(id=1))

    requests_mock.post.assert_called()
