# Dashboard Final Project - Hanif Ismail

This is a Streamlit application for my final project.

## Setup Environment

### Anaconda

```bash
conda create --name my-dashboard-env python=3.9
conda activate my-dashboard-env
pip install -r requirements.txt
```

### Shell/Terminal

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Set NGROK_AUTH_TOKEN
Make sure to set your NGROK_AUTH_TOKEN in the environment variable for local testing:
```bash
export NGROK_AUTH_TOKEN="your_ngrok_auth_token_here"
```

## Run Streamlit App
```bash
streamlit run Python.py
```
