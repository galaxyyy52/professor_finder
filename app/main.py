from fastapi.staticfiles import StaticFiles
import os
from typing import List, Optional
from rank_bm25 import BM25Okapi
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

data =  {
  "professors": [
    {
      "name": "Nancy M. Amato",
      "photo_url": "https://ws.engr.illinois.edu/directory/viewphoto.aspx?photo=17005&s=300",
      "personal_site": "https://cs.illinois.edu/about/people/faculty/namato",
      "university": "University of Illinois at Urbana-Champaign",
      "department": "Computer Science",
      "brief": {
        "title": "Abel Bliss Professor of Engineering and Department Head",
        "research_area": [
          "Robot Motion and Task Planning",
          "Multi-Agent Systems",
          "Crowd Simulation"
        ],
        "courses_taught": [
          "CS 199 STR - CS Stars Seminar",
          "CS 491 PD (CS 491 PDO) - Professional Development",
          "CS 591 CS (CS 591 CSO, CS 591 PHD) - PHD Orientation Seminar"
        ]
      }
    },
    {
      "name": "George Chacko",
      "photo_url": "https://ws.engr.illinois.edu/directory/viewphoto.aspx?photo=12935&s=300",
      "personal_site": "https://cs.illinois.edu/about/people/faculty/chackoge",
      "university": "University of Illinois at Urbana-Champaign",
      "department": "Computer Science",
      "brief": {
        "title": "Scientometrics, Knowledge Diffusion, Data Mining, Network Analysis",
        "research_area": [
          "Data and Information Systems"
        ],
        "courses_taught": [
          "CS 598 GGC - Computational Scientometrics"
        ]
      }
    },
    {
      "name": "ChengXiang Zhai",
      "photo_url": "https://ws.engr.illinois.edu/directory/viewphoto.aspx?photo=8328&s=300",
      "personal_site": "https://cs.illinois.edu/about/people/faculty/czhai",
      "university": "University of Illinois at Urbana-Champaign",
      "department": "Computer Science",
      "brief": {
        "Title": "Intelligent Information Systems, Information Retrieval, Data Mining, Big Data Applications",
        "research_area": [
          "Bioinformatics and Computational Biology",
          "Computers and Education",
          "Data and Information Systems"
        ],
        "courses_taught": [
          "CS 410 - Text Information Systems",
          "CS 510 - Advanced Information Retrieval",
          "CS 598 DM (CS 598 DM1, CS 598 DM2) - Data Mining Capstone",
          "CS 591 TXT - Text Mining Seminar"
        ]
      }
    }
  ]
}


class ProfessorSearch:
    def __init__(self, text_files_directory: str):
        self.text_files_directory = text_files_directory
        self.corpus = self._load_corpus()
        self.tokenized_corpus = [doc.split(" ") for doc in self.corpus]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def _load_corpus(self) -> List[str]:
        corpus = []
        for filename in os.listdir(self.text_files_directory):
            if filename.endswith(".txt"):
                with open(os.path.join(self.text_files_directory, filename), 'r', encoding='utf-8') as f:
                    corpus.append(f.read())
        return corpus

    def search(self, query: str, top_n: int = 5) -> List[str]:
        tokenized_query = query.split(" ")
        doc_scores = self.bm25.get_scores(tokenized_query)
        top_docs = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
        return [self.corpus[i] for i in top_docs if doc_scores[i] > 0]


current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the 'text' directory
TEXT_FILES_DIRECTORY = os.path.join(current_directory, "text/")

professor_search = ProfessorSearch(TEXT_FILES_DIRECTORY)

'''
@app.get("/")
async def search_page(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search/")
async def search_results(request: Request, query: str = Form(...), top_n: Optional[int] = 5) -> templates.TemplateResponse:
    if query:
        results = professor_search.search(query, top_n)
    else:
        results = data["professors"]
    return templates.TemplateResponse("results.html", {"request": request, "results": results, "query": query})
'''

@app.get("/")
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search/")
async def search_results(request: Request, query: str = Form("")):
    if query:
        results = [prof for prof in data["professors"] if query.lower() in prof["name"].lower()]
    else:
        results = data["professors"]
    return templates.TemplateResponse("results.html", {"request": request, "results": results, "query": query})

