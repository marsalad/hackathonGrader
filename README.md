# hackathonGrader
Auto-grade PennApps applications by scraping Devpost

### Running the Auto-Grader
Dependencies: ``requests``, ``bs4``, ``csv``<br>
Save a csv of applicant Devpost usernames as ``apps.csv`` in the same folder as the python file and run ``python3 devpostParser.py``. Allow the scraper to run (this may take a while depending on how many applicants you are grading at once) and it will ouput the file ``scraped.csv`` with scraped applicant data.