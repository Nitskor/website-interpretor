from flask import Flask,render_template,request
from chains import Chain
from langchain_community.document_loaders import WebBaseLoader
from utils import clean_text
from portfolio import Portfolio

app = Flask(__name__)

#loader = WebBaseLoader("https://jobs.nike.com/?jobSearch=true&jsOffset=0&jsSort=posting_start_date&jsLanguage=en&error=jobPost")
#page_data = clean_text(loader.load().pop().page_content)

chain = Chain()
portfolio = Portfolio()
portfolio.load_portfolio()
#try:
    #jobs = chain.extract_jobs(page_data)
#except Exception as e:
    #raise f"Error: {e}"
#skills = ['python']
#link = portfolio.query_links(skills=skills)
#mail = chain.write_mail(job=jobs,links=link)

@app.route('/')
def hello_world():    
    return render_template('home.html')

@app.route('/output' ,methods=['POST'])
def output():
    data = str(request.form.get('url'))
    loader = WebBaseLoader(data)
    page_data = clean_text(loader.load().pop().page_content)
    jobs = chain.extract_jobs(page_data)
    skills = 'python'
    link = portfolio.query_links(skills=skills)
    mail = chain.write_mail(jobs,link)  
    return render_template('output.html',jobs=jobs,data=data,mail=mail.content)

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

