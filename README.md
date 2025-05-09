## install dependency for utils/qa.chain.py
pip install langchain faiss-cpu sentence-transformers python-dotenv requests

pip install pypdf

pip install streamlit

## How to start app, home.py is the homepage
Run "streamlit run home.py" to start the app.

## Model kpi key
The key is stored in .env, using deepseek model from Openrouter
so you need to create a file called .env and write:
OPENROUTER_API_KEY= "sk-or-v1..."
