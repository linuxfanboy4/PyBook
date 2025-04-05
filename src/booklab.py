import os
import sys
import pygments
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import track
from rich.text import Text
from rich.layout import Layout
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown
import time
import shutil
import difflib
from pygments import lexers, formatters


class BookLAB:
    def __init__(self):
        self.console = Console()
        self.current_path = os.getcwd()

    def display_prompt(self, cell_number):
        self.console.print(f"[bold green]Cell {cell_number}:[/bold green] ", end="")
        return input()

    def list_files(self):
        files = os.listdir(self.current_path)
        table = Table(title="Files in Directory", style="cyan")
        table.add_column("Index", justify="center")
        table.add_column("Filename", justify="left")

        for i, file in enumerate(files, 1):
            table.add_row(str(i), file)
        self.console.print(table)

    def show_path(self):
        self.console.print(f"[bold yellow]Current Path:[/bold yellow] {self.current_path}")

    def show_file_contents(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                contents = file.read()
            lexer = lexers.guess_lexer_for_filename(filename, contents)
            syntax = Syntax(contents, lexer.name, theme="monokai", line_numbers=True)
            self.console.print(syntax)
        else:
            self.console.print(f"[bold red]Error:[/bold red] File not found.")

    def show_file_stat(self, filename):
        if os.path.exists(filename):
            stats = os.stat(filename)
            table = Table(title=f"Stats for {filename}", style="magenta")
            table.add_column("Property", justify="left")
            table.add_column("Value", justify="right")

            table.add_row("Size", str(stats.st_size))
            table.add_row("Created", time.ctime(stats.st_ctime))
            table.add_row("Modified", time.ctime(stats.st_mtime))
            table.add_row("Accessed", time.ctime(stats.st_atime))
            self.console.print(table)
        else:
            self.console.print(f"[bold red]Error:[/bold red] File not found.")

    def show_file_size(self, filename):
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            self.console.print(f"[bold green]File Size:[/bold green] {size} bytes")
        else:
            self.console.print(f"[bold red]Error:[/bold red] File not found.")

    def create_file(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write('')
            self.console.print(f"[bold green]File '{filename}' created successfully.[/bold green]")
        else:
            self.console.print(f"[bold red]Error:[/bold red] File already exists.")

    def delete_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
            self.console.print(f"[bold green]File '{filename}' deleted successfully.[/bold green]")
        else:
            self.console.print(f"[bold red]Error:[/bold red] File not found.")

    def rename_file(self, old_name, new_name):
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            self.console.print(f"[bold green]File renamed from '{old_name}' to '{new_name}'[/bold green]")
        else:
            self.console.print(f"[bold red]Error:[/bold red] File not found.")

    def copy_file(self, source, destination):
        if os.path.exists(source):
            shutil.copy(source, destination)
            self.console.print(f"[bold green]File '{source}' copied to '{destination}'[/bold green]")
        else:
            self.console.print(f"[bold red]Error:[/bold red] Source file not found.")

    def move_file(self, source, destination):
        if os.path.exists(source):
            shutil.move(source, destination)
            self.console.print(f"[bold green]File '{source}' moved to '{destination}'[/bold green]")
        else:
            self.console.print(f"[bold red]Error:[/bold red] Source file not found.")

    def search_files(self, keyword):
        files = [f for f in os.listdir(self.current_path) if keyword.lower() in f.lower()]
        if files:
            self.console.print("[bold cyan]Found Files:[/bold cyan]")
            for file in files:
                self.console.print(file)
        else:
            self.console.print(f"[bold red]No files found with '{keyword}'[/bold red]")

    def preview_file(self, filename, num_lines=10):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                preview = ''.join([file.readline() for _ in range(num_lines)])
            self.console.print(f"[bold yellow]Preview of {filename}:[/bold yellow]")
            self.console.print(preview)
        else:
            self.console.print(f"[bold red]Error:[/bold red] File not found.")

    def compare_files(self, file1, file2):
        if os.path.exists(file1) and os.path.exists(file2):
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2)
                self.console.print("[bold cyan]File Comparison:[/bold cyan]")
                self.console.print(''.join(diff))
        else:
            self.console.print(f"[bold red]Error:[/bold red] One or both files not found.")

    def change_directory(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(path)
            self.current_path = os.getcwd()
            self.console.print(f"[bold green]Directory changed to {self.current_path}[/bold green]")
        else:
            self.console.print(f"[bold red]Error:[/bold red] Invalid directory path.")

    def list_directories(self):
        dirs = [d for d in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, d))]
        if dirs:
            self.console.print("[bold cyan]Directories in Current Path:[/bold cyan]")
            for d in dirs:
                self.console.print(d)
        else:
            self.console.print(f"[bold red]No directories found.[/bold red]")

    def show_system_info(self):
        import platform
        self.console.print(f"[bold yellow]System Information:[/bold yellow]")
        self.console.print(f"OS: {platform.system()} {platform.release()}")
        self.console.print(f"Machine: {platform.machine()}")
        self.console.print(f"Processor: {platform.processor()}")
        self.console.print(f"Python Version: {platform.python_version()}")

    def start(self):
        while True:
            self.console.clear()
            self.console.print(Panel("Welcome to BookLAB! Type 'help' for commands.", style="bold cyan"))
            cell_number = 1
            while True:
                command = self.display_prompt(cell_number)
                if command.startswith("list:"):
                    self.list_files()
                elif command.startswith("path:"):
                    self.show_path()
                elif command.startswith("contents:"):
                    filename = command[len("contents:"):].strip()
                    self.show_file_contents(filename)
                elif command.startswith("stat:"):
                    filename = command[len("stat:"):].strip()
                    self.show_file_stat(filename)
                elif command.startswith("size:"):
                    filename = command[len("size:"):].strip()
                    self.show_file_size(filename)
                elif command.startswith("create:"):
                    filename = command[len("create:"):].strip()
                    self.create_file(filename)
                elif command.startswith("delete:"):
                    filename = command[len("delete:"):].strip()
                    self.delete_file(filename)
                elif command.startswith("rename:"):
                    parts = command[len("rename:"):].strip().split(" to ")
                    if len(parts) == 2:
                        self.rename_file(parts[0], parts[1])
                    else:
                        self.console.print("[bold red]Error:[/bold red] Invalid syntax.")
                elif command.startswith("copy:"):
                    parts = command[len("copy:"):].strip().split(" to ")
                    if len(parts) == 2:
                        self.copy_file(parts[0], parts[1])
                    else:
                        self.console.print("[bold red]Error:[/bold red] Invalid syntax.")
                elif command.startswith("move:"):
                    parts = command[len("move:"):].strip().split(" to ")
                    if len(parts) == 2:
                        self.move_file(parts[0], parts[1])
                    else:
                        self.console.print("[bold red]Error:[/bold red] Invalid syntax.")
                elif command.startswith("search:"):
                    keyword = command[len("search:"):].strip()
                    self.search_files(keyword)
                elif command.startswith("preview:"):
                    filename = command[len("preview:"):].strip()
                    self.preview_file(filename)
                elif command.startswith("compare:"):
                    files = command[len("compare:"):].strip().split(" and ")
                    if len(files) == 2:
                        self.compare_files(files[0], files[1])
                    else:
                        self.console.print("[bold red]Error:[/bold red] Invalid syntax.")
                elif command.startswith("cd:"):
                    path = command[len("cd:"):].strip()
                    self.change_directory(path)
                elif command == "dirs":
                    self.list_directories()
                elif command == "sysinfo":
                    self.show_system_info()
                elif command == "exit":
                    sys.exit()
                elif command == "help":
                    self.console.print("[bold yellow]Commands:[/bold yellow]")
                    self.console.print("- list:       List available files")
                    self.console.print("- path:       Show current directory path")
                    self.console.print("- contents:<filename>    Show file contents with syntax highlight")
                    self.console.print("- stat:<filename>        Show file stats")
                    self.console.print("- size:<filename>        Show file size")
                    self.console.print("- create:<filename>      Create a new file")
                    self.console.print("- delete:<filename>      Delete a file")
                    self.console.print("- rename:<old> to <new>  Rename a file")
                    self.console.print("- copy:<source> to <dest>    Copy a file")
                    self.console.print("- move:<source> to <dest>    Move a file")
                    self.console.print("- search:<keyword>       Search files by keyword")
                    self.console.print("- preview:<filename>     Preview the first few lines of a file")
                    self.console.print("- compare:<file1> and <file2>  Compare two files")
                    self.console.print("- cd:<path>              Change directory")
                    self.console.print("- dirs                   List directories in current path")
                    self.console.print("- sysinfo                Show system information")
                    self.console.print("- exit                   Exit BookLAB")
                else:
                    self.console.print(f"[bold red]Error:[/bold red] Unknown command.")
                time.sleep(1)
                cell_number += 1


if __name__ == "__main__":
    lab = BookLAB()
    lab.start()
