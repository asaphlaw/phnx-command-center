# Vector Memory System for PHNX
# Semantic search across conversations and documents

import chromadb
from chromadb.config import Settings
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
import os

class VectorMemory:
    """
    Semantic memory using ChromaDB.
    
    Instead of grep (keyword search), this uses embeddings
    for meaning-based search.
    
    Example:
        "What did Fred say about browser automation?"
        → Finds relevant conversations even if exact words differ
    """
    
    def __init__(self, collection_name: str = "phnx_memory"):
        # Use local ChromaDB (no external server needed)
        import chromadb.utils.embedding_functions as embedding_functions
        
        # Create persistent client
        db_path = os.path.expanduser("~/.openclaw/workspace/vector_db")
        os.makedirs(db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "PHNX semantic memory"}
        )
    
    def store(self, content: str, metadata: Dict = None) -> str:
        """
        Store content in vector memory
        
        Args:
            content: The text to remember
            metadata: Optional tags (e.g., {"type": "conversation", "topic": "browser"})
            
        Returns:
            ID of stored item
        """
        # Generate ID from content hash
        item_id = hashlib.md5(content.encode()).hexdigest()[:16]
        
        # Add timestamp
        meta = metadata or {}
        meta["timestamp"] = datetime.now().isoformat()
        meta["content_preview"] = content[:100] + "..." if len(content) > 100 else content
        
        self.collection.add(
            documents=[content],
            metadatas=[meta],
            ids=[item_id]
        )
        
        return item_id
    
    def recall(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search memory by meaning (not just keywords)
        
        Args:
            query: Natural language query
            n_results: Number of results to return
            
        Returns:
            List of matching memories with scores
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        memories = []
        for i in range(len(results['ids'][0])):
            memories.append({
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': results['distances'][0][i] if 'distances' in results else None
            })
        
        return memories
    
    def list_all(self, limit: int = 100) -> List[Dict]:
        """List all memories (for debugging)"""
        results = self.collection.get(limit=limit)
        
        memories = []
        for i in range(len(results['ids'])):
            memories.append({
                'id': results['ids'][i],
                'content': results['documents'][i],
                'metadata': results['metadatas'][i]
            })
        
        return memories

# Quick test
def test():
    print("🧠 Testing Vector Memory...")
    
    mem = VectorMemory()
    
    # Store some memories
    print("\nStoring memories...")
    mem.store("Fred wants to fix browser automation issues with Camoufox", 
              {"type": "issue", "component": "browser"})
    mem.store("We installed Browser-Use to replace Camoufox - it works great!",
              {"type": "solution", "component": "browser"})
    mem.store("RSI 4-pillar system is now operational with Forager, Forge, Crucible, Warden",
              {"type": "infrastructure", "component": "rsi"})
    
    # Recall by meaning
    print("\nQuery: 'What did we use to fix browser problems?'")
    results = mem.recall("What did we use to fix browser problems?")
    
    for r in results:
        print(f"  → {r['content'][:80]}... (score: {r['score']:.3f})")
    
    print("\n✅ Vector memory working!")

if __name__ == "__main__":
    test()
