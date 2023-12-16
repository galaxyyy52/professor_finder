from fastapi.staticfiles import StaticFiles
from typing import List, Tuple
from rank_bm25 import BM25Okapi
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os,json,nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class ProfessorSearch:
    def __init__(self, text_files_directory: str):
        self.ps = PorterStemmer()  # Initialize the Porter Stemmer
        self.text_files_directory = text_files_directory
        self.corpus, self.filenames = self._load_corpus()
        self.tokenized_corpus = [doc.split(" ") for doc in self.corpus]

        # Custom parameters
        k1 = 1.5
        b = 0.75       
        # Initialize BM25 with custom parameters
        self.bm25 = BM25Okapi(self.tokenized_corpus, k1=k1, b=b)
        
    def _stem_text(self, text):
        tokens = word_tokenize(text)
        return " ".join([self.ps.stem(token) for token in tokens])

    def _load_corpus(self) -> Tuple[List[str], List[str]]:
        corpus = []
        filenames = []
        for filename in os.listdir(self.text_files_directory):
            if filename.endswith(".txt"):
                with open(os.path.join(self.text_files_directory, filename), 'r', encoding='utf-8') as f:
                    text = f.read().lower()
                    stemmed_text = self._stem_text(text)  # Stem the text
                    corpus.append(stemmed_text)
                    filenames.append(os.path.splitext(filename)[0])
        return corpus, filenames

    def search(self, query: str, top_n: int = 5) -> List[dict]:
        # Stem the query
        stemmed_query = self._stem_text(query)
        # Tokenize and expand the query        
        tokenized_query = stemmed_query.split(" ")
        print(f"word,STEM word:{query, tokenized_query}")
        tokenized_query += query.split(" ")
        expanded_query = tokenized_query.copy() 
        
        # To support synonyms search, expand each term in the query with synonyms
        for term in tokenized_query:
            expanded_query.extend(get_synonyms(term, max_synonyms=5))
        
        # Deduplicate and tokenize expanded query
        expanded_query = list(set(expanded_query))
        tokenized_expanded_query = [word.split(" ") for word in expanded_query]
        flat_query = [item.lower() for sublist in tokenized_expanded_query for item in sublist]
        
        print(f"word,synonyms word:{query, flat_query}")
        # Search using expanded query
        doc_scores = self.bm25.get_scores(flat_query)

        #doc_scores = self.bm25.get_scores(tokenized_query)
        top_docs = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
        search_results = []
        for i in top_docs:
            if doc_scores[i] > 0:
                # Extract filename without extension
                filename_without_extension = self.filenames[i]

                # Find the corresponding professor's data
                for professor in professors_data:
                    if professor["name"].replace('-', ' ').lower() == filename_without_extension.lower():
                        search_results.append({"professor": professor, "score": doc_scores[i]})
                        break
    
        #print(f"search_results:{search_results}")
        return search_results
    

def get_synonyms(word, max_synonyms=5):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
            if len(synonyms) >= max_synonyms:
                return list(synonyms)
    return list(synonyms)

current_directory = os.path.dirname(os.path.abspath(__file__))

# Function to load data from JSON file
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
  # This will print the content of the file
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
#json_file_path = os.path.join(current_directory,"professor_index.json")
json_file_path = os.path.join(current_directory,"professor_index.json")
if not os.path.exists(json_file_path):
    print(f"Index files  '{json_file_path}' not found.")
# Load the data
professors_data = load_json_data(json_file_path)

# Construct the path to the 'text' directory
TEXT_FILES_DIRECTORY = os.path.join(current_directory, "professor_doc/")

if not os.path.exists(TEXT_FILES_DIRECTORY):
    print(f"Text files directory '{TEXT_FILES_DIRECTORY}' not found.")


professor_search = ProfessorSearch(TEXT_FILES_DIRECTORY)



@app.get("/", response_model=None)
async def search_page(request: Request) -> templates.TemplateResponse:
    #return templates.TemplateResponse("search.html", {"request": request})
    return templates.TemplateResponse("search_results.html", {"request": request}) 

#@app.post("/search/")
@app.get("/search/", response_class=HTMLResponse)
@app.post("/search/", response_class=HTMLResponse)
async def search_results(request: Request, query: str = Form(""), current_page: int = 1, rows_per_page: int = 10):
    # Your existing search logic
    # If the method is GET, use Query instead of Form
    if request.method == "GET":
        query = request.query_params.get('query', '')
    print(f"query:{query}")
    search_performed = bool(query)
    all_results = professor_search.search(query, 40)

    # Pagination logic
    total_pages = len(all_results) // rows_per_page + (1 if len(all_results) % rows_per_page else 0)
    start_index = (current_page - 1) * rows_per_page
    end_index = start_index + rows_per_page
    page_results = all_results[start_index:end_index]
    
    # Check if the request is an AJAX request
    if "X-Requested-With" in request.headers and request.headers["X-Requested-With"] == "XMLHttpRequest":
        template_name = "results_partial.html"
    else:
        #template_name = "results.html"
        template_name = "search_results.html"
        
    return templates.TemplateResponse(template_name, {
        "request": request, 
        "results": page_results, 
        "query": query,
        "current_page": current_page,
        "total_pages": total_pages,
        "search_performed": search_performed
    })
