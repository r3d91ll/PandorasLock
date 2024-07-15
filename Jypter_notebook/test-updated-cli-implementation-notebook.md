# RAG Tools: CLI Implementation

## 1. Introduction

In this notebook, we'll implement a Command Line Interface (CLI) for our RAG Tools project. The CLI will allow us to interact with our Ollama instances and manage our Docker containers from the command line, providing a more efficient way to control our ML environment.

## 2. Setup and Dependencies

First, let's install the necessary dependencies for our CLI implementation.

```python
!conda install -c conda-forge typer -y
!conda install -c conda-forge rich -y  # for enhanced CLI output
```

## 3. Importing Required Modules

Now, let's import the modules we'll need for our CLI implementation.

```python
import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.utils.config_utils import Config
from src.utils.ollama_manager import OllamaManager
from src.utils.DockerComposeManager import DockerComposeManager
```

## 4. CLI Implementation

Let's implement our CLI using Typer:

```python
app = typer.Typer()
config = Config()
ollama_manager = OllamaManager(config)
docker_manager = DockerComposeManager(str(project_root / "config" / "docker-compose.yml"))
console = Console()

@app.command()
def start():
    """Start the Ollama containers"""
    rprint("[bold green]Starting Ollama containers...[/bold green]")
    docker_manager.start_containers()

@app.command()
def stop():
    """Stop the Ollama containers"""
    rprint("[bold red]Stopping Ollama containers...[/bold red]")
    docker_manager.stop_containers()

@app.command()
def status():
    """Check the status of the Ollama containers"""
    rprint("[bold blue]Checking container status...[/bold blue]")
    docker_manager.show_container_status()

@app.command()
def chat():
    """Start a chat session with the LLM"""
    rprint("[bold cyan]Starting chat session. Type 'exit' to end the session.[/bold cyan]")
    
    if not ollama_manager.is_model_running():
        rprint(f"[bold red]Error: Model {ollama_manager.model} is not running. Please start the model first.[/bold red]")
        return

    while True:
        prompt = typer.prompt("You")
        if prompt.lower() == 'exit':
            break
        response = ollama_manager.generate_response(prompt)
        rprint(f"[bold green]LLM:[/bold green] {response}")

@app.command()
def list_models():
    """List available Ollama models"""
    models = ollama_manager.list_models()
    table = Table(title="Available Ollama Models")
    table.add_column("Model Name", style="cyan")
    table.add_column("Status", style="magenta")
    
    for model in models:
        table.add_row(model['name'], "Loaded" if model['loaded'] else "Not Loaded")
    
    console.print(table)

if __name__ == "__main__":
    app()
```

## 5. Testing the CLI

Now let's test our CLI implementation:

```python
# Test the CLI
!python {__file__} --help
!python {__file__} status
!python {__file__} list-models
```

## 6. Conclusion and Next Steps

In this notebook, we've implemented a basic CLI for our RAG Tools project. This CLI allows us to manage our Docker containers and interact with our LLM from the command line.

Next steps could include:
1. Adding more advanced commands (e.g., switching models, adjusting LLM parameters)
2. Implementing more robust error handling and input validation
3. Enhancing the chat interface with features like conversation history
4. Integrating the CLI with our document ingestion and RAG querying systems (which we'll develop in future notebooks)

In our next notebook, we'll focus on implementing advanced LLM configurables, allowing us to adjust parameters like context length and temperature through our CLI.
