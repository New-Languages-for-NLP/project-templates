"""Convert plaintext to spaCy binary format for pretraining"""

from pathlib import Path

import typer
from spacy.tokens import DocBin
from spacy.util import get_lang_class
from spacy.training.converters.conll_ner_to_docs import n_sents_info
from wasabi import msg


def convert(input_path: Path, output_path: Path, n_sents: int, lang: str):
    # make sure the input and output directories exist
    assert input_path.is_dir()
    assert output_path.is_dir()

    # load custom language model and try to add a simple sentencizer if available
    lang = get_lang_class(lang)
    nlp = lang()
    try:
        nlp.add_pipe("sentencizer")
    except Exception:
        pass

    # convert all of the input .txt files to docs
    # if there are sentences, then group every n_sents sentences into a doc
    # otherwise, just use the whole file as a single doc
    db = DocBin()
    text_files = list(input_path.glob("*.txt"))
    for text_file in text_files:
        doc = nlp(text_file.read_text())
        try:
            sentences = list(doc.sents)
            total_sentences = len(sentences)
            docs_added = 0
            n_sents_info(msg, n_sents)
            for i in range(0, total_sentences, n_sents):
                start_sentence = sentences[i]
                end_sentence = sentences[min(i + n_sents - 1, total_sentences - 1)]
                sentence_span = doc[start_sentence.start : end_sentence.end]
                db.add(sentence_span.as_doc())
                docs_added += 1
            msg.good(
                f"Converted raw text file ({docs_added} documents): {text_file.resolve()}"
            )
        except ValueError:
            msg.warn(
                f"No sentence segmentation available. Using whole file as a document."
            )
            db.add(doc)
            msg.good(f"Converted raw text file (1 document): {text_file.resolve()}")

    # save the DocBin to disk
    msg.info(f"Grouping {len(text_files)} files into a pretraining corpus.")
    out_file_path = (output_path / "pretrain.spacy").resolve()
    db.to_disk(out_file_path)
    msg.good(f"Generated pretraining corpus ({len(db)} documents): {out_file_path}")


if __name__ == "__main__":
    typer.run(convert)
