# Project Name: professor_finder

**Back end:**

Python, beautiful soap to retreive professor's information for a given University

build an index file for professors

**Installation step

.....

**Front end**

**Frame work: ** 

fastapi,unicorn

**Laguange：** 
python，javascripts, html, css

**Feature:**

Implemented BM25 to score the given corpus and return top 40(default) doc

Implemented NLTK for keyword synonyms search

Implemented case non-sensitive keyword search

**Installation：**

pip install fastapi[all] uvicorn

pip install jinja2 aiofiles

pip install rank-bm25

**Bring up fastapi(uvicorn):**

from command line: enter into root directory of application where the main.py located, for example:
cd C:\Users\xxxxx\Documents\GitHub\professor_finder\app

uvicorn main:app --reload

**Access:**

http://127.0.0.1:8000

