import os
import ast
import logging
from py2neo import Graph, Node, Relationship
import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepoDBImporter:
    def __init__(self, neo4j_url, neo4j_user, neo4j_password, pg_connection_string):
        try:
            self.neo4j_graph = Graph(neo4j_url, auth=(neo4j_user, neo4j_password))
            self.pg_conn = psycopg2.connect(pg_connection_string)
            self.pg_cursor = self.pg_conn.cursor()
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            logger.info("Connected to databases and initialized model.")
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

    def import_repo(self, repo_path, repo_name):
        try:
            repo_node = Node("Repository", name=repo_name)
            self.neo4j_graph.create(repo_node)
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        self.process_file(file_path, repo_node)
        except Exception as e:
            logger.error(f"Error importing repository {repo_name}: {e}")

    def process_file(self, file_path, repo_node):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            file_node = Node("File", name=os.path.basename(file_path), path=file_path)
            self.neo4j_graph.create(file_node)
            self.neo4j_graph.create(Relationship(repo_node, "CONTAINS", file_node))

            embedding = self.generate_embedding(content)
            vector_id = self.store_embedding(embedding, 'file', file_path)
            file_node['vector_id'] = vector_id
            self.neo4j_graph.push(file_node)

            tree = ast.parse(content)
            self.process_ast(tree, file_node)
        except SyntaxError:
            logger.error(f"Syntax error in file: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

    def process_ast(self, tree, parent_node):
        try:
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_node = Node("Function", name=node.name)
                    self.neo4j_graph.create(func_node)
                    self.neo4j_graph.create(Relationship(parent_node, "DEFINES", func_node))

                    func_content = ast.get_source_segment(tree.body[0], node)
                    embedding = self.generate_embedding(func_content)
                    vector_id = self.store_embedding(embedding, 'function', node.name)
                    func_node['vector_id'] = vector_id
                    self.neo4j_graph.push(func_node)

                elif isinstance(node, ast.ClassDef):
                    class_node = Node("Class", name=node.name)
                    self.neo4j_graph.create(class_node)
                    self.neo4j_graph.create(Relationship(parent_node, "DEFINES", class_node))

                    class_content = ast.get_source_segment(tree.body[0], node)
                    embedding = self.generate_embedding(class_content)
                    vector_id = self.store_embedding(embedding, 'class', node.name)
                    class_node['vector_id'] = vector_id
                    self.neo4j_graph.push(class_node)
        except Exception as e:
            logger.error(f"Error processing AST node: {e}")

    def generate_embedding(self, text):
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
            return embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")

    def store_embedding(self, embedding, entity_type, entity_name):
        try:
            query = """
            INSERT INTO embeddings (vector, entity_type, entity_name)
            VALUES (%s, %s, %s)
            RETURNING id;
            """
            self.pg_cursor.execute(query, (embedding.tolist(), entity_type, entity_name))
            vector_id = self.pg_cursor.fetchone()[0]
            self.pg_conn.commit()
            return vector_id
        except Exception as e:
            logger.error(f"Error storing embedding: {e}")

    def close(self):
        try:
            self.pg_cursor.close()
            self.pg_conn.close()
            logger.info("Closed database connections.")
        except Exception as e:
            logger.error(f"Error closing connections: {e}")

# Usage example
if __name__ == "__main__":
    neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    pg_connection_string = os.getenv("PG_CONNECTION_STRING", "dbname=your_db user=your_user password=your_password host=localhost")

    importer = RepoDBImporter(neo4j_url, neo4j_user, neo4j_password, pg_connection_string)

    repo_path = "/path/to/cloned/repo"
    repo_name = "example_repo"

    importer.import_repo(repo_path, repo_name)
    importer.close()