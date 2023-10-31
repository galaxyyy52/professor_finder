1. web crawl
1.1. Content scope
2. clean data, generate dataset and build index
2.1. generate professor index in a json file which including below:
   Professor Name, Professor's photo(URL), Professor's personal site(URL), Univerisity, Department, Professor's Brief including research area and course taught list. refer below for a sample file:

   {
  "professors": [
    {
      "name": "Nancy M. Amato",
      "photo_url": "https://ws.engr.illinois.edu/directory/viewphoto/namato?s=200",
      "personal_site": "https://cs.illinois.edu/about/people/faculty/namato",
      "university": "University of Illinois at Urbana-Champaign",
      "department": "Computer Science",
      "brief": {
        "title": "Abel Bliss Professor of Engineering and Department Head",
        "research_area": [
          "Robot Motion and Task Planning",
          "Multi-Agent Systems",
          "Crowd Simulation"
        ]
        "courses_taught": [
          "CS 199 STR - CS Stars Seminar",
          "CS 491 PD (CS 491 PDO) - Professional Development",
          "CS 591 CS (CS 591 CSO, CS 591 PHD) - PHD Orientation Seminar"
        ]
      }
    },
    {
      "name": "Dr. Jane Smith",
      "photo_url": "https://university.edu/images/janesmith.jpg",
      "personal_site": "https://janesmith.university.edu",
      "university": "University of Innovation",
      "department": "Electrical Engineering",
      "brief": {
        "Title": "US Prisdent"
        "research_area": [
          "Embedded Systems",
          "Internet of Things"
        ]
        "courses_taught": [
          "EE101: Introduction to Electrical Engineering",
          "EE250: Digital Logic Design",
          "EE350: Embedded Systems Design"
        ]
      }
    }
  ]
}


2.2. Generate each professor's full dataset into a text file, named with universityName_department_professorName, need think about to handle different professor with same name, i.e consider find universal professor_id during crawlling if applicable.

4. implement BM25 and TF-IDF(optinal) algrithm to design text retrival machinsm(search engine)

5. Front web design
4.1. create a search box allow user input the keywords, click search button to call the search engine to get the match records  
4.2. display result in a html table to include below:
   Professor Name, Professor's picture, Univerisity, Department, Professor's Brief.
   Click the professor's Name or the photo, it will enter professor's personal site.
   Default it will show top 5 or 10 professors based on sort the ranking from high to low, click more will load all matched professor list with ranking from high to low.
