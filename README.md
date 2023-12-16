# Project Name: professor_finder

**Back end:**

Python, beautiful soap to retreive professor's information for a given University and generate professor docs, each professor's information will be put into one dedicate doc.

build an index file for professors

Installation/run step:

.....

**Front end**

Frame work: fastapi,unicorn

Laguange：python，javascripts, html, css

**Feature:**

Implemented BM25 to rank the given corpus(professor doc) and return top 40(default) doc

Implemented NLTK for keyword synonyms search

Implemented case non-sensitive keyword search

**Installation step：**

pip install fastapi[all] uvicorn

pip install jinja2 aiofiles

pip install rank-bm25 nltk

**Bring up fastapi(uvicorn):**

from command line: enter into root directory of application where the main.py located
for example:
cd C:\Users\xxxxx\Documents\GitHub\professor_finder\app

uvicorn main:app --reload

**Access to professor finder:**

http://127.0.0.1:8000

**Project Demo:**

https://www.youtube.com/watch?v=KN9P4RIZmRQ

