from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore


class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)


vanna = MyVanna(config={"model": "llama3"})

# Training DDL
vanna.train(ddl="""
CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  created_at TIMESTAMP
);
""")

# Training con query d'esempio
vanna.train(sql="SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL 7 DAY")

# Training con documentazione naturale
vanna.train(documentation="users.email is the user's primary email address")
