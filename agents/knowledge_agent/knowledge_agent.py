import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.readers.file import IPYNBReader

load_dotenv()

class KnowledgeAgent:
    def __init__(self):
        print("[System] Initializing Agent 3 (Knowledge & RAG)...")
        
        # 1. Configure the LLM (Groq) for Generation
        self.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
        
        # 2. Configure the Embedding Model for Semantic Search
        # This runs locally to convert text into numbers
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        
        # Apply to global LlamaIndex settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        
        # 3. Load the Documents
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        data_dir = "data/study_materials"
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"[Warning] Directory {data_dir} created. Please add your PDFs or .txt files.")
            self.query_engine = None
            return

        print("[System] Reading raw study materials into memory...")
        
        # BYPASS: Using the default SimpleDirectoryReader to read everything as plain text
        reader = SimpleDirectoryReader(
            input_dir=data_dir,
            required_exts=[".pdf", ".txt"] 
        )
        
        documents = reader.load_data()
        
        if not documents:
            print("[Warning] No documents found in study_materials folder.")
            self.query_engine = None
            return
            
        print(f"[System] Successfully loaded {len(documents)} document chunks. Building Vector Index...")
        
        # Create the Vector Database 
        self.index = VectorStoreIndex.from_documents(documents)
        
        # Create the Query Engine
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=3 
        )
        print("[System] Knowledge Agent is ready to answer questions.")
    def query(self, user_question: str) -> str:
        if not self.query_engine:
            return "My knowledge base is empty. Please add files to data/study_materials/."
            
        print("\n[AGENT 3] Searching study materials for the answer...")
        
        # This single line executes the entire 5-step RAG flow we discussed above
        response = self.query_engine.query(user_question)
        
        return str(response)