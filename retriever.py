from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore')

load_dotenv()
embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

pinecone_key ='pcsk_6s9V7z_2cxXhTqckVEcqN22a8E6tADVwmcq4zAnXBVpERnWtwsrUHxkgE3iunSC1E2z4Sm'
os.environ["PINECONE_API_KEY"] = pinecone_key
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

def retrieve_from_pinecone(user_query="What information do you have on Instance Sync Permissions"):
    index_name = "test"
    index = pc.Index(index_name)
    
    print("Index stats:", index.describe_index_stats())
    
    pinecone = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embeddings)
    context = pinecone.similarity_search(user_query)[:5]
    
    return context
