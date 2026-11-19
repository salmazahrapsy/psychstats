# PsychStats

**An open, evidence-informed project on psychology and psychological statistics — with the code that keeps it reproducible.**

Maintained by [Salma Zahra](https://salmazahrapsy.github.io/), Psychology undergraduate, Indonesia.

[![Ecosystem CI/CD](https://github.com/salmazahrapsy/psychstats/actions/workflows/wiki-sync.yml/badge.svg)](https://github.com/salmazahrapsy/psychstats/actions/workflows/wiki-sync.yml)

## What is here

| Part | What it does | Where |
| --- | --- | --- |
| Knowledge pages | Short reference articles on psychology, psychological statistics, psychotherapy and mental health, written to shared templates | `*.md` at the root, `templates/` |
| Schema validation | Checks metadata against a Dublin Core mapping and a schema.org template before anything is published | `pipelines/schema_validator.py`, `config/` |
| Data processing | Normalises datasets (z-scores, min–max) and records every transformation | `src/processing/` |
| Assessment generator | Turns content into Moodle XML and Aiken question banks tagged by Bloom's taxonomy level | `pipelines/moodle_generator.py`, `data/assessments/` |
| Case study | Emotion in 5,400 Indonesian product reviews — clothing vs other categories | `analysis/prdect_case_study.py` |
| Wiki sync | Publishes selected pages to the PsychStats wiki | `src/utils/sync_to_wiki.py` |
| Tests and CI | Pytest suite run on every push by GitHub Actions; credentials come only from GitHub Secrets | `tests/`, `.github/workflows/` |

## Quick start

```bash
pip install -r requirements.txt
pytest -q                                  # run the tests
python pipelines/schema_validator.py       # validate metadata
python analysis/prdect_case_study.py       # reproduce the review case study
```

## Case study: what disappoints online clothing buyers?

Using the PRDECT-ID dataset, negative reviews in four clothing categories mention "not as described / unlike the photo" (27.8% vs 14.0%), fabric (23.2% vs 6.4%), colour (16.8% vs 3.9%) and size or fit (13.5% vs 5.2%) far more than other categories, and delivery less (22.8% vs 31.5%); all p < .001. Full write-up, interpretation and limitations: <https://salmazahrapsy.github.io/business-behaviour/>.

## Principles

1. Distinguish **evidence**, **interpretation** and **hypothesis**.
2. Cite authoritative sources; prefer DOIs.
3. Educational content only — not a substitute for individual professional assessment or care.
4. No secrets in the repository: API keys live in GitHub Secrets or environment variables.

## Data

See [`data/README.md`](data/README.md) for sources and licences.

## Contributing and citation

See [CONTRIBUTING.md](CONTRIBUTING.md). To cite this project, use [CITATION.cff](CITATION.cff). Code is MIT-licensed.
