from flask import Flask,render_template
from chains import Chain
from langchain_community.document_loaders import WebBaseLoader
from utils import clean_text

app = Flask(__name__)

loader = WebBaseLoader("https://jobs.nike.com/?jobSearch=true&jsOffset=0&jsSort=posting_start_date&jsLanguage=en&error=jobPost")
page_data = clean_text(loader.load().pop().page_content)

chain = Chain()
try:
    jobs = chain.extract_jobs(page_data)
except Exception as e:
    raise f"Error: {e}"

@app.route('/')
def hello_world():    
    return render_template('home.html',jobs=jobs)

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

