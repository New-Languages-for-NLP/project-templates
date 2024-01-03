from setuptools import setup

setup(
    name="zxx",
    entry_points={
        "spacy_languages": ["zxx = zxx:NewLanguage"],
    },
)
