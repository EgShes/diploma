import src.text_analyzers.ner.runner as runner_module
from src.text_analyzers.common import Meta
from src.text_analyzers.ner.schemas import EntityType


def test_preprocessor_init(ner_preprocessor):
    pass


def test_analyzer_init(ner_analyzer):
    pass


def test_postprocessor_init(ner_postprocessor):
    pass


def test_publisher_init(ner_publisher):
    pass


def test_runner_init(ner_runner):
    pass


def test_analyze(ner_runner, analyzer_input):
    processed = ner_runner.analyze_text(analyzer_input)
    assert isinstance(processed.entities, list)
    assert len(processed.entities) != 0
    for entity in processed.entities:
        assert isinstance(entity.text, str)
        assert isinstance(entity.type, EntityType)


def test_publish(monkeypatch, requests_mock, ner_publisher, ner_runner, analyzer_input):
    monkeypatch.setattr(runner_module, "requests", requests_mock)

    result = ner_runner.analyze_text(analyzer_input)
    ner_publisher.publish(result, Meta(id=1))

    requests_mock.post.assert_called()
