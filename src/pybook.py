import os
import sys
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.panel import Panel
from rich.tree import Tree
import autopep8
import cProfile
import pstats
from io import StringIO

console = Console()

# Store code and output for saving later
code_output_log = []

def execute_code_in_file(filename, code):
    with open(filename, 'a') as file:
        file.write(f"\n{code}\n")
    console.print(f"Executing code in [bold green]{filename}[/bold green]...", style="bold green")
    result = os.popen(f"python3 {filename}").read()
    # Log the code and output
    code_output_log.append((code, result))
    return result

def install_package(package_name):
    console.print(f"[bold cyan]Installing package[/bold cyan] [bold magenta]{package_name}[/bold magenta]...", style="bold cyan")
    os.system(f"pip install {package_name}")

def format_code(code):
    formatted_code = autopep8.fix_code(code)
    return formatted_code

def create_virtualenv(env_name):
    if not os.path.exists(env_name):
        console.print(f"[bold yellow]Creating virtual environment: {env_name}[/bold yellow]", style="bold yellow")
        os.system(f"python3 -m venv {env_name}")
    else:
        console.print(f"[bold yellow]Virtual environment '{env_name}' already exists![/bold yellow]")

def activate_virtualenv(env_name):
    if os.name == 'posix':
        activate_script = f"./{env_name}/bin/activate"
    else:
        activate_script = f".\\{env_name}\\Scripts\\activate"
    
    console.print(f"[bold green]Activating virtual environment: {env_name}[/bold green]", style="bold green")
    os.system(f"source {activate_script}")

def lint_code(code):
    console.print(f"[bold blue]Linting code...[/bold blue]", style="bold blue")
    linted_code = autopep8.fix_code(code)
    return linted_code

def display_syntax(code):
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)

def show_help():
    help_text = """
[bold green]Welcome to PyBook[/bold green] - An advanced terminal-based interactive Python notebook.
Here are some commands you can use:
[bold cyan]code:<your python code>[/bold cyan] - Append and execute Python code.
[bold cyan]install:<package name>[/bold cyan] - Install a Python package via pip.
[bold cyan]env:create <env_name>[/bold cyan] - Create a virtual environment.
[bold cyan]env:activate <env_name>[/bold cyan] - Activate a virtual environment.
[bold cyan]format:<your python code>[/bold cyan] - Format your Python code using autopep8.
[bold cyan]lint:<your python code>[/bold cyan] - Lint your Python code for best practices.
[bold cyan]file:create <filename>[/bold cyan] - Create a new file.
[bold cyan]file:list[/bold cyan] - List all files in the current directory.
[bold cyan]file:delete <filename>[/bold cyan] - Delete a file.
[bold cyan]shell:<command>[/bold cyan] - Run a shell command.
[bold cyan]profile:<your python code>[/bold cyan] - Profile your Python code for performance.
[bold cyan]save:file[/bold cyan] - Save all code and outputs in a file (notes.pybook).
[bold cyan]exit[/bold cyan] - Exit the PyBook interactive shell.
"""
    console.print(Panel(help_text, title="Help", style="bold yellow"))

def create_file(filename):
    if os.path.exists(filename):
        console.print(f"[bold red]Error: File '{filename}' already exists.[/bold red]")
    else:
        with open(filename, 'w') as f:
            f.write("# New file created\n")
        console.print(f"[bold green]Created new file: {filename}[/bold green]")

def list_files():
    console.print("[bold blue]Listing files in the current directory:[/bold blue]")
    for file in os.listdir('.'):
        if os.path.isfile(file):
            console.print(f" - [bold yellow]{file}[/bold yellow]")

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        console.print(f"[bold green]Deleted file: {filename}[/bold green]")
    else:
        console.print(f"[bold red]Error: File '{filename}' not found.[/bold red]")

def profile_code(code):
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        exec(code)
    except Exception as e:
        console.print(f"[bold red]Error during profiling: {str(e)}[/bold red]")
    finally:
        profiler.disable()
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats(pstats.SortKey.TIME).print_stats()
        console.print(Panel(s.getvalue(), title="Code Profiling Output", style="bold green"))

