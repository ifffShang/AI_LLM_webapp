## install dependency for utils/qa.chain.py
pip install langchain faiss-cpu sentence-transformers python-dotenv requests

pip install pypdf

pip install streamlit

## Model kpi key
The key is stored in .env, using deepseek model from Openrouter
so you need to create a file called .env and write:
OPENROUTER_API_KEY= "sk-or-v1..."
place the .env file under the same root as home.py

## How to start app, home.py is the homepage
Run "streamlit run home.py" to start the app.

## Questions you can ask, examples:
What are the major symbols in The Great Gatsby

Tell me about the women characters in the book

Tell me about Gatsby's life and experiences, put the time in the front

Tell me about the content in page 100 to 150
