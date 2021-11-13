from pathlib import Path

from src.text_analyzers.ner.runner import NerAnalyzer, NerPostprocessor, NerPreprocessor

if __name__ == "__main__":
    text = (
        "Кипиево — село в Ижемском районе Республики Коми (Россия). "
        "Административный центр одноимённого сельского поселения."
    )

    pre = NerPreprocessor.load()
    anal = NerAnalyzer.load(
        navec_embeddings_path=Path("/home/egor/Downloads/navec_news_v1_1B_250K_300d_100q.tar"),
        ner_model_path=Path("/home/egor/Downloads/slovnet_ner_news_v1.tar"),
    )
    post = NerPostprocessor.load()

    x = pre.preprocess(text)
    x = anal.analyze(x)
    x = post.postprocess(x)

    print(x.entities)
    print(set(x.entities))