def save_to_file():
    with open("notes.pybook", "w") as file:
        for code, result in code_output_log:
            file.write(f"Code:\n{code}\n\nOutput:\n{result}\n{'-'*40}\n")
    console.print("[bold green]All cells and outputs have been saved to notes.pybook[/bold green]")

def main():
    console.print("[bold magenta]Welcome to PyBook - The Advanced Terminal Python Notebook[/bold magenta]")
    filename = Prompt.ask("[bold green]Enter the filename including extension (e.g., script.py)[/bold green]", default="script.py")
    if not filename.endswith('.py'):
        console.print("[bold red]Error: The file must have a .py extension.[/bold red]")
        return

    try:
        current_cell = 1
        while True:
            console.print(f"[bold blue]Cell {current_cell}[/bold blue]")
            user_input = Prompt.ask(f"In Cell {current_cell}:", default="").strip()

            if user_input.startswith('code:'):
                code = user_input[5:].strip()
                if code:
                    formatted_code = format_code(code)
                    result = execute_code_in_file(filename, formatted_code)
                    display_syntax(formatted_code)
                    console.print(f"Output:\n{result}")
                else:
                    console.print("[bold red]Error: No code provided after 'code:'[/bold red]")

            elif user_input.startswith('install:'):
                package_name = user_input[8:].strip()
                if package_name:
                    install_package(package_name)
                else:
                    console.print("[bold red]Error: No package name provided after 'install:'[/bold red]")

            elif user_input.startswith('env:create'):
                env_name = user_input.split(' ')[1].strip()
                if env_name:
                    create_virtualenv(env_name)
                else:
                    console.print("[bold red]Error: No environment name provided after 'env:create'[/bold red]")

            elif user_input.startswith('env:activate'):
                env_name = user_input.split(' ')[1].strip()
                if env_name:
                    activate_virtualenv(env_name)
                else:
                    console.print("[bold red]Error: No environment name provided after 'env:activate'[/bold red]")

            elif user_input.startswith('format:'):
                code = user_input[7:].strip()
                if code:
                    formatted_code = format_code(code)
                    console.print(f"[bold yellow]Formatted Code:[/bold yellow]")
                    display_syntax(formatted_code)
                else:
                    console.print("[bold red]Error: No code provided after 'format:'[/bold red]")

            elif user_input.startswith('lint:'):
                code = user_input[5:].strip()
                if code:
                    linted_code = lint_code(code)
                    console.print(f"[bold yellow]Linted Code (formatted to PEP8):[/bold yellow]")
                    display_syntax(linted_code)
                else:
                    console.print("[bold red]Error: No code provided after 'lint:'[/bold red]")

            elif user_input.lower() == 'help':
                show_help()

            elif user_input.startswith('file:create'):
                filename = user_input.split(' ')[1].strip()
                if filename:
                    create_file(filename)
                else:
                    console.print("[bold red]Error: No filename provided after 'file:create'[/bold red]")

            elif user_input.lower() == 'file:list':
                list_files()

            elif user_input.startswith('file:delete'):
                filename = user_input.split(' ')[1].strip()
                if filename:
                    delete_file(filename)
                else:
                    console.print("[bold red]Error: No filename provided after 'file:delete'[/bold red]")

            elif user_input.startswith('shell:'):
                shell_command = user_input[6:].strip()
                if shell_command:
                    console.print(f"[bold cyan]Running shell command: {shell_command}[/bold cyan]")
                    os.system(shell_command)
                else:
                    console.print("[bold red]Error: No shell command provided after 'shell:'[/bold red]")

            elif user_input.startswith('profile:'):
                code = user_input[8:].strip()
                if code:
                    profile_code(code)
                else:
                    console.print("[bold red]Error: No code provided after 'profile:'[/bold red]")

            elif user_input.lower() == 'save:file':
                save_to_file()

            elif user_input.lower() == 'exit' or user_input.lower() == 'quit':
                console.print("[bold red]Exiting PyBook.[/bold red]")
                return

            else:
                console.print("[bold red]Error: Unknown command. Type 'help' for a list of commands.[/bold red]")

            current_cell += 1

    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting PyBook.[/bold red]")
        sys.exit(0)

if __name__ == '__main__':
    main() 
