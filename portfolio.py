import pandas as pd
import chromadb
import uuid


df = pd.read_csv('./resources/my_portfolio.csv')

class Portfolio:
  def __init__(self, file_path = './resources/my_portfolio.csv'):
    self.file_path = file_path
    self.data = pd.read_csv(file_path)
    self.chroma_client = chromadb.PersistentClient(path='./vectorstore')
    self.collection = self.chroma_client.get_or_create_collection(name='portfolio')

  def load_portfolio(self):
    if not self.collection.count():
      for _, row in df.iterrows():
          techstack = row['Techstack']
          link = row['Links']
          doc_id = str(uuid.uuid4())
          print(f"Adding document with ID: {doc_id}, Techstack: {techstack}, Links: {link}")
          self.collection.add(documents=techstack, metadatas={'links': link}, ids=[doc_id])
  
  def query_links(self,skills):
    return self.collection.query(query_texts= skills,n_results=2).get('metadatas')