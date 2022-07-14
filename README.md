# Image Data Generator

[![GitHub](https://img.shields.io/badge/github-img_data_gen-yellow.svg)](https://github.com/SvenBecker/img_data_gen)
[![Python Version](https://img.shields.io/badge/python-3.9%20|%203.10-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-pylint-black.svg)](https://pylint.pycqa.org)

## Prerequisites

- Python 3.9+
- Poetry

## Getting Started

Clone the project via `git clone https://github.com/SvenBecker/img_data_gen.git`.

Enter the project folder via `cd img_data_gen`, install required dependencies via `poetry install` and activate
the virtual environment Poetry created via `poetry shell`.

After having installed all required dependencies you can run `python -m img_data_gen --samples 10` to generate
10 image samples given the default locations for input and background image data, which will be saved to 
the `./output` folder by default.

> See also: Check `python -m img_data_gen --help` to get some insights about what options are currently supported.

## Dev Workflow

Run linting via `pylint img_data_gen` and type checks via `mypy`.
