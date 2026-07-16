import os
import json
import numpy as np
import faiss
from google import genai
from google.genai import types

class CitizenCopilotEngine:
    def __init__(self, gemini_api_key=None):
        if gemini_api_key:
            self.client = genai.Client(api_key=gemini_api_key)
        else:
            self.client = genai.Client()
            
        self.embedding_model = "gemini-embedding-001"
        self.documents = []
        self.index = None
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Initializes and seeds the FAISS vector space with verified government advisories."""
        seed_data = [
            {
                "source": "RBI/2024/FRAUD-DIR",
                "text": "The Reserve Bank of India (RBI) explicitly states that banks and law enforcement authorities will never request retail customers to disclose secure parameters like OTP, net banking passwords, or card CVVs."
            },
            {
                "source": "CERT-In Advisory CI-2026-0041",
                "text": "CERT-In warns against 'Digital Arrest' scams. Scammers impersonate law enforcement via video calls. Note that agencies do not conduct interrogations or execute digital lockups over digital conferencing software."
            },
            {
                "source": "NCRP Standard Operating Procedure",
                "text": "If you fall victim to financial cyber fraud, immediately call 1930 or log onto cybercrime.gov.in within the 2-hour Golden Hour window to maximize transaction freeze probability."
            },
            {
                "source": "RBI Consumer Protection Guidelines",
                "text": "In unauthorized third-party electronic transactions, notifying the bank within three working days caps customer liability at zero."
            }
        ]

        self.documents = seed_data
        embeddings = []
        try:
            for doc in self.documents:
                result = self.client.models.embed_content(
                    model=self.embedding_model,
                    contents=doc["text"],
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
                )
                embeddings.append(result.embeddings[0].values)
                
            embedding_matrix = np.array(embeddings).astype('float32')
            dimension = embedding_matrix.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embedding_matrix)
            print(f"⚡ FAISS Vector Index ready to search!")
            
        except Exception as e:
            print(f"⚠️ Vector Embedding Warning: Could not initialize FAISS: {e}")
            self.index = None

    def query_copilot(self, user_query):
        retrieved_context = ""
        citations = []
        
        try:
            if self.index is not None:
                query_embed_res = self.client.models.embed_content(
                    model=self.embedding_model,
                    contents=user_query,
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
                )
                query_vector = np.array([query_embed_res.embeddings[0].values]).astype('float32')
                
                k = 2
                distances, indices = self.index.search(query_vector, k)
                for idx in indices[0]:
                    if idx < len(self.documents):
                        doc = self.documents[idx]
                        retrieved_context += f"\n- Context Source [{doc['source']}]: {doc['text']}\n"
                        citations.append(doc['source'])
        except Exception as e:
            print(f"⚠️ Search Error: Vector query failed: {e}")

        prompt = f"""
        Act as CyberShield Copilot, an elite, high-speed AI Digital Safety Consultant.
        Answer the following citizen query accurately. Keep your response brief, clear, and direct.
        
        VERIFIED POLICY CONTEXT:
        {retrieved_context}
        
        CITIZEN QUERY:
        {user_query}
        
        STRICT FORMATTING & STYLE RULES:
        1. DO NOT use any Markdown (no **, no ###, no headers).
        2. Keep the answer highly concise (under 120 words). Bullet points are preferred.
        3. Provide quick, immediate action steps.
        """
        
        # SPEED OPTIMIZATION: Prioritize flash-lite for sub-second responses, fallback to flash
        models_to_try = [
            "gemini-3.1-flash-lite",   # Sub-second latency champion
            "gemini-3.5-flash"         # High-intelligence flagship backup
        ]
        
        response = None
        for model in models_to_try:
            try:
                # Set dynamic limits to force fast, snappy generation
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=300, # Shorter limit = much faster response
                        temperature=0.2
                    )
                )
                print(f"🚀 Speed Response generated via model: {model}")
                break
            except Exception as e:
                print(f"⚠️ Speed Fallback: '{model}' busy, skipping. Error: {e}")

        if response:
            return {"answer": response.text, "citations": list(set(citations))}
        else:
            return {"answer": "The safety network is taking longer than usual. Please resubmit your query.", "citations": []}