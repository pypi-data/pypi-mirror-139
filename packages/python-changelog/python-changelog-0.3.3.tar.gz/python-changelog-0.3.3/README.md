# Changelog Generator

A module that generates changelogs based on git tags.
It uses conventional commits ([conventionalcommits.org](https://www.conventionalcommits.org)) to read and scope commits.
Markdown is used for formating.

## Commands

**$ pychangelog generate** [\<path>] [--branch=\<string>] [--types=\<list>] [--bodytags=\<list>]

* generates new CHANGELOG.md file at the repo root
* overrides old CHANGELOG.md

**$ pychangelog add** [\<path>] [--branch=\<string>] [--types=\<list>] [--bodytags=\<list>]

* keeps the content of old CHANGELOG.md while appending new versions

**$ pychangelog printout** [\<path>] [--branch=\<string>] [--types=\<list>] [--bodytags=\<list>]

* prints the generated changelog in the terminal instead of writing it in the CHANGELOG.md
* does not touch CHANGELOG.md

## Options

Option | Format | Description | Default
--- | --- | --- | ---
path | TEXT | path to root of the git repository | .
--branch | TEXT | git branch | main
--types | TEXT comma seperated list | commit types to show in changelog | feat,fix,chore,docs,refactor,test
--bodytags | TEXT comma seperated list | body tags that schould be shown in changelog | BREAKING CHANGE,MAJOR

## Instalation

You can install the changelog generator via PyPI:

`pip install python-changelog`
