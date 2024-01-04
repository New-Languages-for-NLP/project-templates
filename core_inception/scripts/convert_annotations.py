"""Load INCEpTION annotations and convert to spaCy binary format (DocBin)"""

from pathlib import Path
import subprocess
import tempfile
import os

import typer
from spacy.tokens import DocBin
from spacy.util import get_lang_class
from wasabi import msg


def convert(
    input_path: Path,
    output_path: Path,
    n_sents: int,
    lang: str,
):
    # make sure the input and output directories exist
    assert input_path.is_dir()
    assert output_path.is_dir()

    # load custom language model for its vocab
    lang = get_lang_class(lang)
    nlp = lang()

    # keep track of all the input files
    conllu_files = []
    conll_files = []

    # convert all of the input files in a temporary directory
    tmpdir_handle = tempfile.TemporaryDirectory()
    tmpdir = Path(tmpdir_handle.name)
    os.mkdir(tmpdir / "conllu")
    os.mkdir(tmpdir / "conll")
    for conllu_file in input_path.glob("*.conllu"):
        conllu_files.append(conllu_file)
        subprocess.run(
            [
                "python",
                "-m",
                "spacy",
                "convert",
                conllu_file,
                tmpdir / "conllu",
                f"-n {n_sents}",
            ]
        )
    for conll_file in input_path.glob("*.conll"):
        conll_files.append(conll_file)
        subprocess.run(
            [
                "python",
                "-m",
                "spacy",
                "convert",
                conll_file,
                tmpdir / "conll",
                f"-n {n_sents}",
            ]
        )

    # figure out which files have both conllu and conll versions
    conllu_filenames = set([f.stem for f in conllu_files])
    conll_filenames = set([f.stem for f in conll_files])
    all_filenames = conllu_filenames | conll_filenames
    matched_filenames = conllu_filenames & conll_filenames

    # if the file has both conllu and conll versions, join them, otherwise copy
    msg.info(f"Grouping {len(all_filenames)} files into a corpus.")
    out_docs = DocBin()
    for filename in all_filenames:
        if filename in matched_filenames:
            conllu_docs = list((
                DocBin()
                .from_disk(tmpdir / "conllu" / f"{filename}.spacy")
                .get_docs(nlp.vocab)
            ))
            conll_docs = list((
                DocBin()
                .from_disk(tmpdir / "conll" / f"{filename}.spacy")
                .get_docs(nlp.vocab)
            ))
            for base_doc, ner_doc in zip(conllu_docs, conll_docs):
                base_doc.ents = ner_doc.ents
                out_docs.add(base_doc)
            msg.info(
                f"Combined '{filename}.conllu' and '{filename}.conll' ({len(conllu_docs)} docs)"
            )
        else:
            if filename in conllu_filenames:
                file = tmpdir / "conllu" / f"{filename}.spacy"
            if filename in conll_filenames:
                file = tmpdir / "conll" / f"{filename}.spacy"
            docs = list(DocBin().from_disk(file).get_docs(nlp.vocab))
            for doc in docs:
                out_docs.add(doc)

    # write the combined corpus to disk
    out_docs.to_disk(output_path / "all.spacy")
    msg.good(f"Generated corpus ({len(out_docs)} documents): {output_path / 'all.spacy'}")

    # cleanup temporary directory
    tmpdir_handle.cleanup()


if __name__ == "__main__":
    typer.run(convert)
