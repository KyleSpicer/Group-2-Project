# Group-2-Project

Group 2 Project repository for CTU's CS492 Final Project

## Table of Contents
1. [Starting Virtual Environment](#starting-virtual-environment)
1. [Run Bookstore App](#run-bookstore-app)
1. [References](#references)

## Starting Virtual Environment

1. Open terminal and ensure Python 3.10+ is installed. To verify, enter `python --version or python3 --version`
1. Clone the repository from GitHub, `git clone git@github.com:KyleSpicer/Group-2-Project.git`
1. Change directories to the top-level of the project repository: `cd Group-2-Project/`
1. Create virtual environment: `python -m venv my_venv`
1. Activate virtual environment: `source my_venv/bin/activate`
1. Update environment: `pip install -r requirements.txt`
1. Deactivate venv: `deactivate`

## Run Bookstore App

1. From inside the virtual environment, run the following command: `python src/main.py`
1. This will start the flask application at `http://127.0.0.1:5000`

## References

1. Dataset was retrieved from https://www.kaggle.com/datasets/sbonelondhlazi/bookstore-dataset.