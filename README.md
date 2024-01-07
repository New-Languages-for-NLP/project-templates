<!-- adapted from https://github.com/explosion/projects/blob/v3/README.md -->

<a href="https://newnlp.princeton.edu/"><img src="https://new-languages-for-nlp.github.io/course-materials/_static/logo.svg" width="125" height="125" align="right" /></a>

# 🪐 Project Templates

[Weasel](https://github.com/explosion/weasel), previously
[spaCy projects](https://spacy.io/usage/projects), lets you manage and share
**end-to-end workflows** for different **use cases and domains**, and
orchestrate training, packaging and serving your custom pipelines. You can start
off by cloning a pre-defined project template, adjust it to fit your needs, load
in your data, train a pipeline, export it as a Python package, and share your results with other researchers.

This repository contains starter templates published by the New Languages for NLP team aimed at researchers in the humanities who are interested in using spaCy for their projects, especially those who are working in languages not currently supported by spaCy and other NLP tools.

> ⓘ These project templates require
> [Weasel](https://github.com/explosion/weasel), which is **included by
> default** with spaCy v3.7+. Just install spaCy via pip with
> `pip install spacy` and you're ready to get started. Make
> sure to use a fresh virtual environment.

[![tests](https://github.com/New-Languages-for-NLP/project-templates/actions/workflows/tests.yml/badge.svg)](https://github.com/New-Languages-for-NLP/project-templates/actions/workflows/tests.yml)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![spaCy](https://img.shields.io/static/v1?label=made%20with%20%E2%9D%A4%20and&message=spaCy&color=09a3d5&style=flat-square)](https://spacy.io)

## 🗃 Templates

| Template                           | Description                                            |
| ---------------------------------- | ------------------------------------------------------ |
| [`core_inception`](core_inception) | Train new language core model with Cadet and INCEpTION |

## 🚀 Quickstart

Projects can be used via the
[`weasel`](https://github.com/explosion/weasel/blob/main/docs/cli.md) CLI, or
through the [`spacy project`](https://spacy.io/api/cli#project) alias. To find
out more about a command, add `--help`. For detailed instructions, see the
[Weasel documentation](https://github.com/explosion/weasel/tree/main#-documentation)
or [spaCy projects usage guide](https://spacy.io/usage/projects).

1. **Clone** the project template you want to use.
   ```bash
   spacy project clone core_inception my_new_project --repo https://github.com/New-Languages-for-NLP/project-templates
   ```
2. **Install** any project requirements.
   ```bash
   cd my_new_project
   python -m pip install -r requirements.txt
   ```
3. **Fetch assets** (data, weights) defined in the `project.yml`.
   ```bash
   spacy project assets
   ```
4. **Run a command** defined in the `project.yml`.
   ```bash
   spacy project run preprocess
   ```
5. **Run a workflow** of multiple steps in order.
   ```bash
   spacy project run all
   ```
6. **Adjust** the template for **your specific use case**, load in your own
   data, adjust the settings and model, and publish your results.

## 👷‍♀️Repository maintanance

To keep the project templates and their documentation up to date, this repo
contains several scripts:

| Script                                                         | Description                                                                                                                                                                                                               |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`update_docs.py`](.github/update_docs.py)                     | Update all auto-generated docs in the given root. Calls into [`spacy project document`](https://spacy.io/api/cli#project-document) and only replaces the auto-generated sections, not any custom content before or after. |
| [`update_configs.py`](.github/update_configs.py)               | Update and auto-fill all `config.cfg` files included in the repo, similar to [`spacy init fill-config`](https://spacy.io/api/cli#init-fill-config). Can be used to keep the configs up to date with changes in spaCy.     |
| [`update_projects_jsonl.py`](.github/update_projects_jsonl.py) | Update `projects.jsonl` file in the given root. Should be used at the root level of the repo.                                                                                                                             |

---

_This README and several of the scripts were adapted from the main [explosion projects repository](https://github.com/explosion/projects/)._
