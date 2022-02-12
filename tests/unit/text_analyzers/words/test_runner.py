import src.text_analyzers.words.runner as runner_module
from src.text_analyzers.common import Meta


def test_preprocessor_init(word_preprocessor):
    pass


def test_analyzer_init(word_analyzer):
    pass


def test_postprocessor_init(word_postprocessor):
    pass


def test_publisher_init(word_publisher):
    pass


def test_runner_init(word_runner):
    pass


def test_analyze(word_runner, analyzer_input):
    processed = word_runner.analyze_text(analyzer_input)
    assert isinstance(processed, list)
    assert len(processed) != 0
    for word in processed:
        assert isinstance(word.text, str)
        assert isinstance(word.quantity, int)


def test_publish(monkeypatch, requests_mock, word_publisher, word_runner, analyzer_input):
    monkeypatch.setattr(runner_module, "requests", requests_mock)

    result = word_runner.analyze_text(analyzer_input)
    word_publisher.publish(result, Meta(id=1))

    requests_mock.post.assert_called()
