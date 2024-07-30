import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        print("Debug: Environment variables loaded")
        for key, value in os.environ.items():
            if key.startswith(('POSTGRES_', 'NEO4J_', 'DOCKER_', 'OLLAMA_')):
                print(f"Debug: {key} = {value}")

        # PostgreSQL configurations
        self.POSTGRES_DB = os.getenv('POSTGRES_DB')
        self.POSTGRES_USER = os.getenv('POSTGRES_USER')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        
        # Neo4j configurations
        self.NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
        self.NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
        self.NEO4J_AUTH = os.getenv('NEO4J_AUTH')
        if not self.NEO4J_AUTH:
            self.NEO4J_AUTH = f"{self.NEO4J_USER}/{self.NEO4J_PASSWORD}"
        self.NEO4J_HOST = os.getenv('NEO4J_HOST', 'localhost')
        self.NEO4J_HTTP_PORT = os.getenv('NEO4J_HTTP_PORT', '7474')
        self.NEO4J_BOLT_PORT = os.getenv('NEO4J_BOLT_PORT', '7687')
        
        # Docker configurations
        self.POSTGRES_CONTAINER_NAME = os.getenv('POSTGRES_CONTAINER_NAME')
        self.NEO4J_CONTAINER_NAME = os.getenv('NEO4J_CONTAINER_NAME')
        self.DOCKER_NETWORK_NAME = os.getenv('DOCKER_NETWORK_NAME')

        # Ollama configurations
        self.OLLAMA_MODELS_PATH = os.getenv('OLLAMA_MODELS_PATH')
        
        # CodeStral Configuration
        self.OLLAMA_CODESTRALL_CONTAINER_NAME = os.getenv('OLLAMA_CODESTRALL_CONTAINER_NAME')
        self.OLLAMA_CODESTRALL_PORT = int(os.getenv('OLLAMA_CODESTRALL_PORT', 11435))
        self.OLLAMA_CODESTRALL_MODEL = os.getenv('OLLAMA_CODESTRALL_MODEL')
        self.OLLAMA_CODESTRALL_PATH = os.getenv('OLLAMA_CODESTRALL_PATH')
        self.OLLAMA_CODESTRALL_GPU = int(os.getenv('OLLAMA_CODESTRALL_GPU', 0))
        self.OLLAMA_CODESTRALL_HOST = os.getenv('OLLAMA_CODESTRALL_HOST')

        print("Debug: Config object initialized")
        self.print_all_attributes()

    def get_neo4j_connection_params(self):
        user, password = self.NEO4J_AUTH.split('/')
        return {
            "uri": f"bolt://{self.NEO4J_HOST}:{self.NEO4J_BOLT_PORT}",
            "auth": (user, password)
        }

    def get_postgres_connection_params(self):
        return {
            "dbname": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT
        }

    def print_all_attributes(self):
        print("All Config attributes:")
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")

    @classmethod
    def from_env(cls, env_path):
        # Load environment variables from a specific .env file
        load_dotenv(dotenv_path=env_path)
        return cls()

    def update_from_dict(self, config_dict):
        # Update configuration from a dictionary
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        # Convert configuration to a dictionary
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}