from __future__ import annotations

import ast
import json
import os
import platform
import re
import subprocess
import sys
import threading
import warnings
import webbrowser

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Iterable

try:
    import customtkinter as ctk
except ImportError:
    raise SystemExit(
        "\nCustomTkinter wurde nicht gefunden.\n"
        "CustomTkinter was not found.\n\n"
        "Installation:\n"
        "    pip install customtkinter\n"
    )



APP_TITLE       = " Codebase Cartographer | ©Thorsten Bylicki - ©BYLICKILABS"
APP_NAME        = " Codebase Cartographer"
APP_AUTHOR      = " BylickiLabs"
APP_VERSION     = " 1.0.0"
APP_YEAR        = " 06/2026"
APP_LICENSE     = " MIT"

APP_GITHUB_URL = "https://github.com/bylickilabs"

APP_DESCRIPTION_DE = (
    "Codebase Cartographer analysiert Python-Projekte vollständig lokal und "
    "erstellt eine strukturierte Übersicht über Dateien, Module, Klassen, "
    "Funktionen, Methoden, Importe, Dokumentation, Komplexität und mögliche "
    "Wartungsrisiken."
)

APP_DESCRIPTION_EN = (
    "Codebase Cartographer analyzes Python projects entirely locally and "
    "creates a structured overview of files, modules, classes, functions, "
    "methods, imports, documentation, complexity, and potential "
    "maintainability risks."
)



SUPPORTED_FILE_EXTENSIONS = {".py"}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".github",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "node_modules",
    "site-packages",
    "dist",
    "build",
}



MAX_FILE_SIZE_BYTES = 3_000_000

LARGE_FILE_LINE_LIMIT = 500
HIGH_FILE_COMPLEXITY_LIMIT = 25
HIGH_SYMBOL_COMPLEXITY_LIMIT = 10
DEEP_NESTING_LIMIT = 5

DEFAULT_WINDOW_WIDTH = 1500
DEFAULT_WINDOW_HEIGHT = 900

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")



TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": {
        "language_button": "EN",
        "language_tooltip": "Switch to English",
        "dashboard": "Übersicht",
        "files": "Dateien",
        "symbols": "Struktur",
        "dependencies": "Abhängigkeiten",
        "findings": "Befunde",
        "report": "Bericht",
        "select_project": "Projekt auswählen",
        "analyze_project": "Analyse starten",
        "open_folder": "Ordner öffnen",
        "github": "GitHub",
        "about": "Info",
        "appearance": "Darstellung",
        "dark": "Dunkel",
        "light": "Hell",
        "system": "System",
        "ready": "Bereit",
        "no_project": "Noch kein Projekt ausgewählt",
        "project_selected": "Projekt ausgewählt",
        "select_project_first": (
            "Bitte wähle zuerst einen gültigen Projektordner aus."
        ),
        "analysis_running": "Die Codebasis wird analysiert …",
        "analysis_finished": "Analyse erfolgreich abgeschlossen",
        "analysis_failed": "Die Analyse ist fehlgeschlagen",
        "files_scanned": "Python-Dateien",
        "code_lines": "Codezeilen",
        "classes": "Klassen",
        "functions": "Funktionen",
        "imports": "Importe",
        "findings_count": "Befunde",
        "documentation": "Dokumentation",
        "quality_score": "Qualitätsindex",
        "project_information": "Projektinformationen",
        "project_path": "Projektpfad",
        "generated_at": "Erstellt",
        "total_lines": "Gesamtzeilen",
        "comment_lines": "Kommentarzeilen",
        "blank_lines": "Leerzeilen",
        "syntax_errors": "Syntaxfehler",
        "todo_markers": "TODO/FIXME",
        "ignored_files": "Ignorierte Dateien",
        "top_dependencies": "Häufigste Abhängigkeiten",
        "complex_files": "Komplexeste Dateien",
        "file": "Datei",
        "module": "Modul",
        "lines": "Zeilen",
        "size": "Größe",
        "complexity": "Komplexität",
        "status": "Status",
        "symbol": "Symbol",
        "type": "Typ",
        "line": "Zeile",
        "docstring": "Docstring",
        "parent": "Übergeordnet",
        "dependency": "Abhängigkeit",
        "category": "Kategorie",
        "count": "Anzahl",
        "used_by": "Verwendet von",
        "severity": "Priorität",
        "description": "Beschreibung",
        "recommendation": "Empfehlung",
        "filter_files": "Dateien filtern …",
        "filter_symbols": "Symbole filtern …",
        "filter_findings": "Befunde filtern …",
        "export_json": "JSON exportieren",
        "export_markdown": "Markdown exportieren",
        "export_success": "Der Bericht wurde erfolgreich gespeichert.",
        "export_failed": "Der Bericht konnte nicht gespeichert werden.",
        "folder_open_failed": "Der Projektordner konnte nicht geöffnet werden.",
        "no_data": "Keine Daten verfügbar",
        "no_findings": "Keine relevanten Befunde erkannt",
        "yes": "Ja",
        "no": "Nein",
        "class": "Klasse",
        "function": "Funktion",
        "async_function": "Async-Funktion",
        "method": "Methode",
        "standard_library": "Standardbibliothek",
        "external": "Extern",
        "local": "Lokal/Projekt",
        "relative": "Relativer Import",
        "unknown": "Unbekannt",
        "critical": "Kritisch",
        "high": "Hoch",
        "medium": "Mittel",
        "low": "Niedrig",
        "info": "Info",
        "clean": "Unauffällig",
        "review": "Prüfen",
        "attention": "Aufmerksamkeit",
        "high_risk": "Hoher Handlungsbedarf",
        "about_title": "Über Codebase Cartographer",
        "privacy": (
            "Datenschutz: Sämtliche Analysen werden lokal durchgeführt. "
            "Es werden keine Projektdateien, Quellcodes oder Analyseergebnisse "
            "an externe Dienste übertragen."
        ),
        "analysis_hint": (
            "Wähle einen Python-Projektordner aus. Codebase Cartographer "
            "untersucht anschließend die Projektstruktur, Symbole, Importe, "
            "Dokumentation, Komplexität und mögliche Wartungsrisiken."
        ),
        "scan_summary": (
            "{files} Dateien, {lines} Codezeilen und {findings} Befunde analysiert"
        ),
        "report_title": "Codebase-Analysebericht",
        "overview": "Gesamtübersicht",
        "file_analysis": "Dateianalyse",
        "quality_findings": "Qualitätsbefunde",
        "generated_by": "Erstellt mit",
        "invalid_project": "Der ausgewählte Projektordner ist nicht verfügbar.",
        "operation_cancelled": "Vorgang abgebrochen",
        "file_too_large": "Datei wegen ihrer Größe übersprungen",
        "syntax_error": "Python-Syntaxfehler erkannt",
        "large_file": "Sehr große Quelldatei",
        "high_file_complexity": "Hohe Dateikomplexität",
        "high_symbol_complexity": "Komplexes Symbol erkannt",
        "deep_nesting": "Tiefe Verschachtelung erkannt",
        "missing_module_docstring": "Modul-Docstring fehlt",
        "missing_symbol_docstrings": "Öffentliche Symbole ohne Docstring",
        "todo_detected": "Offene TODO- oder FIXME-Markierungen",
        "wildcard_import": "Wildcard-Import erkannt",
        "duplicate_symbol": "Symbolname mehrfach vorhanden",
        "rec_file_too_large": (
            "Dateigröße prüfen und das Scan-Limit nur bei Bedarf anpassen."
        ),
        "rec_syntax_error": (
            "Syntaxfehler beheben, bevor weitere Qualitätswerte bewertet werden."
        ),
        "rec_large_file": (
            "Die Datei in kleinere, fachlich getrennte Module aufteilen."
        ),
        "rec_file_complexity": (
            "Verzweigungen reduzieren und Verantwortlichkeiten auf mehrere "
            "Module oder Funktionen verteilen."
        ),
        "rec_symbol_complexity": (
            "Die Logik in kleinere Funktionen extrahieren und Kontrollflüsse "
            "vereinfachen."
        ),
        "rec_deep_nesting": (
            "Guard Clauses, Hilfsfunktionen oder klarere Kontrollflüsse verwenden."
        ),
        "rec_module_docstring": (
            "Eine Modulbeschreibung mit Zweck und Verantwortlichkeit ergänzen."
        ),
        "rec_symbol_docstrings": (
            "Öffentliche Klassen, Methoden und Funktionen dokumentieren."
        ),
        "rec_todo": (
            "Offene Markierungen als Issue erfassen, priorisieren oder entfernen."
        ),
        "rec_wildcard": "Nur die tatsächlich benötigten Namen explizit importieren.",
        "rec_duplicate": (
            "Namensgebung und Verantwortlichkeiten der betroffenen Symbole prüfen."
        ),
    },
    "en": {
        "language_button": "DE",
        "language_tooltip": "Auf Deutsch umschalten",
        "dashboard": "Dashboard",
        "files": "Files",
        "symbols": "Structure",
        "dependencies": "Dependencies",
        "findings": "Findings",
        "report": "Report",
        "select_project": "Select project",
        "analyze_project": "Start analysis",
        "open_folder": "Open folder",
        "github": "GitHub",
        "about": "About",
        "appearance": "Appearance",
        "dark": "Dark",
        "light": "Light",
        "system": "System",
        "ready": "Ready",
        "no_project": "No project selected",
        "project_selected": "Project selected",
        "select_project_first": (
            "Please select a valid project folder first."
        ),
        "analysis_running": "Analyzing the codebase …",
        "analysis_finished": "Analysis completed successfully",
        "analysis_failed": "The analysis failed",
        "files_scanned": "Python files",
        "code_lines": "Lines of code",
        "classes": "Classes",
        "functions": "Functions",
        "imports": "Imports",
        "findings_count": "Findings",
        "documentation": "Documentation",
        "quality_score": "Quality index",
        "project_information": "Project information",
        "project_path": "Project path",
        "generated_at": "Generated",
        "total_lines": "Total lines",
        "comment_lines": "Comment lines",
        "blank_lines": "Blank lines",
        "syntax_errors": "Syntax errors",
        "todo_markers": "TODO/FIXME",
        "ignored_files": "Ignored files",
        "top_dependencies": "Top dependencies",
        "complex_files": "Most complex files",
        "file": "File",
        "module": "Module",
        "lines": "Lines",
        "size": "Size",
        "complexity": "Complexity",
        "status": "Status",
        "symbol": "Symbol",
        "type": "Type",
        "line": "Line",
        "docstring": "Docstring",
        "parent": "Parent",
        "dependency": "Dependency",
        "category": "Category",
        "count": "Count",
        "used_by": "Used by",
        "severity": "Priority",
        "description": "Description",
        "recommendation": "Recommendation",
        "filter_files": "Filter files …",
        "filter_symbols": "Filter symbols …",
        "filter_findings": "Filter findings …",
        "export_json": "Export JSON",
        "export_markdown": "Export Markdown",
        "export_success": "The report was saved successfully.",
        "export_failed": "The report could not be saved.",
        "folder_open_failed": "The project folder could not be opened.",
        "no_data": "No data available",
        "no_findings": "No relevant findings detected",
        "yes": "Yes",
        "no": "No",
        "class": "Class",
        "function": "Function",
        "async_function": "Async function",
        "method": "Method",
        "standard_library": "Standard library",
        "external": "External",
        "local": "Local/project",
        "relative": "Relative import",
        "unknown": "Unknown",
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "info": "Info",
        "clean": "Clean",
        "review": "Review",
        "attention": "Attention",
        "high_risk": "High action required",
        "about_title": "About Codebase Cartographer",
        "privacy": (
            "Privacy: All analyses are performed locally. No project files, "
            "source code, or analysis results are transferred to external services."
        ),
        "analysis_hint": (
            "Select a Python project folder. Codebase Cartographer will examine "
            "the project structure, symbols, imports, documentation, complexity, "
            "and potential maintainability risks."
        ),
        "scan_summary": (
            "Analyzed {files} files, {lines} lines of code, and {findings} findings"
        ),
        "report_title": "Codebase Analysis Report",
        "overview": "Overview",
        "file_analysis": "File analysis",
        "quality_findings": "Quality findings",
        "generated_by": "Generated with",
        "invalid_project": "The selected project folder is unavailable.",
        "operation_cancelled": "Operation cancelled",
        "file_too_large": "File skipped because of its size",
        "syntax_error": "Python syntax error detected",
        "large_file": "Very large source file",
        "high_file_complexity": "High file complexity",
        "high_symbol_complexity": "Complex symbol detected",
        "deep_nesting": "Deep nesting detected",
        "missing_module_docstring": "Module docstring is missing",
        "missing_symbol_docstrings": "Public symbols without docstrings",
        "todo_detected": "Open TODO or FIXME markers",
        "wildcard_import": "Wildcard import detected",
        "duplicate_symbol": "Symbol name occurs multiple times",
        "rec_file_too_large": (
            "Review the file size and adjust the scan limit only if required."
        ),
        "rec_syntax_error": (
            "Fix syntax errors before relying on other quality metrics."
        ),
        "rec_large_file": (
            "Split the file into smaller modules with clear responsibilities."
        ),
        "rec_file_complexity": (
            "Reduce branching and distribute responsibilities across multiple "
            "modules or functions."
        ),
        "rec_symbol_complexity": (
            "Extract logic into smaller functions and simplify control flow."
        ),
        "rec_deep_nesting": (
            "Use guard clauses, helper functions, or clearer control flow."
        ),
        "rec_module_docstring": (
            "Add a module description explaining its purpose and responsibility."
        ),
        "rec_symbol_docstrings": (
            "Document public classes, methods, and functions."
        ),
        "rec_todo": (
            "Track open markers as issues, prioritize them, or remove them."
        ),
        "rec_wildcard": "Explicitly import only the names that are required.",
        "rec_duplicate": (
            "Review naming and responsibilities of the affected symbols."
        ),
    },
}



@dataclass
class SymbolInformation:
    name: str
    symbol_type: str
    line: int
    end_line: int
    parent: str
    has_docstring: bool
    complexity: int
    maximum_nesting: int


@dataclass
class ImportInformation:
    module: str
    imported_names: list[str]
    line: int
    category: str
    wildcard: bool = False


@dataclass
class Finding:
    severity: str
    category: str
    message_key: str
    recommendation_key: str
    file: str = ""
    line: int = 0
    details: str = ""


@dataclass
class FileAnalysis:
    absolute_path: str
    relative_path: str
    module_name: str
    size_bytes: int

    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0

    module_has_docstring: bool = False

    symbols: list[SymbolInformation] = field(default_factory=list)
    imports: list[ImportInformation] = field(default_factory=list)
    todo_markers: list[dict[str, Any]] = field(default_factory=list)

    complexity: int = 0
    maximum_nesting: int = 0

    syntax_error: str = ""
    skipped_reason: str = ""

    @property
    def class_count(self) -> int:
        return sum(
            1
            for symbol in self.symbols
            if symbol.symbol_type == "class"
        )

    @property
    def function_count(self) -> int:
        return sum(
            1
            for symbol in self.symbols
            if symbol.symbol_type in {
                "function",
                "async_function",
                "method",
            }
        )

    @property
    def public_symbol_count(self) -> int:
        return sum(
            1
            for symbol in self.symbols
            if not symbol.name.startswith("_")
        )

    @property
    def documented_public_symbol_count(self) -> int:
        return sum(
            1
            for symbol in self.symbols
            if not symbol.name.startswith("_")
            and symbol.has_docstring
        )


@dataclass
class ProjectAnalysis:
    project_path: str
    generated_at: str
    files: list[FileAnalysis]
    findings: list[Finding]
    ignored_files: int
    excluded_directories: list[str]

    def totals(self) -> dict[str, Any]:
        valid_files = [
            file
            for file in self.files
            if not file.skipped_reason
        ]

        total_public_symbols = sum(
            file.public_symbol_count
            for file in valid_files
        )

        documented_public_symbols = sum(
            file.documented_public_symbol_count
            for file in valid_files
        )

        symbol_documentation_percentage = (
            documented_public_symbols
            / total_public_symbols
            * 100
            if total_public_symbols
            else 100.0
        )

        module_documentation_percentage = (
            sum(
                1
                for file in valid_files
                if file.module_has_docstring
            )
            / len(valid_files)
            * 100
            if valid_files
            else 100.0
        )

        documentation_percentage = (
            symbol_documentation_percentage * 0.70
            + module_documentation_percentage * 0.30
        )

        severity_penalties = {
            "critical": 18,
            "high": 9,
            "medium": 4,
            "low": 1,
            "info": 0,
        }

        penalty = sum(
            severity_penalties.get(finding.severity, 0)
            for finding in self.findings
        )

        documentation_bonus = documentation_percentage * 0.15

        quality_score = round(
            max(
                0,
                min(
                    100,
                    100 - penalty + documentation_bonus,
                ),
            )
        )

        return {
            "files": len(valid_files),
            "code_lines": sum(
                file.code_lines
                for file in valid_files
            ),
            "total_lines": sum(
                file.total_lines
                for file in valid_files
            ),
            "comment_lines": sum(
                file.comment_lines
                for file in valid_files
            ),
            "blank_lines": sum(
                file.blank_lines
                for file in valid_files
            ),
            "classes": sum(
                file.class_count
                for file in valid_files
            ),
            "functions": sum(
                file.function_count
                for file in valid_files
            ),
            "imports": sum(
                len(file.imports)
                for file in valid_files
            ),
            "findings": len(self.findings),
            "documentation_percentage": round(
                documentation_percentage,
                1,
            ),
            "quality_score": quality_score,
            "syntax_errors": sum(
                1
                for file in self.files
                if file.syntax_error
            ),
            "todo_markers": sum(
                len(file.todo_markers)
                for file in valid_files
            ),
            "ignored_files": self.ignored_files,
        }



class ComplexityVisitor(ast.NodeVisitor):
    """
    Aktualisiert
    """

    BRANCH_NODES = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncWith,
        ast.IfExp,
        ast.Assert,
        ast.comprehension,
        ast.Match,
    )

    def __init__(self) -> None:
        self.complexity = 1
        self.current_depth = 0
        self.maximum_depth = 0

    def generic_visit(self, node: ast.AST) -> None:
        is_branch = isinstance(
            node,
            self.BRANCH_NODES,
        )

        if is_branch:
            self.complexity += 1
            self.current_depth += 1
            self.maximum_depth = max(
                self.maximum_depth,
                self.current_depth,
            )

        if isinstance(node, ast.BoolOp):
            self.complexity += max(
                0,
                len(node.values) - 1,
            )

        if isinstance(node, ast.ExceptHandler):
            self.complexity += 1

        super().generic_visit(node)

        if is_branch:
            self.current_depth -= 1



class PythonStructureVisitor(ast.NodeVisitor):
    def __init__(
        self,
        project_modules: set[str],
    ) -> None:
        self.project_modules = project_modules
        self.symbols: list[SymbolInformation] = []
        self.imports: list[ImportInformation] = []
        self.parent_stack: list[str] = []

    @staticmethod
    def calculate_complexity(
        node: ast.AST,
    ) -> tuple[int, int]:
        visitor = ComplexityVisitor()
        visitor.visit(node)

        return (
            visitor.complexity,
            visitor.maximum_depth,
        )

    def visit_ClassDef(
        self,
        node: ast.ClassDef,
    ) -> None:
        complexity, maximum_nesting = (
            self.calculate_complexity(node)
        )

        self.symbols.append(
            SymbolInformation(
                name=node.name,
                symbol_type="class",
                line=node.lineno,
                end_line=getattr(
                    node,
                    "end_lineno",
                    node.lineno,
                ),
                parent=".".join(self.parent_stack),
                has_docstring=ast.get_docstring(node) is not None,
                complexity=complexity,
                maximum_nesting=maximum_nesting,
            )
        )

        self.parent_stack.append(node.name)
        self.generic_visit(node)
        self.parent_stack.pop()

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> None:
        self._visit_function(
            node=node,
            asynchronous=False,
        )

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:
        self._visit_function(
            node=node,
            asynchronous=True,
        )

    def _visit_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        asynchronous: bool,
    ) -> None:
        complexity, maximum_nesting = (
            self.calculate_complexity(node)
        )

        inside_class = bool(self.parent_stack)

        if inside_class:
            symbol_type = "method"
        elif asynchronous:
            symbol_type = "async_function"
        else:
            symbol_type = "function"

        self.symbols.append(
            SymbolInformation(
                name=node.name,
                symbol_type=symbol_type,
                line=node.lineno,
                end_line=getattr(
                    node,
                    "end_lineno",
                    node.lineno,
                ),
                parent=".".join(self.parent_stack),
                has_docstring=ast.get_docstring(node) is not None,
                complexity=complexity,
                maximum_nesting=maximum_nesting,
            )
        )

        self.parent_stack.append(node.name)
        self.generic_visit(node)
        self.parent_stack.pop()

    def visit_Import(
        self,
        node: ast.Import,
    ) -> None:
        for alias in node.names:
            self.imports.append(
                ImportInformation(
                    module=alias.name,
                    imported_names=[
                        alias.asname or alias.name
                    ],
                    line=node.lineno,
                    category=categorize_import(
                        alias.name,
                        self.project_modules,
                    ),
                )
            )

    def visit_ImportFrom(
        self,
        node: ast.ImportFrom,
    ) -> None:
        module = (
            "." * node.level
            + (node.module or "")
        )

        imported_names = [
            alias.asname or alias.name
            for alias in node.names
        ]

        wildcard = any(
            alias.name == "*"
            for alias in node.names
        )

        if node.level:
            category = "relative"
        else:
            category = categorize_import(
                node.module or "",
                self.project_modules,
            )

        self.imports.append(
            ImportInformation(
                module=module or ".",
                imported_names=imported_names,
                line=node.lineno,
                category=category,
                wildcard=wildcard,
            )
        )



def categorize_import(
    module: str,
    project_modules: set[str],
) -> str:
    root_module = module.split(".")[0]

    if root_module in project_modules:
        return "local"

    standard_library_modules = getattr(
        sys,
        "stdlib_module_names",
        set(),
    )

    if root_module in standard_library_modules:
        return "standard_library"

    if root_module:
        return "external"

    return "unknown"


def discover_python_files(
    project_path: Path,
) -> tuple[list[Path], int]:
    python_files: list[Path] = []
    ignored_files = 0

    for root, directory_names, file_names in os.walk(
        project_path
    ):
        directory_names[:] = [
            directory_name
            for directory_name in directory_names
            if directory_name not in EXCLUDED_DIRECTORIES
            and not directory_name.startswith(".")
        ]

        for file_name in file_names:
            file_path = Path(root) / file_name

            if (
                file_path.suffix.lower()
                in SUPPORTED_FILE_EXTENSIONS
            ):
                python_files.append(file_path)
            else:
                ignored_files += 1

    python_files.sort(
        key=lambda file_path: str(file_path).lower()
    )

    return python_files, ignored_files


def collect_project_modules(
    project_path: Path,
    python_files: Iterable[Path],
) -> set[str]:
    modules: set[str] = set()

    for file_path in python_files:
        try:
            relative_path = file_path.relative_to(
                project_path
            )
        except ValueError:
            continue

        if relative_path.parts:
            first_part = relative_path.parts[0]

            if first_part.endswith(".py"):
                first_part = Path(first_part).stem

            modules.add(first_part)

        modules.add(file_path.stem)

    return modules


def path_to_module_name(
    project_path: Path,
    file_path: Path,
) -> str:
    relative_path = file_path.relative_to(
        project_path
    ).with_suffix("")

    parts = list(relative_path.parts)

    if parts and parts[-1] == "__init__":
        parts.pop()

    return ".".join(parts) or project_path.name


def count_source_lines(
    source_code: str,
) -> tuple[int, int, int, int]:
    lines = source_code.splitlines()

    total_lines = len(lines)
    blank_lines = 0
    comment_lines = 0
    code_lines = 0

    inside_multiline_string = False
    multiline_delimiter = ""

    for raw_line in lines:
        stripped_line = raw_line.strip()

        if not stripped_line:
            blank_lines += 1
            continue

        if inside_multiline_string:
            code_lines += 1

            if (
                multiline_delimiter in stripped_line
                and stripped_line.count(
                    multiline_delimiter
                ) % 2 == 1
            ):
                inside_multiline_string = False

            continue

        if stripped_line.startswith("#"):
            comment_lines += 1
            continue

        triple_double = '"' * 3
        triple_single = "'" * 3

        if stripped_line.startswith(
            (
                triple_double,
                triple_single,
            )
        ):
            multiline_delimiter = stripped_line[:3]
            code_lines += 1

            if (
                stripped_line.count(
                    multiline_delimiter
                ) % 2 == 1
            ):
                inside_multiline_string = True

            continue

        code_lines += 1

    return (
        total_lines,
        code_lines,
        comment_lines,
        blank_lines,
    )


def find_todo_markers(
    source_code: str,
) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"\b(TODO|FIXME|HACK|XXX)\b"
        r"[:\s-]*(.*)",
        re.IGNORECASE,
    )

    markers: list[dict[str, Any]] = []

    for line_number, line in enumerate(
        source_code.splitlines(),
        start=1,
    ):
        match = pattern.search(line)

        if not match:
            continue

        markers.append(
            {
                "line": line_number,
                "tag": match.group(1).upper(),
                "text": match.group(2).strip()[:200],
            }
        )

    return markers


def read_source_file(
    file_path: Path,
) -> str:
    try:
        return file_path.read_text(
            encoding="utf-8",
        )
    except UnicodeDecodeError:
        return file_path.read_text(
            encoding="utf-8",
            errors="replace",
        )


def analyze_python_file(
    project_path: Path,
    file_path: Path,
    project_modules: set[str],
) -> FileAnalysis:
    relative_path = str(
        file_path.relative_to(project_path)
    )

    module_name = path_to_module_name(
        project_path,
        file_path,
    )

    size_bytes = file_path.stat().st_size

    if size_bytes > MAX_FILE_SIZE_BYTES:
        return FileAnalysis(
            absolute_path=str(file_path),
            relative_path=relative_path,
            module_name=module_name,
            size_bytes=size_bytes,
            skipped_reason="file_too_large",
        )

    source_code = read_source_file(file_path)

    (
        total_lines,
        code_lines,
        comment_lines,
        blank_lines,
    ) = count_source_lines(source_code)

    todo_markers = find_todo_markers(
        source_code
    )

    try:
        # Python 3.14 kann bei analysierten Fremddateien SyntaxWarning-
        # Meldungen für ungültige Escape-Sequenzen erzeugen.
        # Diese Warnungen gehören zum analysierten Projekt und sollen nicht
        # ungefiltert in der Konsole dieser Anwendung erscheinen.
        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore",
                SyntaxWarning,
            )

            syntax_tree = ast.parse(
                source_code,
                filename=str(file_path),
            )

    except SyntaxError as error:
        error_line = error.lineno or 0
        error_column = error.offset or 0

        return FileAnalysis(
            absolute_path=str(file_path),
            relative_path=relative_path,
            module_name=module_name,
            size_bytes=size_bytes,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            todo_markers=todo_markers,
            syntax_error=(
                f"{error.msg} "
                f"(line {error_line}, "
                f"column {error_column})"
            ),
        )

    structure_visitor = PythonStructureVisitor(
        project_modules=project_modules
    )

    structure_visitor.visit(syntax_tree)

    complexity_visitor = ComplexityVisitor()
    complexity_visitor.visit(syntax_tree)

    return FileAnalysis(
        absolute_path=str(file_path),
        relative_path=relative_path,
        module_name=module_name,
        size_bytes=size_bytes,
        total_lines=total_lines,
        code_lines=code_lines,
        comment_lines=comment_lines,
        blank_lines=blank_lines,
        module_has_docstring=(
            ast.get_docstring(syntax_tree)
            is not None
        ),
        symbols=structure_visitor.symbols,
        imports=structure_visitor.imports,
        todo_markers=todo_markers,
        complexity=complexity_visitor.complexity,
        maximum_nesting=(
            complexity_visitor.maximum_depth
        ),
    )


def create_findings(
    analyzed_files: list[FileAnalysis],
) -> list[Finding]:
    findings: list[Finding] = []

    symbol_locations: defaultdict[
        str,
        list[tuple[str, int]],
    ] = defaultdict(list)

    for file_analysis in analyzed_files:
        if file_analysis.skipped_reason:
            findings.append(
                Finding(
                    severity="low",
                    category="scan",
                    message_key="file_too_large",
                    recommendation_key=(
                        "rec_file_too_large"
                    ),
                    file=file_analysis.relative_path,
                    details=(
                        f"{format_file_size(file_analysis.size_bytes)}"
                    ),
                )
            )

            continue

        if file_analysis.syntax_error:
            findings.append(
                Finding(
                    severity="critical",
                    category="syntax",
                    message_key="syntax_error",
                    recommendation_key=(
                        "rec_syntax_error"
                    ),
                    file=file_analysis.relative_path,
                    details=file_analysis.syntax_error,
                )
            )

            continue

        if (
            file_analysis.total_lines
            >= LARGE_FILE_LINE_LIMIT
        ):
            findings.append(
                Finding(
                    severity="medium",
                    category="maintainability",
                    message_key="large_file",
                    recommendation_key="rec_large_file",
                    file=file_analysis.relative_path,
                    details=(
                        f"{file_analysis.total_lines} lines"
                    ),
                )
            )

        if (
            file_analysis.complexity
            >= HIGH_FILE_COMPLEXITY_LIMIT
        ):
            severity = (
                "high"
                if file_analysis.complexity >= 45
                else "medium"
            )

            findings.append(
                Finding(
                    severity=severity,
                    category="complexity",
                    message_key=(
                        "high_file_complexity"
                    ),
                    recommendation_key=(
                        "rec_file_complexity"
                    ),
                    file=file_analysis.relative_path,
                    details=(
                        f"complexity="
                        f"{file_analysis.complexity}"
                    ),
                )
            )

        if (
            file_analysis.maximum_nesting
            >= DEEP_NESTING_LIMIT
        ):
            findings.append(
                Finding(
                    severity="medium",
                    category="complexity",
                    message_key="deep_nesting",
                    recommendation_key=(
                        "rec_deep_nesting"
                    ),
                    file=file_analysis.relative_path,
                    details=(
                        f"depth="
                        f"{file_analysis.maximum_nesting}"
                    ),
                )
            )

        if not file_analysis.module_has_docstring:
            findings.append(
                Finding(
                    severity="low",
                    category="documentation",
                    message_key=(
                        "missing_module_docstring"
                    ),
                    recommendation_key=(
                        "rec_module_docstring"
                    ),
                    file=file_analysis.relative_path,
                )
            )

        undocumented_symbols = [
            symbol
            for symbol in file_analysis.symbols
            if not symbol.name.startswith("_")
            and not symbol.has_docstring
        ]

        if undocumented_symbols:
            severity = (
                "medium"
                if len(undocumented_symbols) >= 5
                else "low"
            )

            findings.append(
                Finding(
                    severity=severity,
                    category="documentation",
                    message_key=(
                        "missing_symbol_docstrings"
                    ),
                    recommendation_key=(
                        "rec_symbol_docstrings"
                    ),
                    file=file_analysis.relative_path,
                    details=", ".join(
                        symbol.name
                        for symbol
                        in undocumented_symbols[:10]
                    ),
                )
            )

        if file_analysis.todo_markers:
            first_marker = (
                file_analysis.todo_markers[0]
            )

            findings.append(
                Finding(
                    severity="low",
                    category="maintenance",
                    message_key="todo_detected",
                    recommendation_key="rec_todo",
                    file=file_analysis.relative_path,
                    line=first_marker["line"],
                    details=(
                        f"{len(file_analysis.todo_markers)} "
                        f"marker(s)"
                    ),
                )
            )

        for import_information in (
            file_analysis.imports
        ):
            if import_information.wildcard:
                findings.append(
                    Finding(
                        severity="medium",
                        category="imports",
                        message_key="wildcard_import",
                        recommendation_key=(
                            "rec_wildcard"
                        ),
                        file=(
                            file_analysis.relative_path
                        ),
                        line=import_information.line,
                        details=(
                            import_information.module
                        ),
                    )
                )

        for symbol in file_analysis.symbols:
            if (
                symbol.complexity
                >= HIGH_SYMBOL_COMPLEXITY_LIMIT
            ):
                findings.append(
                    Finding(
                        severity=(
                            "high"
                            if symbol.complexity >= 20
                            else "medium"
                        ),
                        category="complexity",
                        message_key=(
                            "high_symbol_complexity"
                        ),
                        recommendation_key=(
                            "rec_symbol_complexity"
                        ),
                        file=(
                            file_analysis.relative_path
                        ),
                        line=symbol.line,
                        details=(
                            f"{symbol.name}: "
                            f"{symbol.complexity}"
                        ),
                    )
                )

            if not symbol.name.startswith("_"):
                symbol_locations[symbol.name].append(
                    (
                        file_analysis.relative_path,
                        symbol.line,
                    )
                )

    for symbol_name, locations in (
        symbol_locations.items()
    ):
        unique_files = {
            file_name
            for file_name, _ in locations
        }

        if len(unique_files) < 3:
            continue

        first_file, first_line = locations[0]

        findings.append(
            Finding(
                severity="info",
                category="architecture",
                message_key="duplicate_symbol",
                recommendation_key="rec_duplicate",
                file=first_file,
                line=first_line,
                details=(
                    f"{symbol_name}: "
                    f"{len(locations)} occurrences"
                ),
            )
        )

    severity_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
        "info": 4,
    }

    findings.sort(
        key=lambda finding: (
            severity_order.get(
                finding.severity,
                99,
            ),
            finding.file.lower(),
            finding.line,
        )
    )

    return findings


def analyze_project(
    project_path: Path,
) -> ProjectAnalysis:
    python_files, ignored_files = (
        discover_python_files(project_path)
    )

    project_modules = collect_project_modules(
        project_path,
        python_files,
    )

    analyzed_files = [
        analyze_python_file(
            project_path=project_path,
            file_path=file_path,
            project_modules=project_modules,
        )
        for file_path in python_files
    ]

    findings = create_findings(
        analyzed_files
    )

    return ProjectAnalysis(
        project_path=str(project_path),
        generated_at=(
            datetime.now()
            .astimezone()
            .isoformat(timespec="seconds")
        ),
        files=analyzed_files,
        findings=findings,
        ignored_files=ignored_files,
        excluded_directories=sorted(
            EXCLUDED_DIRECTORIES
        ),
    )



def format_number(
    value: int | float,
) -> str:
    if isinstance(value, float):
        return f"{value:,.1f}".replace(",", " ")

    return f"{value:,}".replace(",", " ")


def format_file_size(
    size_bytes: int,
) -> str:
    size = float(size_bytes)

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"

            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size_bytes} B"


def open_folder_in_file_manager(
    folder_path: Path,
) -> None:
    operating_system = platform.system()

    if operating_system == "Windows":
        os.startfile(folder_path)  # type: ignore[attr-defined]
        return

    if operating_system == "Darwin":
        subprocess.Popen(
            ["open", str(folder_path)]
        )
        return

    subprocess.Popen(
        ["xdg-open", str(folder_path)]
    )



class ModernTreeview(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        columns: list[str],
        column_widths: dict[str, int],
    ) -> None:
        super().__init__(
            master,
            corner_radius=14,
        )

        self.columns = columns
        self.column_widths = column_widths

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            0,
            weight=1,
        )

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Codebase.Treeview",
            rowheight=30,
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        style.configure(
            "Codebase.Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )

        style.map(
            "Codebase.Treeview",
            background=[
                ("selected", "#1F6AA5"),
            ],
            foreground=[
                ("selected", "#FFFFFF"),
            ],
        )

        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings",
            style="Codebase.Treeview",
        )

        for column in self.columns:
            self.tree.heading(
                column,
                text=column,
            )

            self.tree.column(
                column,
                width=self.column_widths.get(
                    column,
                    150,
                ),
                minwidth=70,
                stretch=True,
                anchor="w",
            )

        self.vertical_scrollbar = (
            ctk.CTkScrollbar(
                self,
                orientation="vertical",
                command=self.tree.yview,
            )
        )

        self.horizontal_scrollbar = (
            ctk.CTkScrollbar(
                self,
                orientation="horizontal",
                command=self.tree.xview,
            )
        )

        self.tree.configure(
            yscrollcommand=(
                self.vertical_scrollbar.set
            ),
            xscrollcommand=(
                self.horizontal_scrollbar.set
            ),
        )

        self.tree.grid(
            row=0,
            column=0,
            padx=(10, 2),
            pady=(10, 2),
            sticky="nsew",
        )

        self.vertical_scrollbar.grid(
            row=0,
            column=1,
            padx=(2, 10),
            pady=(10, 2),
            sticky="ns",
        )

        self.horizontal_scrollbar.grid(
            row=1,
            column=0,
            padx=(10, 2),
            pady=(2, 10),
            sticky="ew",
        )

    def set_headings(
        self,
        headings: dict[str, str],
    ) -> None:
        for column, heading in headings.items():
            self.tree.heading(
                column,
                text=heading,
            )

    def clear(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert(
        self,
        values: Iterable[Any],
        tags: tuple[str, ...] = (),
    ) -> None:
        self.tree.insert(
            "",
            "end",
            values=list(values),
            tags=tags,
        )

    def configure_tag(
        self,
        tag: str,
        **options: Any,
    ) -> None:
        self.tree.tag_configure(
            tag,
            **options,
        )



class MetricCard(ctk.CTkFrame):
    def __init__(
        self,
        master: Any,
        title: str,
    ) -> None:
        super().__init__(
            master,
            corner_radius=16,
            border_width=1,
        )

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.value_label = ctk.CTkLabel(
            self,
            text="—",
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
            anchor="w",
        )

        self.value_label.grid(
            row=0,
            column=0,
            padx=18,
            pady=(16, 2),
            sticky="ew",
        )

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(
                size=13,
            ),
            text_color=(
                "gray35",
                "gray70",
            ),
            anchor="w",
        )

        self.title_label.grid(
            row=1,
            column=0,
            padx=18,
            pady=(0, 16),
            sticky="ew",
        )

    def update_content(
        self,
        title: str,
        value: str,
    ) -> None:
        self.title_label.configure(
            text=title
        )

        self.value_label.configure(
            text=value
        )



class CodebaseCartographerApplication(
    ctk.CTk
):
    def __init__(self) -> None:
        super().__init__()

        self.language = "de"

        self.project_path: Path | None = None
        self.analysis_result: ProjectAnalysis | None = None
        self.analysis_thread: threading.Thread | None = None

        self.current_page = "dashboard"

        self.navigation_buttons: dict[
            str,
            ctk.CTkButton,
        ] = {}

        self.pages: dict[
            str,
            ctk.CTkFrame,
        ] = {}

        self.metric_cards: dict[
            str,
            MetricCard,
        ] = {}

        self.title(
            f"{APP_TITLE} {APP_VERSION}"
        )

        self.geometry(
            f"{DEFAULT_WINDOW_WIDTH}x"
            f"{DEFAULT_WINDOW_HEIGHT}"
        )

        self.minsize(
            1180,
            720,
        )

        self.grid_columnconfigure(
            1,
            weight=1,
        )

        self.grid_rowconfigure(
            0,
            weight=1,
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.destroy,
        )

        self._build_sidebar()
        self._build_main_area()
        self._apply_language()
        self._show_page("dashboard")

    def tr(
        self,
        key: str,
    ) -> str:
        return TRANSLATIONS[
            self.language
        ].get(
            key,
            key,
        )

    def _build_sidebar(self) -> None:
        self.sidebar = ctk.CTkFrame(
            self,
            width=265,
            corner_radius=0,
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(
            0,
            weight=1,
        )

        self.sidebar.grid_rowconfigure(
            10,
            weight=1,
        )

        self.application_name_label = (
            ctk.CTkLabel(
                self.sidebar,
                text=APP_NAME,
                font=ctk.CTkFont(
                    size=24,
                    weight="bold",
                ),
                anchor="w",
                justify="left",
                wraplength=215,
            )
        )

        self.application_name_label.grid(
            row=0,
            column=0,
            padx=22,
            pady=(26, 4),
            sticky="ew",
        )

        self.version_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Version {APP_VERSION}",
            text_color=(
                "gray35",
                "gray65",
            ),
            anchor="w",
        )

        self.version_label.grid(
            row=1,
            column=0,
            padx=22,
            pady=(0, 20),
            sticky="ew",
        )

        navigation_items = [
            ("dashboard", "dashboard"),
            ("files", "files"),
            ("symbols", "symbols"),
            (
                "dependencies",
                "dependencies",
            ),
            ("findings", "findings"),
            ("report", "report"),
        ]

        for row_index, (
            page_name,
            translation_key,
        ) in enumerate(
            navigation_items,
            start=2,
        ):
            button = ctk.CTkButton(
                self.sidebar,
                text=translation_key,
                height=42,
                corner_radius=10,
                anchor="w",
                fg_color="transparent",
                hover_color=(
                    "gray82",
                    "gray25",
                ),
                command=(
                    lambda name=page_name:
                    self._show_page(name)
                ),
            )

            button.grid(
                row=row_index,
                column=0,
                padx=14,
                pady=4,
                sticky="ew",
            )

            self.navigation_buttons[
                page_name
            ] = button

        self.appearance_label = (
            ctk.CTkLabel(
                self.sidebar,
                text="",
                anchor="w",
                text_color=(
                    "gray35",
                    "gray70",
                ),
            )
        )

        self.appearance_label.grid(
            row=11,
            column=0,
            padx=20,
            pady=(12, 5),
            sticky="ew",
        )

        self.appearance_menu = (
            ctk.CTkOptionMenu(
                self.sidebar,
                values=[],
                command=(
                    self._change_appearance
                ),
            )
        )

        self.appearance_menu.grid(
            row=12,
            column=0,
            padx=18,
            pady=(0, 8),
            sticky="ew",
        )

        self.language_button = (
            ctk.CTkButton(
                self.sidebar,
                text="EN",
                height=40,
                command=(
                    self._toggle_language
                ),
            )
        )

        self.language_button.grid(
            row=13,
            column=0,
            padx=18,
            pady=5,
            sticky="ew",
        )

        self.github_button = (
            ctk.CTkButton(
                self.sidebar,
                text="GitHub",
                height=40,
                fg_color=(
                    "gray28",
                    "gray18",
                ),
                hover_color=(
                    "gray38",
                    "gray28",
                ),
                command=(
                    self._open_github
                ),
            )
        )

        self.github_button.grid(
            row=14,
            column=0,
            padx=18,
            pady=5,
            sticky="ew",
        )

        self.about_button = (
            ctk.CTkButton(
                self.sidebar,
                text="Info",
                height=40,
                fg_color="transparent",
                border_width=1,
                command=self._show_about_dialog,
            )
        )

        self.about_button.grid(
            row=15,
            column=0,
            padx=18,
            pady=(5, 18),
            sticky="ew",
        )

    def _build_main_area(self) -> None:
        self.main_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent",
        )

        self.main_area.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.main_area.grid_columnconfigure(
            0,
            weight=1,
        )

        self.main_area.grid_rowconfigure(
            2,
            weight=1,
        )

        self._build_topbar()
        self._build_statusbar()
        self._build_pages()

    def _build_topbar(self) -> None:
        self.topbar = ctk.CTkFrame(
            self.main_area,
            corner_radius=0,
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.topbar.grid_columnconfigure(
            1,
            weight=1,
        )

        self.select_project_button = (
            ctk.CTkButton(
                self.topbar,
                text="",
                width=160,
                height=42,
                command=(
                    self._select_project
                ),
            )
        )

        self.select_project_button.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=16,
        )

        self.project_path_label = (
            ctk.CTkLabel(
                self.topbar,
                text="",
                anchor="w",
                text_color=(
                    "gray35",
                    "gray70",
                ),
            )
        )

        self.project_path_label.grid(
            row=0,
            column=1,
            padx=8,
            pady=16,
            sticky="ew",
        )

        self.open_folder_button = (
            ctk.CTkButton(
                self.topbar,
                text="",
                width=125,
                height=42,
                fg_color="transparent",
                border_width=1,
                command=(
                    self._open_project_folder
                ),
            )
        )

        self.open_folder_button.grid(
            row=0,
            column=2,
            padx=6,
            pady=16,
        )

        self.analyze_button = (
            ctk.CTkButton(
                self.topbar,
                text="",
                width=150,
                height=42,
                command=(
                    self._start_analysis
                ),
            )
        )

        self.analyze_button.grid(
            row=0,
            column=3,
            padx=(6, 20),
            pady=16,
        )

    def _build_statusbar(self) -> None:
        self.statusbar = ctk.CTkFrame(
            self.main_area,
            corner_radius=0,
            height=38,
        )

        self.statusbar.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.statusbar.grid_columnconfigure(
            1,
            weight=1,
        )

        self.progressbar = (
            ctk.CTkProgressBar(
                self.statusbar,
                width=130,
                mode="indeterminate",
            )
        )

        self.progressbar.grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=10,
        )

        self.progressbar.set(0)

        self.status_label = ctk.CTkLabel(
            self.statusbar,
            text="",
            anchor="w",
            text_color=(
                "gray35",
                "gray70",
            ),
        )

        self.status_label.grid(
            row=0,
            column=1,
            padx=5,
            pady=8,
            sticky="ew",
        )

    def _build_pages(self) -> None:
        self.page_container = ctk.CTkFrame(
            self.main_area,
            corner_radius=0,
            fg_color="transparent",
        )

        self.page_container.grid(
            row=2,
            column=0,
            sticky="nsew",
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1,
        )

        self.page_container.grid_rowconfigure(
            0,
            weight=1,
        )

        self._build_dashboard_page()
        self._build_files_page()
        self._build_symbols_page()
        self._build_dependencies_page()
        self._build_findings_page()
        self._build_report_page()

    def _create_page(
        self,
        page_name: str,
    ) -> ctk.CTkFrame:
        page = ctk.CTkFrame(
            self.page_container,
            corner_radius=0,
            fg_color="transparent",
        )

        page.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.pages[page_name] = page

        return page

    def _create_page_header(
        self,
        page: ctk.CTkFrame,
    ) -> tuple[
        ctk.CTkLabel,
        ctk.CTkLabel,
    ]:
        page.grid_columnconfigure(
            0,
            weight=1,
        )

        title_label = ctk.CTkLabel(
            page,
            text="",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
            anchor="w",
        )

        title_label.grid(
            row=0,
            column=0,
            padx=24,
            pady=(22, 2),
            sticky="ew",
        )

        subtitle_label = ctk.CTkLabel(
            page,
            text="",
            anchor="w",
            justify="left",
            wraplength=1050,
            text_color=(
                "gray35",
                "gray70",
            ),
        )

        subtitle_label.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 16),
            sticky="ew",
        )

        return (
            title_label,
            subtitle_label,
        )

    def _build_dashboard_page(self) -> None:
        page = self._create_page(
            "dashboard"
        )

        (
            self.dashboard_title_label,
            self.dashboard_subtitle_label,
        ) = self._create_page_header(page)

        page.grid_rowconfigure(
            3,
            weight=1,
        )

        metric_container = ctk.CTkFrame(
            page,
            corner_radius=0,
            fg_color="transparent",
        )

        metric_container.grid(
            row=2,
            column=0,
            padx=18,
            pady=(0, 10),
            sticky="ew",
        )

        for column_index in range(4):
            metric_container.grid_columnconfigure(
                column_index,
                weight=1,
            )

        metric_definitions = [
            ("files", "files_scanned"),
            ("code_lines", "code_lines"),
            ("classes", "classes"),
            ("functions", "functions"),
            ("imports", "imports"),
            (
                "findings",
                "findings_count",
            ),
            (
                "documentation_percentage",
                "documentation",
            ),
            (
                "quality_score",
                "quality_score",
            ),
        ]

        for index, (
            metric_key,
            title_key,
        ) in enumerate(metric_definitions):
            card = MetricCard(
                metric_container,
                title_key,
            )

            card.grid(
                row=index // 4,
                column=index % 4,
                padx=6,
                pady=6,
                sticky="nsew",
            )

            self.metric_cards[
                metric_key
            ] = card

        self.dashboard_text = (
            ctk.CTkTextbox(
                page,
                corner_radius=14,
                wrap="word",
                font=ctk.CTkFont(
                    family="Consolas",
                    size=13,
                ),
            )
        )

        self.dashboard_text.grid(
            row=3,
            column=0,
            padx=24,
            pady=(8, 24),
            sticky="nsew",
        )

        self.dashboard_text.configure(
            state="disabled"
        )

    def _build_files_page(self) -> None:
        page = self._create_page(
            "files"
        )

        (
            self.files_title_label,
            self.files_subtitle_label,
        ) = self._create_page_header(page)

        page.grid_rowconfigure(
            3,
            weight=1,
        )

        self.file_filter_entry = (
            ctk.CTkEntry(
                page,
                placeholder_text="",
            )
        )

        self.file_filter_entry.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        self.file_filter_entry.bind(
            "<KeyRelease>",
            lambda _event:
            self._render_files(),
        )

        file_columns = [
            "file",
            "lines",
            "size",
            "classes",
            "functions",
            "imports",
            "complexity",
            "status",
        ]

        self.files_table = ModernTreeview(
            page,
            columns=file_columns,
            column_widths={
                "file": 400,
                "lines": 80,
                "size": 90,
                "classes": 80,
                "functions": 90,
                "imports": 80,
                "complexity": 100,
                "status": 180,
            },
        )

        self.files_table.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew",
        )

    def _build_symbols_page(self) -> None:
        page = self._create_page(
            "symbols"
        )

        (
            self.symbols_title_label,
            self.symbols_subtitle_label,
        ) = self._create_page_header(page)

        page.grid_rowconfigure(
            3,
            weight=1,
        )

        self.symbol_filter_entry = (
            ctk.CTkEntry(
                page,
                placeholder_text="",
            )
        )

        self.symbol_filter_entry.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        self.symbol_filter_entry.bind(
            "<KeyRelease>",
            lambda _event:
            self._render_symbols(),
        )

        symbol_columns = [
            "module",
            "symbol",
            "type",
            "parent",
            "line",
            "complexity",
            "docstring",
        ]

        self.symbols_table = ModernTreeview(
            page,
            columns=symbol_columns,
            column_widths={
                "module": 260,
                "symbol": 250,
                "type": 130,
                "parent": 220,
                "line": 70,
                "complexity": 100,
                "docstring": 90,
            },
        )

        self.symbols_table.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew",
        )

    def _build_dependencies_page(self) -> None:
        page = self._create_page(
            "dependencies"
        )

        (
            self.dependencies_title_label,
            self.dependencies_subtitle_label,
        ) = self._create_page_header(page)

        page.grid_rowconfigure(
            2,
            weight=1,
        )

        dependency_columns = [
            "dependency",
            "category",
            "count",
            "used_by",
        ]

        self.dependencies_table = (
            ModernTreeview(
                page,
                columns=dependency_columns,
                column_widths={
                    "dependency": 280,
                    "category": 170,
                    "count": 90,
                    "used_by": 650,
                },
            )
        )

        self.dependencies_table.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew",
        )

    def _build_findings_page(self) -> None:
        page = self._create_page(
            "findings"
        )

        (
            self.findings_title_label,
            self.findings_subtitle_label,
        ) = self._create_page_header(page)

        page.grid_rowconfigure(
            3,
            weight=1,
        )

        self.finding_filter_entry = (
            ctk.CTkEntry(
                page,
                placeholder_text="",
            )
        )

        self.finding_filter_entry.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        self.finding_filter_entry.bind(
            "<KeyRelease>",
            lambda _event:
            self._render_findings(),
        )

        finding_columns = [
            "severity",
            "file",
            "category",
            "description",
            "recommendation",
        ]

        self.findings_table = (
            ModernTreeview(
                page,
                columns=finding_columns,
                column_widths={
                    "severity": 100,
                    "file": 280,
                    "category": 150,
                    "description": 390,
                    "recommendation": 470,
                },
            )
        )

        self.findings_table.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew",
        )

        self.findings_table.configure_tag(
            "critical",
            foreground="#D32F2F",
        )

        self.findings_table.configure_tag(
            "high",
            foreground="#E65100",
        )

        self.findings_table.configure_tag(
            "medium",
            foreground="#B8860B",
        )

    def _build_report_page(self) -> None:
        page = self._create_page(
            "report"
        )

        (
            self.report_title_label,
            self.report_subtitle_label,
        ) = self._create_page_header(page)

        page.grid_rowconfigure(
            3,
            weight=1,
        )

        action_frame = ctk.CTkFrame(
            page,
            corner_radius=0,
            fg_color="transparent",
        )

        action_frame.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        self.export_json_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                width=155,
                command=self._export_json,
            )
        )

        self.export_json_button.pack(
            side="left",
            padx=(0, 8),
        )

        self.export_markdown_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                width=180,
                fg_color="transparent",
                border_width=1,
                command=(
                    self._export_markdown
                ),
            )
        )

        self.export_markdown_button.pack(
            side="left",
            padx=8,
        )

        self.report_text = ctk.CTkTextbox(
            page,
            corner_radius=14,
            wrap="word",
            font=ctk.CTkFont(
                family="Consolas",
                size=13,
            ),
        )

        self.report_text.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew",
        )

        self.report_text.configure(
            state="disabled"
        )

    def _toggle_language(self) -> None:
        self.language = (
            "en"
            if self.language == "de"
            else "de"
        )

        self._apply_language()

    def _apply_language(self) -> None:
        self.language_button.configure(
            text=self.tr(
                "language_button"
            )
        )

        self.github_button.configure(
            text=self.tr("github")
        )

        self.about_button.configure(
            text=self.tr("about")
        )

        self.appearance_label.configure(
            text=self.tr("appearance")
        )

        self.select_project_button.configure(
            text=self.tr("select_project")
        )

        self.open_folder_button.configure(
            text=self.tr("open_folder")
        )

        self.analyze_button.configure(
            text=self.tr("analyze_project")
        )

        for page_name, button in (
            self.navigation_buttons.items()
        ):
            button.configure(
                text=self.tr(page_name)
            )

        appearance_values = [
            self.tr("dark"),
            self.tr("light"),
            self.tr("system"),
        ]

        self.appearance_menu.configure(
            values=appearance_values
        )

        current_mode = (
            ctk.get_appearance_mode()
        )

        if current_mode == "Light":
            self.appearance_menu.set(
                self.tr("light")
            )
        else:
            self.appearance_menu.set(
                self.tr("dark")
            )

        self.dashboard_title_label.configure(
            text=self.tr("dashboard")
        )

        self.files_title_label.configure(
            text=self.tr("files")
        )

        self.symbols_title_label.configure(
            text=self.tr("symbols")
        )

        self.dependencies_title_label.configure(
            text=self.tr("dependencies")
        )

        self.findings_title_label.configure(
            text=self.tr("findings")
        )

        self.report_title_label.configure(
            text=self.tr("report")
        )

        for subtitle_label in [
            self.dashboard_subtitle_label,
            self.files_subtitle_label,
            self.symbols_subtitle_label,
            self.dependencies_subtitle_label,
            self.findings_subtitle_label,
            self.report_subtitle_label,
        ]:
            subtitle_label.configure(
                text=self.tr("analysis_hint")
            )

        self.file_filter_entry.configure(
            placeholder_text=self.tr(
                "filter_files"
            )
        )

        self.symbol_filter_entry.configure(
            placeholder_text=self.tr(
                "filter_symbols"
            )
        )

        self.finding_filter_entry.configure(
            placeholder_text=self.tr(
                "filter_findings"
            )
        )

        self.export_json_button.configure(
            text=self.tr("export_json")
        )

        self.export_markdown_button.configure(
            text=self.tr(
                "export_markdown"
            )
        )

        metric_translation_keys = {
            "files": "files_scanned",
            "code_lines": "code_lines",
            "classes": "classes",
            "functions": "functions",
            "imports": "imports",
            "findings": "findings_count",
            "documentation_percentage": (
                "documentation"
            ),
            "quality_score": "quality_score",
        }

        for metric_key, translation_key in (
            metric_translation_keys.items()
        ):
            card = self.metric_cards[
                metric_key
            ]

            current_value = (
                card.value_label.cget("text")
            )

            card.update_content(
                title=self.tr(
                    translation_key
                ),
                value=current_value,
            )

        self.files_table.set_headings(
            {
                "file": self.tr("file"),
                "lines": self.tr("lines"),
                "size": self.tr("size"),
                "classes": self.tr("classes"),
                "functions": self.tr("functions"),
                "imports": self.tr("imports"),
                "complexity": self.tr(
                    "complexity"
                ),
                "status": self.tr("status"),
            }
        )

        self.symbols_table.set_headings(
            {
                "module": self.tr("module"),
                "symbol": self.tr("symbol"),
                "type": self.tr("type"),
                "parent": self.tr("parent"),
                "line": self.tr("line"),
                "complexity": self.tr(
                    "complexity"
                ),
                "docstring": self.tr(
                    "docstring"
                ),
            }
        )

        self.dependencies_table.set_headings(
            {
                "dependency": self.tr(
                    "dependency"
                ),
                "category": self.tr(
                    "category"
                ),
                "count": self.tr("count"),
                "used_by": self.tr("used_by"),
            }
        )

        self.findings_table.set_headings(
            {
                "severity": self.tr(
                    "severity"
                ),
                "file": self.tr("file"),
                "category": self.tr(
                    "category"
                ),
                "description": self.tr(
                    "description"
                ),
                "recommendation": self.tr(
                    "recommendation"
                ),
            }
        )

        self._update_project_path_label()
        self._set_status(
            self.tr("ready")
        )

        self._render_all()

    def _change_appearance(
        self,
        selected_value: str,
    ) -> None:
        mapping = {
            TRANSLATIONS["de"]["dark"]: (
                "Dark"
            ),
            TRANSLATIONS["de"]["light"]: (
                "Light"
            ),
            TRANSLATIONS["de"]["system"]: (
                "System"
            ),
            TRANSLATIONS["en"]["dark"]: (
                "Dark"
            ),
            TRANSLATIONS["en"]["light"]: (
                "Light"
            ),
            TRANSLATIONS["en"]["system"]: (
                "System"
            ),
        }

        ctk.set_appearance_mode(
            mapping.get(
                selected_value,
                "Dark",
            )
        )

    def _show_page(
        self,
        page_name: str,
    ) -> None:
        self.current_page = page_name

        self.pages[
            page_name
        ].tkraise()

        for name, button in (
            self.navigation_buttons.items()
        ):
            if name == page_name:
                button.configure(
                    fg_color=(
                        "gray75",
                        "gray30",
                    )
                )
            else:
                button.configure(
                    fg_color="transparent"
                )

    def _set_status(
        self,
        text: str,
        busy: bool = False,
    ) -> None:
        self.status_label.configure(
            text=text
        )

        if busy:
            self.progressbar.start()
        else:
            self.progressbar.stop()
            self.progressbar.set(0)

    def _update_project_path_label(
        self,
    ) -> None:
        if self.project_path:
            text = str(self.project_path)
        else:
            text = self.tr("no_project")

        self.project_path_label.configure(
            text=text
        )

    def _select_project(self) -> None:
        selected_directory = (
            filedialog.askdirectory(
                title=self.tr(
                    "select_project"
                ),
                mustexist=True,
            )
        )

        if not selected_directory:
            self._set_status(
                self.tr(
                    "operation_cancelled"
                )
            )

            return

        candidate_path = Path(
            selected_directory
        ).resolve()

        if not candidate_path.is_dir():
            messagebox.showerror(
                APP_NAME,
                self.tr("invalid_project"),
            )

            return

        self.project_path = candidate_path
        self.analysis_result = None

        self._update_project_path_label()

        self._set_status(
            f"{self.tr('project_selected')}: "
            f"{candidate_path.name}"
        )

        self._reset_views()

    def _start_analysis(self) -> None:
        if (
            not self.project_path
            or not self.project_path.is_dir()
        ):
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "select_project_first"
                ),
            )

            return

        if (
            self.analysis_thread
            and self.analysis_thread.is_alive()
        ):
            return

        self.analyze_button.configure(
            state="disabled"
        )

        self.select_project_button.configure(
            state="disabled"
        )

        self._set_status(
            self.tr("analysis_running"),
            busy=True,
        )

        self.analysis_thread = (
            threading.Thread(
                target=self._analysis_worker,
                daemon=True,
            )
        )

        self.analysis_thread.start()

    def _analysis_worker(self) -> None:
        try:
            if self.project_path is None:
                raise RuntimeError(
                    "No project path selected."
                )

            result = analyze_project(
                self.project_path
            )

            self.after(
                0,
                lambda:
                self._analysis_finished(
                    result
                ),
            )

        except Exception as error:
            self.after(
                0,
                lambda:
                self._analysis_failed(
                    error
                ),
            )

    def _analysis_finished(
        self,
        result: ProjectAnalysis,
    ) -> None:
        self.analysis_result = result

        self.analyze_button.configure(
            state="normal"
        )

        self.select_project_button.configure(
            state="normal"
        )

        totals = result.totals()

        self._set_status(
            self.tr("scan_summary").format(
                files=totals["files"],
                lines=totals["code_lines"],
                findings=totals["findings"],
            )
        )

        self._render_all()
        self._show_page("dashboard")

    def _analysis_failed(
        self,
        error: Exception,
    ) -> None:
        self.analyze_button.configure(
            state="normal"
        )

        self.select_project_button.configure(
            state="normal"
        )

        self._set_status(
            self.tr("analysis_failed")
        )

        messagebox.showerror(
            self.tr("analysis_failed"),
            f"{type(error).__name__}: {error}",
        )

    def _reset_views(self) -> None:
        for card in self.metric_cards.values():
            card.value_label.configure(
                text="—"
            )

        self._set_textbox_content(
            self.dashboard_text,
            self.tr("analysis_hint"),
        )

        self._set_textbox_content(
            self.report_text,
            self.tr("analysis_hint"),
        )

        self.files_table.clear()
        self.symbols_table.clear()
        self.dependencies_table.clear()
        self.findings_table.clear()

    def _render_all(self) -> None:
        if not self.analysis_result:
            self._reset_views()
            return

        self._render_dashboard()
        self._render_files()
        self._render_symbols()
        self._render_dependencies()
        self._render_findings()
        self._render_report()

    def _render_dashboard(self) -> None:
        if not self.analysis_result:
            return

        totals = self.analysis_result.totals()

        metric_values = {
            "files": format_number(
                totals["files"]
            ),
            "code_lines": format_number(
                totals["code_lines"]
            ),
            "classes": format_number(
                totals["classes"]
            ),
            "functions": format_number(
                totals["functions"]
            ),
            "imports": format_number(
                totals["imports"]
            ),
            "findings": format_number(
                totals["findings"]
            ),
            "documentation_percentage": (
                f"{totals['documentation_percentage']:.1f} %"
            ),
            "quality_score": (
                f"{totals['quality_score']} / 100"
            ),
        }

        for metric_key, value in (
            metric_values.items()
        ):
            self.metric_cards[
                metric_key
            ].value_label.configure(
                text=value
            )

        dependency_counter = Counter(
            import_information.module
            for file_analysis
            in self.analysis_result.files
            for import_information
            in file_analysis.imports
        )

        complex_files = sorted(
            [
                file_analysis
                for file_analysis
                in self.analysis_result.files
                if not file_analysis.skipped_reason
                and not file_analysis.syntax_error
            ],
            key=lambda file_analysis:
            file_analysis.complexity,
            reverse=True,
        )[:10]

        lines = [
            self.tr("project_information"),
            "=" * 80,
            "",
            (
                f"{self.tr('project_path')}: "
                f"{self.analysis_result.project_path}"
            ),
            (
                f"{self.tr('generated_at')}: "
                f"{self.analysis_result.generated_at}"
            ),
            "",
            (
                f"{self.tr('total_lines')}: "
                f"{format_number(totals['total_lines'])}"
            ),
            (
                f"{self.tr('code_lines')}: "
                f"{format_number(totals['code_lines'])}"
            ),
            (
                f"{self.tr('comment_lines')}: "
                f"{format_number(totals['comment_lines'])}"
            ),
            (
                f"{self.tr('blank_lines')}: "
                f"{format_number(totals['blank_lines'])}"
            ),
            (
                f"{self.tr('syntax_errors')}: "
                f"{totals['syntax_errors']}"
            ),
            (
                f"{self.tr('todo_markers')}: "
                f"{totals['todo_markers']}"
            ),
            (
                f"{self.tr('ignored_files')}: "
                f"{totals['ignored_files']}"
            ),
            "",
            self.tr("top_dependencies"),
            "-" * 80,
        ]

        if dependency_counter:
            for module, count in (
                dependency_counter.most_common(12)
            ):
                lines.append(
                    f"{module:<45} {count}"
                )
        else:
            lines.append(
                self.tr("no_data")
            )

        lines.extend(
            [
                "",
                self.tr("complex_files"),
                "-" * 80,
            ]
        )

        if complex_files:
            for file_analysis in (
                complex_files
            ):
                lines.append(
                    f"{file_analysis.relative_path:<60} "
                    f"{file_analysis.complexity}"
                )
        else:
            lines.append(
                self.tr("no_data")
            )

        self._set_textbox_content(
            self.dashboard_text,
            "\n".join(lines),
        )

    def _render_files(self) -> None:
        self.files_table.clear()

        if not self.analysis_result:
            return

        search_term = (
            self.file_filter_entry
            .get()
            .strip()
            .lower()
        )

        for file_analysis in (
            self.analysis_result.files
        ):
            if (
                search_term
                and search_term
                not in
                file_analysis.relative_path.lower()
            ):
                continue

            status = self._file_status(
                file_analysis
            )

            self.files_table.insert(
                [
                    file_analysis.relative_path,
                    file_analysis.code_lines,
                    format_file_size(
                        file_analysis.size_bytes
                    ),
                    file_analysis.class_count,
                    file_analysis.function_count,
                    len(file_analysis.imports),
                    file_analysis.complexity,
                    status,
                ]
            )

    def _render_symbols(self) -> None:
        self.symbols_table.clear()

        if not self.analysis_result:
            return

        search_term = (
            self.symbol_filter_entry
            .get()
            .strip()
            .lower()
        )

        for file_analysis in (
            self.analysis_result.files
        ):
            for symbol in (
                file_analysis.symbols
            ):
                searchable_text = (
                    f"{file_analysis.module_name} "
                    f"{symbol.name} "
                    f"{symbol.symbol_type} "
                    f"{symbol.parent}"
                ).lower()

                if (
                    search_term
                    and search_term
                    not in searchable_text
                ):
                    continue

                self.symbols_table.insert(
                    [
                        file_analysis.module_name,
                        symbol.name,
                        self.tr(
                            symbol.symbol_type
                        ),
                        symbol.parent or "—",
                        symbol.line,
                        symbol.complexity,
                        (
                            self.tr("yes")
                            if symbol.has_docstring
                            else self.tr("no")
                        ),
                    ]
                )

    def _render_dependencies(self) -> None:
        self.dependencies_table.clear()

        if not self.analysis_result:
            return

        dependency_data: defaultdict[
            str,
            dict[str, Any],
        ] = defaultdict(
            lambda: {
                "count": 0,
                "files": set(),
                "categories": Counter(),
            }
        )

        for file_analysis in (
            self.analysis_result.files
        ):
            for import_information in (
                file_analysis.imports
            ):
                module = (
                    import_information.module
                )

                dependency_data[
                    module
                ]["count"] += 1

                dependency_data[
                    module
                ]["files"].add(
                    file_analysis.relative_path
                )

                dependency_data[
                    module
                ]["categories"][
                    import_information.category
                ] += 1

        sorted_dependencies = sorted(
            dependency_data.items(),
            key=lambda item: (
                -item[1]["count"],
                item[0].lower(),
            ),
        )

        for module, details in (
            sorted_dependencies
        ):
            category = (
                details["categories"]
                .most_common(1)[0][0]
            )

            files = sorted(
                details["files"]
            )

            visible_files = ", ".join(
                files[:6]
            )

            if len(files) > 6:
                visible_files += (
                    f" (+{len(files) - 6})"
                )

            self.dependencies_table.insert(
                [
                    module,
                    self.tr(category),
                    details["count"],
                    visible_files,
                ]
            )

    def _render_findings(self) -> None:
        self.findings_table.clear()

        if not self.analysis_result:
            return

        search_term = (
            self.finding_filter_entry
            .get()
            .strip()
            .lower()
        )

        for finding in (
            self.analysis_result.findings
        ):
            location = finding.file

            if finding.line:
                location += (
                    f":{finding.line}"
                )

            description = self.tr(
                finding.message_key
            )

            if finding.details:
                description += (
                    f" — {finding.details}"
                )

            recommendation = self.tr(
                finding.recommendation_key
            )

            searchable_text = (
                f"{finding.severity} "
                f"{location} "
                f"{finding.category} "
                f"{description} "
                f"{recommendation}"
            ).lower()

            if (
                search_term
                and search_term
                not in searchable_text
            ):
                continue

            self.findings_table.insert(
                [
                    self.tr(
                        finding.severity
                    ),
                    location,
                    finding.category,
                    description,
                    recommendation,
                ],
                tags=(
                    finding.severity,
                ),
            )

    def _render_report(self) -> None:
        if not self.analysis_result:
            self._set_textbox_content(
                self.report_text,
                self.tr("analysis_hint"),
            )

            return

        self._set_textbox_content(
            self.report_text,
            self._build_markdown_report(),
        )

    def _file_status(
        self,
        file_analysis: FileAnalysis,
    ) -> str:
        if file_analysis.skipped_reason:
            return self.tr(
                file_analysis.skipped_reason
            )

        if file_analysis.syntax_error:
            return self.tr(
                "syntax_error"
            )

        if (
            file_analysis.complexity >= 45
            or file_analysis.maximum_nesting >= 7
        ):
            return self.tr("high_risk")

        if (
            file_analysis.complexity
            >= HIGH_FILE_COMPLEXITY_LIMIT
            or file_analysis.total_lines
            >= LARGE_FILE_LINE_LIMIT
        ):
            return self.tr("attention")

        if (
            not file_analysis.module_has_docstring
        ):
            return self.tr("review")

        return self.tr("clean")

    @staticmethod
    def _set_textbox_content(
        textbox: ctk.CTkTextbox,
        content: str,
    ) -> None:
        textbox.configure(
            state="normal"
        )

        textbox.delete(
            "1.0",
            "end",
        )

        textbox.insert(
            "1.0",
            content,
        )

        textbox.configure(
            state="disabled"
        )

    def _analysis_as_dictionary(
        self,
    ) -> dict[str, Any]:
        if not self.analysis_result:
            return {}

        result = asdict(
            self.analysis_result
        )

        result["totals"] = (
            self.analysis_result.totals()
        )

        result["application"] = {
            "title": APP_TITLE,
            "name": APP_NAME,
            "author": APP_AUTHOR,
            "version": APP_VERSION,
            "license": APP_LICENSE,
            "github": APP_GITHUB_URL,
        }

        return result

    def _build_markdown_report(
        self,
    ) -> str:
        if not self.analysis_result:
            return self.tr(
                "analysis_hint"
            )

        totals = (
            self.analysis_result.totals()
        )

        dependency_counter = Counter(
            import_information.module
            for file_analysis
            in self.analysis_result.files
            for import_information
            in file_analysis.imports
        )

        complex_files = sorted(
            [
                file_analysis
                for file_analysis
                in self.analysis_result.files
                if not file_analysis.skipped_reason
            ],
            key=lambda file_analysis:
            file_analysis.complexity,
            reverse=True,
        )[:15]

        report_lines = [
            f"# {self.tr('report_title')}",
            "",
            (
                f"- **{self.tr('project_path')}:** "
                f"`{self.analysis_result.project_path}`"
            ),
            (
                f"- **{self.tr('generated_at')}:** "
                f"{self.analysis_result.generated_at}"
            ),
            (
                f"- **{APP_NAME}:** "
                f"{APP_VERSION}"
            ),
            "",
            f"## {self.tr('overview')}",
            "",
            (
                f"| {self.tr('description')} | "
                f"{self.tr('count')} |"
            ),
            "|---|---:|",
            (
                f"| {self.tr('files_scanned')} | "
                f"{totals['files']} |"
            ),
            (
                f"| {self.tr('code_lines')} | "
                f"{totals['code_lines']} |"
            ),
            (
                f"| {self.tr('total_lines')} | "
                f"{totals['total_lines']} |"
            ),
            (
                f"| {self.tr('classes')} | "
                f"{totals['classes']} |"
            ),
            (
                f"| {self.tr('functions')} | "
                f"{totals['functions']} |"
            ),
            (
                f"| {self.tr('imports')} | "
                f"{totals['imports']} |"
            ),
            (
                f"| {self.tr('findings_count')} | "
                f"{totals['findings']} |"
            ),
            (
                f"| {self.tr('documentation')} | "
                f"{totals['documentation_percentage']} % |"
            ),
            (
                f"| {self.tr('quality_score')} | "
                f"{totals['quality_score']} / 100 |"
            ),
            "",
            f"## {self.tr('top_dependencies')}",
            "",
        ]

        if dependency_counter:
            for module, count in (
                dependency_counter.most_common(20)
            ):
                report_lines.append(
                    f"- `{module}`: {count}"
                )
        else:
            report_lines.append(
                f"- {self.tr('no_data')}"
            )

        report_lines.extend(
            [
                "",
                f"## {self.tr('complex_files')}",
                "",
            ]
        )

        if complex_files:
            for file_analysis in (
                complex_files
            ):
                report_lines.append(
                    f"- `{file_analysis.relative_path}` — "
                    f"{self.tr('complexity')}: "
                    f"{file_analysis.complexity}"
                )
        else:
            report_lines.append(
                f"- {self.tr('no_data')}"
            )

        report_lines.extend(
            [
                "",
                f"## {self.tr('file_analysis')}",
                "",
                (
                    f"| {self.tr('file')} | "
                    f"{self.tr('lines')} | "
                    f"{self.tr('classes')} | "
                    f"{self.tr('functions')} | "
                    f"{self.tr('imports')} | "
                    f"{self.tr('complexity')} |"
                ),
                "|---|---:|---:|---:|---:|---:|",
            ]
        )

        for file_analysis in (
            self.analysis_result.files
        ):
            report_lines.append(
                f"| `{file_analysis.relative_path}` | "
                f"{file_analysis.code_lines} | "
                f"{file_analysis.class_count} | "
                f"{file_analysis.function_count} | "
                f"{len(file_analysis.imports)} | "
                f"{file_analysis.complexity} |"
            )

        report_lines.extend(
            [
                "",
                f"## {self.tr('quality_findings')}",
                "",
            ]
        )

        if not self.analysis_result.findings:
            report_lines.append(
                self.tr("no_findings")
            )
        else:
            for finding in (
                self.analysis_result.findings
            ):
                location = finding.file

                if finding.line:
                    location += (
                        f":{finding.line}"
                    )

                details = (
                    f" — {finding.details}"
                    if finding.details
                    else ""
                )

                report_lines.extend(
                    [
                        (
                            f"### "
                            f"{self.tr(finding.severity)} "
                            f"· `{location}`"
                        ),
                        "",
                        (
                            f"**{self.tr('description')}:** "
                            f"{self.tr(finding.message_key)}"
                            f"{details}"
                        ),
                        "",
                        (
                            f"**{self.tr('recommendation')}:** "
                            f"{self.tr(finding.recommendation_key)}"
                        ),
                        "",
                    ]
                )

        report_lines.extend(
            [
                "---",
                "",
                (
                    f"{self.tr('generated_by')} "
                    f"{APP_NAME} {APP_VERSION} "
                    f"· {APP_AUTHOR}"
                ),
            ]
        )

        return "\n".join(
            report_lines
        )

    def _export_json(self) -> None:
        if not self.analysis_result:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "select_project_first"
                ),
            )

            return

        project_name = Path(
            self.analysis_result.project_path
        ).name

        destination = (
            filedialog.asksaveasfilename(
                title=self.tr("export_json"),
                defaultextension=".json",
                initialfile=(
                    f"{project_name}_"
                    f"codebase_report.json"
                ),
                filetypes=[
                    (
                        "JSON",
                        "*.json",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if not destination:
            return

        try:
            Path(destination).write_text(
                json.dumps(
                    self._analysis_as_dictionary(),
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            messagebox.showinfo(
                APP_NAME,
                self.tr("export_success"),
            )

        except OSError as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('export_failed')}"
                    f"\n\n{error}"
                ),
            )

    def _export_markdown(self) -> None:
        if not self.analysis_result:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "select_project_first"
                ),
            )

            return

        project_name = Path(
            self.analysis_result.project_path
        ).name

        destination = (
            filedialog.asksaveasfilename(
                title=self.tr(
                    "export_markdown"
                ),
                defaultextension=".md",
                initialfile=(
                    f"{project_name}_"
                    f"codebase_report.md"
                ),
                filetypes=[
                    (
                        "Markdown",
                        "*.md",
                    ),
                    (
                        "Text",
                        "*.txt",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if not destination:
            return

        try:
            Path(destination).write_text(
                self._build_markdown_report(),
                encoding="utf-8",
            )

            messagebox.showinfo(
                APP_NAME,
                self.tr("export_success"),
            )

        except OSError as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('export_failed')}"
                    f"\n\n{error}"
                ),
            )

    def _open_github(self) -> None:
        webbrowser.open(
            APP_GITHUB_URL
        )

    def _open_project_folder(self) -> None:
        if not self.project_path:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "select_project_first"
                ),
            )

            return

        try:
            open_folder_in_file_manager(
                self.project_path
            )

        except (
            OSError,
            subprocess.SubprocessError,
        ) as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('folder_open_failed')}"
                    f"\n\n{error}"
                ),
            )


    def _show_about_dialog(self) -> None:
        description = (
            APP_DESCRIPTION_DE
            if self.language == "de"
            else APP_DESCRIPTION_EN
        )

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            self.tr("about_title")
        )

        dialog.geometry(
            "680x520"
        )

        dialog.minsize(
            600,
            460,
        )

        dialog.transient(self)
        dialog.grab_set()

        dialog.grid_columnconfigure(
            0,
            weight=1,
        )

        dialog.grid_rowconfigure(
            1,
            weight=1,
        )

        title_label = ctk.CTkLabel(
            dialog,
            text=APP_NAME,
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
            anchor="w",
        )

        title_label.grid(
            row=0,
            column=0,
            padx=26,
            pady=(26, 10),
            sticky="ew",
        )

        information_text = (
            f"{description}\n\n"
            f"Version: {APP_VERSION}\n"
            f"{'Autor' if self.language == 'de' else 'Author'}: "
            f"{APP_AUTHOR}\n"
            f"{'Lizenz' if self.language == 'de' else 'License'}: "
            f"{APP_LICENSE}\n"
            f"Python: {platform.python_version()}\n"
            f"{'System' if self.language == 'de' else 'System'}: "
            f"{platform.system()} {platform.release()}\n\n"
            f"{self.tr('privacy')}\n\n"
            f"GitHub:\n{APP_GITHUB_URL}"
        )

        text_widget = ctk.CTkTextbox(
            dialog,
            corner_radius=14,
            wrap="word",
            font=ctk.CTkFont(
                size=14,
            ),
        )

        text_widget.grid(
            row=1,
            column=0,
            padx=26,
            pady=10,
            sticky="nsew",
        )

        text_widget.insert(
            "1.0",
            information_text,
        )

        text_widget.configure(
            state="disabled"
        )

        action_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent",
        )

        action_frame.grid(
            row=2,
            column=0,
            padx=26,
            pady=(8, 26),
            sticky="ew",
        )

        github_button = ctk.CTkButton(
            action_frame,
            text=self.tr("github"),
            command=self._open_github,
        )

        github_button.pack(
            side="left"
        )

        close_button = ctk.CTkButton(
            action_frame,
            text="OK",
            fg_color="transparent",
            border_width=1,
            command=dialog.destroy,
        )

        close_button.pack(
            side="right"
        )



import hashlib
import shutil
import sqlite3
import tempfile

from tkinter import simpledialog

try:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError as error:
    raise SystemExit(
        "\nDie Erweiterung 'cryptography' wurde nicht gefunden.\n"
        "The 'cryptography' extension was not found.\n\n"
        "Installation:\n"
        "    pip install customtkinter cryptography\n"
    ) from error


MAX_CUSTOM_MESSAGE_LENGTH = 1000
DATABASE_EXPORT_MAGIC = b"CODEBASE_CARTOGRAPHER_DB_V3\x00"
DATABASE_KEY_ITERATIONS = 390_000

APPLICATION_DATA_DIRECTORY = (
    Path.home()
    / ".codebase_cartographer"
)

APPLICATION_DATABASE_PATH = (
    APPLICATION_DATA_DIRECTORY
    / "codebase_cartographer.sqlite3"
)


TRANSLATIONS["de"].update(
    {
        "database": "Datenbank",
        "database_archive": "SQLite-Projektarchiv",
        "database_archive_hint": (
            "Jede abgeschlossene Analyse wird automatisch mit allen "
            "Dateiinformationen, Symbolen, Importen, Befunden und der "
            "benutzerdefinierten Meldung in SQLite gespeichert."
        ),
        "custom_message": "Benutzerdefinierte Meldung",
        "custom_message_placeholder": (
            "Meldung zum Projekt oder zur Analyse eingeben …"
        ),
        "custom_message_counter": "{count}/1000 Zeichen",
        "save_custom_message": "Meldung speichern",
        "custom_message_saved": "Die Meldung wurde gespeichert.",
        "custom_message_too_long": (
            "Die Meldung darf maximal 1000 Zeichen enthalten."
        ),
        "custom_message_requires_scan": (
            "Die Meldung kann gespeichert werden, sobald eine Analyse "
            "erstellt oder ein archivierter Scan geladen wurde."
        ),
        "editor": "Integrierter Editor",
        "open_in_editor": "Im Editor öffnen",
        "editor_double_click_hint": (
            "Doppelklick auf eine Datei öffnet sie im integrierten Editor."
        ),
        "editor_save": "Speichern",
        "editor_save_as": "Speichern unter",
        "editor_reload": "Neu laden",
        "editor_find": "Suchen",
        "editor_replace": "Ersetzen",
        "editor_go_to_line": "Gehe zu Zeile",
        "editor_select_all": "Alles auswählen",
        "editor_undo": "Rückgängig",
        "editor_redo": "Wiederholen",
        "editor_file_saved": "Die Datei wurde gespeichert.",
        "editor_save_failed": "Die Datei konnte nicht gespeichert werden.",
        "editor_confirm_overwrite": (
            "Die Datei im Projektverzeichnis wirklich überschreiben?"
        ),
        "editor_unsaved_title": "Ungespeicherte Änderungen",
        "editor_unsaved_question": (
            "Sollen die Änderungen vor dem Schließen gespeichert werden?"
        ),
        "editor_reload_question": (
            "Die Datei neu laden und ungespeicherte Änderungen verwerfen?"
        ),
        "editor_file_changed_externally": (
            "Die Datei wurde außerhalb des Editors verändert. "
            "Trotzdem überschreiben?"
        ),
        "editor_search_term": "Suchbegriff",
        "editor_replacement": "Ersetzung",
        "editor_line_number": "Zeilennummer",
        "editor_matches": "{count} Treffer",
        "editor_no_match": "Kein Treffer",
        "editor_read_error": "Die Datei konnte nicht gelesen werden.",
        "editor_invalid_file": "Die ausgewählte Datei ist nicht verfügbar.",
        "editor_status": "Zeile {line}, Spalte {column} · UTF-8 · {characters} Zeichen",
        "scan_id": "Scan-ID",
        "archive_project": "Projekt",
        "archive_date": "Zeitpunkt",
        "archive_files": "Dateien",
        "archive_findings": "Befunde",
        "archive_message": "Meldung",
        "archive_load": "Scan laden",
        "archive_delete": "Scan löschen",
        "archive_refresh": "Aktualisieren",
        "archive_export_scan_json": "Scan als JSON",
        "archive_export_scan_markdown": "Scan als Markdown",
        "archive_export_database": "Datenbank exportieren",
        "archive_import_database": "Datenbank importieren",
        "archive_no_selection": (
            "Bitte zuerst einen archivierten Scan auswählen."
        ),
        "archive_loaded": "Der archivierte Scan wurde geladen.",
        "archive_delete_question": (
            "Den ausgewählten Scan wirklich dauerhaft löschen?"
        ),
        "archive_deleted": "Der archivierte Scan wurde gelöscht.",
        "database_password": "Datenbankpasswort",
        "database_password_repeat": "Passwort wiederholen",
        "database_password_required": "Ein Passwort ist erforderlich.",
        "database_password_mismatch": (
            "Die eingegebenen Passwörter stimmen nicht überein."
        ),
        "database_export_title": (
            "Passwortgeschützte Datenbank exportieren"
        ),
        "database_import_title": (
            "Passwortgeschützte Datenbank importieren"
        ),
        "database_exported": (
            "Die Datenbank wurde als passwortgeschütztes Paket exportiert."
        ),
        "database_imported": (
            "Die Datenbank wurde erfolgreich importiert."
        ),
        "database_import_warning": (
            "Beim Import wird die aktuelle lokale Datenbank ersetzt. "
            "Vorher wird automatisch eine Sicherungskopie angelegt. "
            "Möchtest du fortfahren?"
        ),
        "database_wrong_password": (
            "Das Passwort ist falsch oder das Datenbankpaket ist beschädigt."
        ),
        "database_export_failed": (
            "Die Datenbank konnte nicht exportiert werden."
        ),
        "database_import_failed": (
            "Die Datenbank konnte nicht importiert werden."
        ),
        "database_path": "Lokale Datenbank",
        "database_encryption": (
            "Geschützte Exporte verwenden AES-256-GCM und eine "
            "PBKDF2-Schlüsselableitung."
        ),
        "automatic_archive_saved": (
            "Die Analyse wurde automatisch im SQLite-Archiv gespeichert."
        ),
        "rescan_after_editor_save": (
            "Die bearbeitete Datei wurde gespeichert. Starte die Analyse "
            "erneut, um alle Kennzahlen zu aktualisieren."
        ),
    }
)

TRANSLATIONS["en"].update(
    {
        "database": "Database",
        "database_archive": "SQLite project archive",
        "database_archive_hint": (
            "Every completed analysis is automatically stored in SQLite "
            "with all file information, symbols, imports, findings, and "
            "the custom message."
        ),
        "custom_message": "Custom message",
        "custom_message_placeholder": (
            "Enter a message for the project or analysis …"
        ),
        "custom_message_counter": "{count}/1000 characters",
        "save_custom_message": "Save message",
        "custom_message_saved": "The message was saved.",
        "custom_message_too_long": (
            "The message may contain no more than 1000 characters."
        ),
        "custom_message_requires_scan": (
            "The message can be saved after an analysis has been created "
            "or an archived scan has been loaded."
        ),
        "editor": "Integrated editor",
        "open_in_editor": "Open in editor",
        "editor_double_click_hint": (
            "Double-click a file to open it in the integrated editor."
        ),
        "editor_save": "Save",
        "editor_save_as": "Save as",
        "editor_reload": "Reload",
        "editor_find": "Find",
        "editor_replace": "Replace",
        "editor_go_to_line": "Go to line",
        "editor_select_all": "Select all",
        "editor_undo": "Undo",
        "editor_redo": "Redo",
        "editor_file_saved": "The file was saved.",
        "editor_save_failed": "The file could not be saved.",
        "editor_confirm_overwrite": (
            "Really overwrite the file in the project directory?"
        ),
        "editor_unsaved_title": "Unsaved changes",
        "editor_unsaved_question": (
            "Save the changes before closing?"
        ),
        "editor_reload_question": (
            "Reload the file and discard unsaved changes?"
        ),
        "editor_file_changed_externally": (
            "The file was changed outside the editor. "
            "Overwrite it anyway?"
        ),
        "editor_search_term": "Search term",
        "editor_replacement": "Replacement",
        "editor_line_number": "Line number",
        "editor_matches": "{count} matches",
        "editor_no_match": "No match",
        "editor_read_error": "The file could not be read.",
        "editor_invalid_file": "The selected file is unavailable.",
        "editor_status": "Line {line}, column {column} · UTF-8 · {characters} characters",
        "scan_id": "Scan ID",
        "archive_project": "Project",
        "archive_date": "Date",
        "archive_files": "Files",
        "archive_findings": "Findings",
        "archive_message": "Message",
        "archive_load": "Load scan",
        "archive_delete": "Delete scan",
        "archive_refresh": "Refresh",
        "archive_export_scan_json": "Scan as JSON",
        "archive_export_scan_markdown": "Scan as Markdown",
        "archive_export_database": "Export database",
        "archive_import_database": "Import database",
        "archive_no_selection": (
            "Please select an archived scan first."
        ),
        "archive_loaded": "The archived scan was loaded.",
        "archive_delete_question": (
            "Permanently delete the selected scan?"
        ),
        "archive_deleted": "The archived scan was deleted.",
        "database_password": "Database password",
        "database_password_repeat": "Repeat password",
        "database_password_required": "A password is required.",
        "database_password_mismatch": (
            "The entered passwords do not match."
        ),
        "database_export_title": (
            "Export password-protected database"
        ),
        "database_import_title": (
            "Import password-protected database"
        ),
        "database_exported": (
            "The database was exported as a password-protected package."
        ),
        "database_imported": (
            "The database was imported successfully."
        ),
        "database_import_warning": (
            "Importing replaces the current local database. "
            "A backup copy will be created automatically first. "
            "Do you want to continue?"
        ),
        "database_wrong_password": (
            "The password is wrong or the database package is damaged."
        ),
        "database_export_failed": (
            "The database could not be exported."
        ),
        "database_import_failed": (
            "The database could not be imported."
        ),
        "database_path": "Local database",
        "database_encryption": (
            "Protected exports use AES-256-GCM and PBKDF2 key derivation."
        ),
        "automatic_archive_saved": (
            "The analysis was automatically saved in the SQLite archive."
        ),
        "rescan_after_editor_save": (
            "The edited file was saved. Run the analysis again to update "
            "all metrics."
        ),
    }
)


def serialize_project_analysis(
    analysis: ProjectAnalysis,
) -> dict[str, Any]:
    """
    Neuerung
    """

    return {
        "project_path": analysis.project_path,
        "generated_at": analysis.generated_at,
        "ignored_files": analysis.ignored_files,
        "excluded_directories": list(
            analysis.excluded_directories
        ),
        "totals": analysis.totals(),
        "files": [
            asdict(file_analysis)
            for file_analysis in analysis.files
        ],
        "findings": [
            asdict(finding)
            for finding in analysis.findings
        ],
    }


def deserialize_project_analysis(
    payload: dict[str, Any],
) -> ProjectAnalysis:
    """
    Neuerung
    """

    files: list[FileAnalysis] = []

    for file_payload in payload.get(
        "files",
        [],
    ):
        symbols = [
            SymbolInformation(**symbol_payload)
            for symbol_payload in file_payload.get(
                "symbols",
                [],
            )
        ]

        imports = [
            ImportInformation(**import_payload)
            for import_payload in file_payload.get(
                "imports",
                [],
            )
        ]

        file_copy = dict(file_payload)
        file_copy["symbols"] = symbols
        file_copy["imports"] = imports

        files.append(
            FileAnalysis(**file_copy)
        )

    findings = [
        Finding(**finding_payload)
        for finding_payload in payload.get(
            "findings",
            [],
        )
    ]

    return ProjectAnalysis(
        project_path=payload.get(
            "project_path",
            "",
        ),
        generated_at=payload.get(
            "generated_at",
            "",
        ),
        files=files,
        findings=findings,
        ignored_files=int(
            payload.get(
                "ignored_files",
                0,
            )
        ),
        excluded_directories=list(
            payload.get(
                "excluded_directories",
                [],
            )
        ),
    )


class CodebaseDatabaseManager:
    """
    Aktualisiert
    """

    def __init__(
        self,
        database_path: Path,
    ) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.initialize_database()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        connection.execute(
            "PRAGMA journal_mode = WAL"
        )

        connection.execute(
            "PRAGMA synchronous = NORMAL"
        )

        return connection

    def initialize_database(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS project_scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_path TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    custom_message TEXT NOT NULL DEFAULT '',
                    file_count INTEGER NOT NULL DEFAULT 0,
                    finding_count INTEGER NOT NULL DEFAULT 0,
                    quality_score INTEGER NOT NULL DEFAULT 0,
                    payload_json TEXT NOT NULL,
                    application_version TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS
                    idx_project_scans_project_path
                    ON project_scans(project_path);

                CREATE INDEX IF NOT EXISTS
                    idx_project_scans_generated_at
                    ON project_scans(generated_at);
                """
            )

    def save_analysis(
        self,
        analysis: ProjectAnalysis,
        custom_message: str,
    ) -> int:
        payload = serialize_project_analysis(
            analysis
        )

        totals = analysis.totals()

        payload_json = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO project_scans (
                    project_path,
                    generated_at,
                    custom_message,
                    file_count,
                    finding_count,
                    quality_score,
                    payload_json,
                    application_version
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    analysis.project_path,
                    analysis.generated_at,
                    custom_message[
                        :MAX_CUSTOM_MESSAGE_LENGTH
                    ],
                    int(totals.get("files", 0)),
                    int(totals.get("findings", 0)),
                    int(totals.get("quality_score", 0)),
                    payload_json,
                    APP_VERSION,
                ),
            )

            scan_id = cursor.lastrowid

        if scan_id is None:
            raise RuntimeError(
                "SQLite did not return a scan identifier."
            )

        return int(scan_id)

    def update_custom_message(
        self,
        scan_id: int,
        custom_message: str,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE project_scans
                SET custom_message = ?
                WHERE id = ?
                """,
                (
                    custom_message[
                        :MAX_CUSTOM_MESSAGE_LENGTH
                    ],
                    scan_id,
                ),
            )

    def list_scans(
        self,
    ) -> list[sqlite3.Row]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    project_path,
                    generated_at,
                    custom_message,
                    file_count,
                    finding_count,
                    quality_score,
                    application_version
                FROM project_scans
                ORDER BY id DESC
                """
            ).fetchall()

        return list(rows)

    def load_scan(
        self,
        scan_id: int,
    ) -> tuple[ProjectAnalysis, str]:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    payload_json,
                    custom_message
                FROM project_scans
                WHERE id = ?
                """,
                (scan_id,),
            ).fetchone()

        if row is None:
            raise LookupError(
                f"Scan {scan_id} was not found."
            )

        payload = json.loads(
            row["payload_json"]
        )

        analysis = deserialize_project_analysis(
            payload
        )

        return (
            analysis,
            str(row["custom_message"]),
        )

    def export_scan_payload(
        self,
        scan_id: int,
    ) -> dict[str, Any]:
        analysis, custom_message = self.load_scan(
            scan_id
        )

        return {
            "scan_id": scan_id,
            "custom_message": custom_message,
            "analysis": serialize_project_analysis(
                analysis
            ),
            "application": {
                "title": APP_TITLE,
                "name": APP_NAME,
                "author": APP_AUTHOR,
                "version": APP_VERSION,
                "github": APP_GITHUB_URL,
            },
        }

    def delete_scan(
        self,
        scan_id: int,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                DELETE FROM project_scans
                WHERE id = ?
                """,
                (scan_id,),
            )

    def checkpoint(self) -> None:
        with self.connect() as connection:
            connection.execute(
                "PRAGMA wal_checkpoint(FULL)"
            )

    def integrity_check(self) -> bool:
        with self.connect() as connection:
            row = connection.execute(
                "PRAGMA integrity_check"
            ).fetchone()

        return bool(
            row
            and row[0] == "ok"
        )


def derive_database_encryption_key(
    password: str,
    salt: bytes,
) -> bytes:
    key_derivation = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=DATABASE_KEY_ITERATIONS,
    )

    return key_derivation.derive(
        password.encode("utf-8")
    )


def export_password_protected_database(
    database_manager: CodebaseDatabaseManager,
    destination: Path,
    password: str,
) -> None:
    """
    Implementiert
    """

    database_manager.checkpoint()

    database_bytes = (
        database_manager.database_path
        .read_bytes()
    )

    salt = os.urandom(16)
    nonce = os.urandom(12)

    encryption_key = (
        derive_database_encryption_key(
            password,
            salt,
        )
    )

    encrypted_bytes = AESGCM(
        encryption_key
    ).encrypt(
        nonce,
        database_bytes,
        DATABASE_EXPORT_MAGIC,
    )

    destination.write_bytes(
        DATABASE_EXPORT_MAGIC
        + salt
        + nonce
        + encrypted_bytes
    )


def import_password_protected_database(
    source: Path,
    destination: Path,
    password: str,
) -> None:
    """
    Aktualisiert
    """

    package = source.read_bytes()

    header_length = len(
        DATABASE_EXPORT_MAGIC
    )

    minimum_length = (
        header_length
        + 16
        + 12
        + 16
    )

    if (
        len(package) < minimum_length
        or not package.startswith(
            DATABASE_EXPORT_MAGIC
        )
    ):
        raise ValueError(
            "Invalid Codebase Cartographer database package."
        )

    salt_start = header_length
    salt_end = salt_start + 16
    nonce_end = salt_end + 12

    salt = package[
        salt_start:salt_end
    ]

    nonce = package[
        salt_end:nonce_end
    ]

    encrypted_bytes = package[
        nonce_end:
    ]

    encryption_key = (
        derive_database_encryption_key(
            password,
            salt,
        )
    )

    database_bytes = AESGCM(
        encryption_key
    ).decrypt(
        nonce,
        encrypted_bytes,
        DATABASE_EXPORT_MAGIC,
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_file = tempfile.NamedTemporaryFile(
        mode="wb",
        delete=False,
        dir=destination.parent,
        suffix=".sqlite3",
    )

    temporary_path = Path(
        temporary_file.name
    )

    try:
        with temporary_file:
            temporary_file.write(
                database_bytes
            )

        with sqlite3.connect(
            temporary_path
        ) as connection:
            row = connection.execute(
                "PRAGMA integrity_check"
            ).fetchone()

            if (
                row is None
                or row[0] != "ok"
            ):
                raise ValueError(
                    "Imported database failed its integrity check."
                )

        shutil.move(
            str(temporary_path),
            str(destination),
        )

    finally:
        temporary_path.unlink(
            missing_ok=True
        )


class DatabasePasswordDialog(
    ctk.CTkToplevel
):
    """
    Aktualisiert
    """

    def __init__(
        self,
        master: Any,
        title_text: str,
        require_confirmation: bool,
    ) -> None:
        super().__init__(
            master
        )

        self.master_application = master
        self.require_confirmation = (
            require_confirmation
        )
        self.result: str | None = None

        self.title(
            title_text
        )

        self.geometry(
            "460x285"
            if require_confirmation
            else "460x225"
        )

        self.resizable(
            False,
            False,
        )

        self.transient(
            master
        )

        self.grab_set()

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        title_label = ctk.CTkLabel(
            self,
            text=title_text,
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
            anchor="w",
        )

        title_label.grid(
            row=0,
            column=0,
            padx=26,
            pady=(26, 14),
            sticky="ew",
        )

        self.password_entry = (
            ctk.CTkEntry(
                self,
                show="•",
                placeholder_text=(
                    master.tr(
                        "database_password"
                    )
                ),
            )
        )

        self.password_entry.grid(
            row=1,
            column=0,
            padx=26,
            pady=6,
            sticky="ew",
        )

        self.confirmation_entry: (
            ctk.CTkEntry | None
        ) = None

        if require_confirmation:
            self.confirmation_entry = (
                ctk.CTkEntry(
                    self,
                    show="•",
                    placeholder_text=(
                        master.tr(
                            "database_password_repeat"
                        )
                    ),
                )
            )

            self.confirmation_entry.grid(
                row=2,
                column=0,
                padx=26,
                pady=6,
                sticky="ew",
            )

        actions = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        actions.grid(
            row=3,
            column=0,
            padx=26,
            pady=22,
            sticky="ew",
        )

        cancel_button = ctk.CTkButton(
            actions,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            command=self.destroy,
        )

        cancel_button.pack(
            side="right",
            padx=(8, 0),
        )

        accept_button = ctk.CTkButton(
            actions,
            text="OK",
            command=self._accept,
        )

        accept_button.pack(
            side="right",
        )

        self.password_entry.focus_set()

        self.bind(
            "<Return>",
            lambda _event:
            self._accept(),
        )

        self.bind(
            "<Escape>",
            lambda _event:
            self.destroy(),
        )

    def _accept(self) -> None:
        password = (
            self.password_entry
            .get()
        )

        if not password:
            messagebox.showwarning(
                APP_NAME,
                self.master_application.tr(
                    "database_password_required"
                ),
                parent=self,
            )

            return

        if (
            self.confirmation_entry
            is not None
            and password
            != self.confirmation_entry.get()
        ):
            messagebox.showwarning(
                APP_NAME,
                self.master_application.tr(
                    "database_password_mismatch"
                ),
                parent=self,
            )

            return

        self.result = password
        self.destroy()

    def show(
        self,
    ) -> str | None:
        self.wait_window()
        return self.result


class SourceCodeEditorWindow(
    ctk.CTkToplevel
):
    """
    Aktualisiert
    """

    def __init__(
        self,
        master: Any,
        file_path: Path,
    ) -> None:
        super().__init__(
            master
        )

        self.master_application = master
        self.file_path = file_path

        self.original_content = ""
        self.original_digest = ""
        self.modified = False

        self.title(
            f"{master.tr('editor')} — "
            f"{file_path.name}"
        )

        self.geometry(
            "1280x820"
        )

        self.minsize(
            860,
            560,
        )

        self.transient(
            master
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self._request_close,
        )

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            2,
            weight=1,
        )

        self._build_menu_bar()
        self._build_toolbar()
        self._build_editor_area()
        self._build_status_bar()

        self._load_file()

    def _build_menu_bar(self) -> None:
        menu_bar = ctk.CTkFrame(
            self,
            corner_radius=0,
        )

        menu_bar.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        self.save_button = ctk.CTkButton(
            menu_bar,
            text=self.master_application.tr(
                "editor_save"
            ),
            width=105,
            command=self._save,
        )

        self.save_button.pack(
            side="left",
            padx=(12, 5),
            pady=10,
        )

        self.save_as_button = ctk.CTkButton(
            menu_bar,
            text=self.master_application.tr(
                "editor_save_as"
            ),
            width=120,
            fg_color="transparent",
            border_width=1,
            command=self._save_as,
        )

        self.save_as_button.pack(
            side="left",
            padx=5,
            pady=10,
        )

        self.reload_button = ctk.CTkButton(
            menu_bar,
            text=self.master_application.tr(
                "editor_reload"
            ),
            width=105,
            fg_color="transparent",
            border_width=1,
            command=self._reload,
        )

        self.reload_button.pack(
            side="left",
            padx=5,
            pady=10,
        )

        self.path_label = ctk.CTkLabel(
            menu_bar,
            text=str(
                self.file_path
            ),
            anchor="e",
        )

        self.path_label.pack(
            side="right",
            padx=14,
            pady=10,
        )

    def _build_toolbar(self) -> None:
        toolbar = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent",
        )

        toolbar.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        actions = [
            (
                "editor_undo",
                self._undo,
            ),
            (
                "editor_redo",
                self._redo,
            ),
            (
                "editor_find",
                self._find,
            ),
            (
                "editor_replace",
                self._replace,
            ),
            (
                "editor_go_to_line",
                self._go_to_line,
            ),
            (
                "editor_select_all",
                self._select_all,
            ),
        ]

        for translation_key, command in actions:
            button = ctk.CTkButton(
                toolbar,
                text=self.master_application.tr(
                    translation_key
                ),
                width=110,
                height=34,
                fg_color="transparent",
                border_width=1,
                command=command,
            )

            button.pack(
                side="left",
                padx=5,
                pady=(4, 8),
            )

    def _build_editor_area(self) -> None:
        editor_container = ctk.CTkFrame(
            self,
            corner_radius=0,
        )

        editor_container.grid(
            row=2,
            column=0,
            sticky="nsew",
        )

        editor_container.grid_columnconfigure(
            1,
            weight=1,
        )

        editor_container.grid_rowconfigure(
            0,
            weight=1,
        )

        self.line_number_textbox = (
            ctk.CTkTextbox(
                editor_container,
                width=72,
                corner_radius=0,
                wrap="none",
                font=ctk.CTkFont(
                    family="Consolas",
                    size=13,
                ),
            )
        )

        self.line_number_textbox.grid(
            row=0,
            column=0,
            sticky="ns",
        )

        self.line_number_textbox.configure(
            state="disabled"
        )

        self.editor_textbox = (
            ctk.CTkTextbox(
                editor_container,
                corner_radius=0,
                wrap="none",
                undo=True,
                maxundo=-1,
                font=ctk.CTkFont(
                    family="Consolas",
                    size=13,
                ),
            )
        )

        self.editor_textbox.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.editor_textbox.bind(
            "<<Modified>>",
            self._on_modified,
        )

        self.editor_textbox.bind(
            "<KeyRelease>",
            self._on_cursor_event,
        )

        self.editor_textbox.bind(
            "<ButtonRelease-1>",
            self._on_cursor_event,
        )

        self.editor_textbox.bind(
            "<Control-s>",
            lambda _event:
            self._save(),
        )

        self.editor_textbox.bind(
            "<Control-Shift-S>",
            lambda _event:
            self._save_as(),
        )

        self.editor_textbox.bind(
            "<Control-f>",
            lambda _event:
            self._find(),
        )

        self.editor_textbox.bind(
            "<Control-h>",
            lambda _event:
            self._replace(),
        )

        self.editor_textbox.bind(
            "<Control-g>",
            lambda _event:
            self._go_to_line(),
        )

    def _build_status_bar(self) -> None:
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
        )

        self.status_label.grid(
            row=3,
            column=0,
            padx=12,
            pady=7,
            sticky="ew",
        )

    def _calculate_digest(
        self,
        content: str,
    ) -> str:
        return hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

    def _load_file(self) -> None:
        try:
            content = read_source_file(
                self.file_path
            )

        except OSError as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.master_application.tr('editor_read_error')}"
                    f"\n\n{error}"
                ),
                parent=self,
            )

            self.destroy()
            return

        self.original_content = content

        self.original_digest = (
            self._calculate_digest(
                content
            )
        )

        self.editor_textbox.delete(
            "1.0",
            "end",
        )

        self.editor_textbox.insert(
            "1.0",
            content,
        )

        self.editor_textbox.edit_reset()

        self.editor_textbox.edit_modified(
            False
        )

        self.modified = False

        self._update_window_title()
        self._update_line_numbers()
        self._update_status()

    def _current_content(self) -> str:
        return self.editor_textbox.get(
            "1.0",
            "end-1c",
        )

    def _update_window_title(self) -> None:
        marker = (
            " *"
            if self.modified
            else ""
        )

        self.title(
            f"{self.master_application.tr('editor')} — "
            f"{self.file_path.name}{marker}"
        )

    def _update_line_numbers(self) -> None:
        final_index = (
            self.editor_textbox
            .index("end-1c")
        )

        total_lines = int(
            final_index.split(".")[0]
        )

        numbers = "\n".join(
            str(number)
            for number in range(
                1,
                total_lines + 1,
            )
        )

        self.line_number_textbox.configure(
            state="normal"
        )

        self.line_number_textbox.delete(
            "1.0",
            "end",
        )

        self.line_number_textbox.insert(
            "1.0",
            numbers,
        )

        self.line_number_textbox.configure(
            state="disabled"
        )

    def _update_status(self) -> None:
        cursor_index = (
            self.editor_textbox
            .index("insert")
        )

        line_text, column_text = (
            cursor_index.split(".")
        )

        status_text = (
            self.master_application.tr(
                "editor_status"
            ).format(
                line=int(line_text),
                column=int(column_text) + 1,
                characters=len(
                    self._current_content()
                ),
            )
        )

        self.status_label.configure(
            text=status_text
        )

    def _on_modified(
        self,
        _event: Any,
    ) -> None:
        if not self.editor_textbox.edit_modified():
            return

        self.modified = True

        self.editor_textbox.edit_modified(
            False
        )

        self._update_window_title()
        self._update_line_numbers()
        self._update_status()

    def _on_cursor_event(
        self,
        _event: Any,
    ) -> None:
        self.after(
            1,
            self._update_status,
        )

    def _file_changed_externally(self) -> bool:
        if not self.file_path.exists():
            return False

        try:
            disk_content = read_source_file(
                self.file_path
            )

        except OSError:
            return False

        disk_digest = self._calculate_digest(
            disk_content
        )

        return (
            disk_digest
            != self.original_digest
        )

    def _save(self) -> bool:
        if self._file_changed_externally():
            overwrite_external_change = (
                messagebox.askyesno(
                    APP_NAME,
                    self.master_application.tr(
                        "editor_file_changed_externally"
                    ),
                    parent=self,
                )
            )

            if not overwrite_external_change:
                return False

        overwrite_confirmed = (
            messagebox.askyesno(
                APP_NAME,
                self.master_application.tr(
                    "editor_confirm_overwrite"
                ),
                parent=self,
            )
        )

        if not overwrite_confirmed:
            return False

        return self._write_file(
            self.file_path
        )

    def _save_as(self) -> bool:
        destination = (
            filedialog.asksaveasfilename(
                parent=self,
                title=self.master_application.tr(
                    "editor_save_as"
                ),
                initialdir=str(
                    self.file_path.parent
                ),
                initialfile=(
                    self.file_path.name
                ),
                defaultextension=(
                    self.file_path.suffix
                ),
                filetypes=[
                    (
                        "Python",
                        "*.py",
                    ),
                    (
                        "Text",
                        "*.txt",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if not destination:
            return False

        destination_path = Path(
            destination
        )

        if (
            destination_path.exists()
            and not messagebox.askyesno(
                APP_NAME,
                self.master_application.tr(
                    "editor_confirm_overwrite"
                ),
                parent=self,
            )
        ):
            return False

        saved = self._write_file(
            destination_path
        )

        if saved:
            self.file_path = destination_path

            self.path_label.configure(
                text=str(
                    self.file_path
                )
            )

            self._update_window_title()

        return saved

    def _write_file(
        self,
        destination: Path,
    ) -> bool:
        content = self._current_content()

        try:
            destination.write_text(
                content,
                encoding="utf-8",
                newline="\n",
            )

        except OSError as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.master_application.tr('editor_save_failed')}"
                    f"\n\n{error}"
                ),
                parent=self,
            )

            return False

        self.original_content = content

        self.original_digest = (
            self._calculate_digest(
                content
            )
        )

        self.modified = False

        self.editor_textbox.edit_modified(
            False
        )

        self._update_window_title()

        messagebox.showinfo(
            APP_NAME,
            self.master_application.tr(
                "editor_file_saved"
            ),
            parent=self,
        )

        self.master_application._set_status(
            self.master_application.tr(
                "rescan_after_editor_save"
            )
        )

        return True

    def _reload(self) -> None:
        if self.modified:
            confirmed = messagebox.askyesno(
                APP_NAME,
                self.master_application.tr(
                    "editor_reload_question"
                ),
                parent=self,
            )

            if not confirmed:
                return

        self._load_file()

    def _undo(self) -> None:
        try:
            self.editor_textbox.edit_undo()
        except Exception:
            pass

    def _redo(self) -> None:
        try:
            self.editor_textbox.edit_redo()
        except Exception:
            pass

    def _select_all(self) -> None:
        self.editor_textbox.tag_add(
            "sel",
            "1.0",
            "end-1c",
        )

        self.editor_textbox.mark_set(
            "insert",
            "1.0",
        )

        self.editor_textbox.see(
            "1.0"
        )

        self.editor_textbox.focus_set()

    def _find(self) -> None:
        search_term = simpledialog.askstring(
            self.master_application.tr(
                "editor_find"
            ),
            self.master_application.tr(
                "editor_search_term"
            ),
            parent=self,
        )

        if not search_term:
            return

        self.editor_textbox.tag_remove(
            "editor_search_match",
            "1.0",
            "end",
        )

        start_index = "1.0"
        match_count = 0
        first_match = ""

        while True:
            match_index = (
                self.editor_textbox.search(
                    search_term,
                    start_index,
                    stopindex="end",
                    nocase=True,
                )
            )

            if not match_index:
                break

            match_end = (
                f"{match_index}"
                f"+{len(search_term)}c"
            )

            self.editor_textbox.tag_add(
                "editor_search_match",
                match_index,
                match_end,
            )

            if not first_match:
                first_match = match_index

            start_index = match_end
            match_count += 1

        self.editor_textbox.tag_config(
            "editor_search_match",
            background="#B7791F",
            foreground="#FFFFFF",
        )

        if first_match:
            self.editor_textbox.mark_set(
                "insert",
                first_match,
            )

            self.editor_textbox.see(
                first_match
            )

            self.status_label.configure(
                text=(
                    self.master_application.tr(
                        "editor_matches"
                    ).format(
                        count=match_count
                    )
                )
            )

        else:
            self.status_label.configure(
                text=self.master_application.tr(
                    "editor_no_match"
                )
            )

    def _replace(self) -> None:
        search_term = simpledialog.askstring(
            self.master_application.tr(
                "editor_find"
            ),
            self.master_application.tr(
                "editor_search_term"
            ),
            parent=self,
        )

        if search_term is None:
            return

        replacement = simpledialog.askstring(
            self.master_application.tr(
                "editor_replace"
            ),
            self.master_application.tr(
                "editor_replacement"
            ),
            parent=self,
        )

        if replacement is None:
            return

        current_content = (
            self._current_content()
        )

        updated_content = (
            current_content.replace(
                search_term,
                replacement,
            )
        )

        self.editor_textbox.delete(
            "1.0",
            "end",
        )

        self.editor_textbox.insert(
            "1.0",
            updated_content,
        )

        self.modified = True

        self._update_window_title()
        self._update_line_numbers()
        self._update_status()

    def _go_to_line(self) -> None:
        line_number = simpledialog.askinteger(
            self.master_application.tr(
                "editor_go_to_line"
            ),
            self.master_application.tr(
                "editor_line_number"
            ),
            parent=self,
            minvalue=1,
        )

        if line_number is None:
            return

        total_lines = int(
            self.editor_textbox
            .index("end-1c")
            .split(".")[0]
        )

        target_line = min(
            line_number,
            total_lines,
        )

        target_index = (
            f"{target_line}.0"
        )

        self.editor_textbox.mark_set(
            "insert",
            target_index,
        )

        self.editor_textbox.see(
            target_index
        )

        self.editor_textbox.focus_set()

        self._update_status()

    def _request_close(self) -> None:
        if not self.modified:
            self.destroy()
            return

        answer = messagebox.askyesnocancel(
            self.master_application.tr(
                "editor_unsaved_title"
            ),
            self.master_application.tr(
                "editor_unsaved_question"
            ),
            parent=self,
        )

        if answer is None:
            return

        if answer:
            if not self._save():
                return

        self.destroy()


class CompleteCodebaseCartographerApplication(
    CodebaseCartographerApplication
):
    """
    Aktualisiert
    """

    def __init__(self) -> None:
        self.database_manager = (
            CodebaseDatabaseManager(
                APPLICATION_DATABASE_PATH
            )
        )

        self.current_scan_id: int | None = None
        self.current_custom_message = ""

        super().__init__()

        self._install_file_editor_integration()
        self._install_custom_message_panel()
        self._install_database_archive_page()
        self._apply_complete_language()
        self._refresh_database_archive()

    def _install_file_editor_integration(
        self,
    ) -> None:
        self.files_table.tree.bind(
            "<Double-1>",
            self._open_selected_file_in_editor,
        )

        self.files_table.tree.bind(
            "<Return>",
            self._open_selected_file_in_editor,
        )

    def _install_custom_message_panel(
        self,
    ) -> None:
        self.pages[
            "dashboard"
        ].grid_rowconfigure(
            4,
            weight=1,
        )

        self.dashboard_text.grid_configure(
            row=4,
        )

        self.custom_message_frame = (
            ctk.CTkFrame(
                self.pages["dashboard"],
                corner_radius=14,
            )
        )

        self.custom_message_frame.grid(
            row=3,
            column=0,
            padx=24,
            pady=8,
            sticky="ew",
        )

        self.custom_message_frame.grid_columnconfigure(
            0,
            weight=1,
        )

        self.custom_message_title_label = (
            ctk.CTkLabel(
                self.custom_message_frame,
                text="",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold",
                ),
                anchor="w",
            )
        )

        self.custom_message_title_label.grid(
            row=0,
            column=0,
            padx=14,
            pady=(13, 4),
            sticky="ew",
        )

        self.custom_message_textbox = (
            ctk.CTkTextbox(
                self.custom_message_frame,
                height=105,
                wrap="word",
            )
        )

        self.custom_message_textbox.grid(
            row=1,
            column=0,
            padx=14,
            pady=(4, 13),
            sticky="ew",
        )

        self.custom_message_textbox.bind(
            "<KeyRelease>",
            self._update_custom_message_counter,
        )

        actions = ctk.CTkFrame(
            self.custom_message_frame,
            fg_color="transparent",
        )

        actions.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=(0, 14),
            pady=13,
            sticky="ns",
        )

        self.custom_message_counter_label = (
            ctk.CTkLabel(
                actions,
                text="",
            )
        )

        self.custom_message_counter_label.pack(
            pady=(6, 12),
        )

        self.custom_message_save_button = (
            ctk.CTkButton(
                actions,
                text="",
                width=150,
                command=(
                    self._save_custom_message
                ),
            )
        )

        self.custom_message_save_button.pack()

    def _install_database_archive_page(
        self,
    ) -> None:
        archive_page = self._create_page(
            "database"
        )

        archive_page.grid_rowconfigure(
            3,
            weight=1,
        )

        (
            self.database_title_label,
            self.database_subtitle_label,
        ) = self._create_page_header(
            archive_page
        )

        action_frame = ctk.CTkFrame(
            archive_page,
            corner_radius=0,
            fg_color="transparent",
        )

        action_frame.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        self.database_load_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                command=self._load_archived_scan,
            )
        )

        self.database_load_button.pack(
            side="left",
            padx=(0, 6),
        )

        self.database_delete_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                fg_color="transparent",
                border_width=1,
                command=self._delete_archived_scan,
            )
        )

        self.database_delete_button.pack(
            side="left",
            padx=6,
        )

        self.database_refresh_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                fg_color="transparent",
                border_width=1,
                command=self._refresh_database_archive,
            )
        )

        self.database_refresh_button.pack(
            side="left",
            padx=6,
        )

        self.database_scan_json_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                fg_color="transparent",
                border_width=1,
                command=self._export_selected_scan_json,
            )
        )

        self.database_scan_json_button.pack(
            side="left",
            padx=6,
        )

        self.database_scan_markdown_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                fg_color="transparent",
                border_width=1,
                command=(
                    self._export_selected_scan_markdown
                ),
            )
        )

        self.database_scan_markdown_button.pack(
            side="left",
            padx=6,
        )

        self.database_export_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                command=(
                    self._export_complete_database
                ),
            )
        )

        self.database_export_button.pack(
            side="right",
            padx=(6, 0),
        )

        self.database_import_button = (
            ctk.CTkButton(
                action_frame,
                text="",
                fg_color="transparent",
                border_width=1,
                command=(
                    self._import_complete_database
                ),
            )
        )

        self.database_import_button.pack(
            side="right",
            padx=6,
        )

        archive_columns = [
            "scan_id",
            "project",
            "date",
            "files",
            "findings",
            "quality",
            "message",
        ]

        self.database_table = (
            ModernTreeview(
                archive_page,
                columns=archive_columns,
                column_widths={
                    "scan_id": 80,
                    "project": 390,
                    "date": 190,
                    "files": 80,
                    "findings": 90,
                    "quality": 90,
                    "message": 380,
                },
            )
        )

        self.database_table.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 24),
            sticky="nsew",
        )

        self.database_table.tree.bind(
            "<Double-1>",
            lambda _event:
            self._load_archived_scan(),
        )

        self.database_navigation_button = (
            ctk.CTkButton(
                self.sidebar,
                text="",
                height=42,
                corner_radius=10,
                anchor="w",
                fg_color="transparent",
                hover_color=(
                    "gray82",
                    "gray25",
                ),
                command=lambda:
                self._show_page("database"),
            )
        )

        self.database_navigation_button.grid(
            row=8,
            column=0,
            padx=14,
            pady=4,
            sticky="ew",
        )

        self.navigation_buttons[
            "database"
        ] = self.database_navigation_button

    def _apply_complete_language(
        self,
    ) -> None:
        self.custom_message_title_label.configure(
            text=self.tr(
                "custom_message"
            )
        )

        self.custom_message_save_button.configure(
            text=self.tr(
                "save_custom_message"
            )
        )

        self.database_title_label.configure(
            text=self.tr(
                "database_archive"
            )
        )

        self.database_subtitle_label.configure(
            text=self.tr(
                "database_archive_hint"
            )
        )

        self.database_navigation_button.configure(
            text=self.tr(
                "database"
            )
        )

        self.database_load_button.configure(
            text=self.tr(
                "archive_load"
            )
        )

        self.database_delete_button.configure(
            text=self.tr(
                "archive_delete"
            )
        )

        self.database_refresh_button.configure(
            text=self.tr(
                "archive_refresh"
            )
        )

        self.database_scan_json_button.configure(
            text=self.tr(
                "archive_export_scan_json"
            )
        )

        self.database_scan_markdown_button.configure(
            text=self.tr(
                "archive_export_scan_markdown"
            )
        )

        self.database_export_button.configure(
            text=self.tr(
                "archive_export_database"
            )
        )

        self.database_import_button.configure(
            text=self.tr(
                "archive_import_database"
            )
        )

        self.database_table.set_headings(
            {
                "scan_id": self.tr(
                    "scan_id"
                ),
                "project": self.tr(
                    "archive_project"
                ),
                "date": self.tr(
                    "archive_date"
                ),
                "files": self.tr(
                    "archive_files"
                ),
                "findings": self.tr(
                    "archive_findings"
                ),
                "quality": self.tr(
                    "quality_score"
                ),
                "message": self.tr(
                    "archive_message"
                ),
            }
        )

        self._update_custom_message_counter()

    def _toggle_language(self) -> None:
        super()._toggle_language()
        self._apply_complete_language()
        self._refresh_database_archive()

    def _show_page(
        self,
        page_name: str,
    ) -> None:
        super()._show_page(
            page_name
        )

        if page_name == "database":
            self._refresh_database_archive()

    def _analysis_finished(
        self,
        result: ProjectAnalysis,
    ) -> None:
        custom_message = (
            self._get_custom_message()
        )

        if len(custom_message) > (
            MAX_CUSTOM_MESSAGE_LENGTH
        ):
            custom_message = custom_message[
                :MAX_CUSTOM_MESSAGE_LENGTH
            ]

        self.current_scan_id = (
            self.database_manager.save_analysis(
                result,
                custom_message,
            )
        )

        self.current_custom_message = (
            custom_message
        )

        super()._analysis_finished(
            result
        )

        self._set_status(
            (
                f"{self.status_label.cget('text')} · "
                f"{self.tr('automatic_archive_saved')} "
                f"ID {self.current_scan_id}"
            )
        )

        self._refresh_database_archive()

    def _reset_views(self) -> None:
        super()._reset_views()

        if hasattr(
            self,
            "custom_message_textbox",
        ):
            self.custom_message_textbox.delete(
                "1.0",
                "end",
            )

            self.current_custom_message = ""

            self._update_custom_message_counter()

    def _get_custom_message(self) -> str:
        return (
            self.custom_message_textbox
            .get(
                "1.0",
                "end-1c",
            )
        )

    def _set_custom_message(
        self,
        message: str,
    ) -> None:
        self.custom_message_textbox.delete(
            "1.0",
            "end",
        )

        self.custom_message_textbox.insert(
            "1.0",
            message,
        )

        self.current_custom_message = message

        self._update_custom_message_counter()

    def _update_custom_message_counter(
        self,
        _event: Any = None,
    ) -> None:
        if not hasattr(
            self,
            "custom_message_textbox",
        ):
            return

        character_count = len(
            self._get_custom_message()
        )

        counter_text = self.tr(
            "custom_message_counter"
        ).format(
            count=character_count
        )

        self.custom_message_counter_label.configure(
            text=counter_text
        )

        if character_count > (
            MAX_CUSTOM_MESSAGE_LENGTH
        ):
            self.custom_message_counter_label.configure(
                text_color="#D32F2F"
            )

            self.custom_message_save_button.configure(
                state="disabled"
            )

        else:
            self.custom_message_counter_label.configure(
                text_color=(
                    "gray25",
                    "gray75",
                )
            )

            self.custom_message_save_button.configure(
                state="normal"
            )

    def _save_custom_message(self) -> None:
        custom_message = (
            self._get_custom_message()
        )

        if len(custom_message) > (
            MAX_CUSTOM_MESSAGE_LENGTH
        ):
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "custom_message_too_long"
                ),
            )

            return

        if self.current_scan_id is None:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "custom_message_requires_scan"
                ),
            )

            return

        self.database_manager.update_custom_message(
            self.current_scan_id,
            custom_message,
        )

        self.current_custom_message = (
            custom_message
        )

        self._refresh_database_archive()

        messagebox.showinfo(
            APP_NAME,
            self.tr(
                "custom_message_saved"
            ),
        )

    def _selected_file_analysis(
        self,
    ) -> FileAnalysis | None:
        if not self.analysis_result:
            return None

        selection = (
            self.files_table.tree
            .selection()
        )

        if not selection:
            return None

        values = (
            self.files_table.tree
            .item(
                selection[0],
                "values",
            )
        )

        if not values:
            return None

        relative_path = str(
            values[0]
        )

        for file_analysis in (
            self.analysis_result.files
        ):
            if (
                file_analysis.relative_path
                == relative_path
            ):
                return file_analysis

        return None

    def _open_selected_file_in_editor(
        self,
        _event: Any = None,
    ) -> None:
        selected_file = (
            self._selected_file_analysis()
        )

        if selected_file is None:
            return

        file_path = Path(
            selected_file.absolute_path
        )

        if not file_path.is_file():
            messagebox.showerror(
                APP_NAME,
                self.tr(
                    "editor_invalid_file"
                ),
            )

            return

        SourceCodeEditorWindow(
            self,
            file_path,
        )

    def _selected_archive_scan_id(
        self,
    ) -> int | None:
        selection = (
            self.database_table.tree
            .selection()
        )

        if not selection:
            return None

        values = (
            self.database_table.tree
            .item(
                selection[0],
                "values",
            )
        )

        if not values:
            return None

        return int(
            values[0]
        )

    def _refresh_database_archive(
        self,
    ) -> None:
        if not hasattr(
            self,
            "database_table",
        ):
            return

        self.database_table.clear()

        for row in (
            self.database_manager.list_scans()
        ):
            self.database_table.insert(
                [
                    row["id"],
                    row["project_path"],
                    row["generated_at"],
                    row["file_count"],
                    row["finding_count"],
                    (
                        f"{row['quality_score']}"
                        f" / 100"
                    ),
                    str(
                        row["custom_message"]
                    )[:180],
                ]
            )

    def _load_archived_scan(self) -> None:
        scan_id = (
            self._selected_archive_scan_id()
        )

        if scan_id is None:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "archive_no_selection"
                ),
            )

            return

        analysis, custom_message = (
            self.database_manager.load_scan(
                scan_id
            )
        )

        self.current_scan_id = scan_id
        self.current_custom_message = (
            custom_message
        )

        self.analysis_result = analysis

        project_path = Path(
            analysis.project_path
        )

        self.project_path = project_path

        self._update_project_path_label()
        self._set_custom_message(
            custom_message
        )
        self._render_all()
        self._show_page(
            "dashboard"
        )

        self._set_status(
            (
                f"{self.tr('archive_loaded')} "
                f"ID {scan_id}"
            )
        )

    def _delete_archived_scan(self) -> None:
        scan_id = (
            self._selected_archive_scan_id()
        )

        if scan_id is None:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "archive_no_selection"
                ),
            )

            return

        confirmed = messagebox.askyesno(
            APP_NAME,
            self.tr(
                "archive_delete_question"
            ),
        )

        if not confirmed:
            return

        self.database_manager.delete_scan(
            scan_id
        )

        if self.current_scan_id == scan_id:
            self.current_scan_id = None

        self._refresh_database_archive()

        messagebox.showinfo(
            APP_NAME,
            self.tr(
                "archive_deleted"
            ),
        )

    def _export_selected_scan_json(
        self,
    ) -> None:
        scan_id = (
            self._selected_archive_scan_id()
        )

        if scan_id is None:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "archive_no_selection"
                ),
            )

            return

        payload = (
            self.database_manager
            .export_scan_payload(
                scan_id
            )
        )

        destination = (
            filedialog.asksaveasfilename(
                title=self.tr(
                    "archive_export_scan_json"
                ),
                defaultextension=".json",
                initialfile=(
                    f"codebase_scan_{scan_id}.json"
                ),
                filetypes=[
                    (
                        "JSON",
                        "*.json",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if not destination:
            return

        try:
            Path(destination).write_text(
                json.dumps(
                    payload,
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            messagebox.showinfo(
                APP_NAME,
                self.tr(
                    "export_success"
                ),
            )

        except OSError as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('export_failed')}"
                    f"\n\n{error}"
                ),
            )

    def _export_selected_scan_markdown(
        self,
    ) -> None:
        scan_id = (
            self._selected_archive_scan_id()
        )

        if scan_id is None:
            messagebox.showwarning(
                APP_NAME,
                self.tr(
                    "archive_no_selection"
                ),
            )

            return

        archived_analysis, custom_message = (
            self.database_manager.load_scan(
                scan_id
            )
        )

        previous_analysis = (
            self.analysis_result
        )

        previous_message = (
            self.current_custom_message
        )

        try:
            self.analysis_result = (
                archived_analysis
            )

            report = (
                self._build_markdown_report()
            )

            report = (
                f"{report}\n\n"
                f"## {self.tr('custom_message')}\n\n"
                f"{custom_message or '—'}\n"
            )

        finally:
            self.analysis_result = (
                previous_analysis
            )

            self.current_custom_message = (
                previous_message
            )

        destination = (
            filedialog.asksaveasfilename(
                title=self.tr(
                    "archive_export_scan_markdown"
                ),
                defaultextension=".md",
                initialfile=(
                    f"codebase_scan_{scan_id}.md"
                ),
                filetypes=[
                    (
                        "Markdown",
                        "*.md",
                    ),
                    (
                        "Text",
                        "*.txt",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if not destination:
            return

        try:
            Path(destination).write_text(
                report,
                encoding="utf-8",
            )

            messagebox.showinfo(
                APP_NAME,
                self.tr(
                    "export_success"
                ),
            )

        except OSError as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('export_failed')}"
                    f"\n\n{error}"
                ),
            )

    def _export_complete_database(
        self,
    ) -> None:
        destination = (
            filedialog.asksaveasfilename(
                title=self.tr(
                    "database_export_title"
                ),
                defaultextension=".ccdb",
                initialfile=(
                    "codebase_cartographer_backup.ccdb"
                ),
                filetypes=[
                    (
                        "Codebase Cartographer Database",
                        "*.ccdb",
                    ),
                    (
                        "All files",
                        "*.*",
                    ),
                ],
            )
        )

        if not destination:
            return

        password = DatabasePasswordDialog(
            self,
            self.tr(
                "database_export_title"
            ),
            require_confirmation=True,
        ).show()

        if not password:
            return

        try:
            export_password_protected_database(
                self.database_manager,
                Path(destination),
                password,
            )

            messagebox.showinfo(
                APP_NAME,
                self.tr(
                    "database_exported"
                ),
            )

        except Exception as error:
            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('database_export_failed')}"
                    f"\n\n{error}"
                ),
            )

    def _import_complete_database(
        self,
    ) -> None:
        source = filedialog.askopenfilename(
            title=self.tr(
                "database_import_title"
            ),
            filetypes=[
                (
                    "Codebase Cartographer Database",
                    "*.ccdb",
                ),
                (
                    "All files",
                    "*.*",
                ),
            ],
        )

        if not source:
            return

        confirmed = messagebox.askyesno(
            APP_NAME,
            self.tr(
                "database_import_warning"
            ),
        )

        if not confirmed:
            return

        password = DatabasePasswordDialog(
            self,
            self.tr(
                "database_import_title"
            ),
            require_confirmation=False,
        ).show()

        if not password:
            return

        backup_path = (
            APPLICATION_DATABASE_PATH
            .with_suffix(
                ".before_import.sqlite3"
            )
        )

        try:
            self.database_manager.checkpoint()

            if APPLICATION_DATABASE_PATH.exists():
                shutil.copy2(
                    APPLICATION_DATABASE_PATH,
                    backup_path,
                )

            import_password_protected_database(
                Path(source),
                APPLICATION_DATABASE_PATH,
                password,
            )

            self.database_manager = (
                CodebaseDatabaseManager(
                    APPLICATION_DATABASE_PATH
                )
            )

            self.current_scan_id = None
            self._refresh_database_archive()

            messagebox.showinfo(
                APP_NAME,
                self.tr(
                    "database_imported"
                ),
            )

        except (
            InvalidTag,
            ValueError,
        ):
            if backup_path.exists():
                shutil.copy2(
                    backup_path,
                    APPLICATION_DATABASE_PATH,
                )

            messagebox.showerror(
                APP_NAME,
                self.tr(
                    "database_wrong_password"
                ),
            )

        except Exception as error:
            if backup_path.exists():
                shutil.copy2(
                    backup_path,
                    APPLICATION_DATABASE_PATH,
                )

            messagebox.showerror(
                APP_NAME,
                (
                    f"{self.tr('database_import_failed')}"
                    f"\n\n{error}"
                ),
            )

        finally:
            backup_path.unlink(
                missing_ok=True
            )

    def _analysis_as_dictionary(
        self,
    ) -> dict[str, Any]:
        payload = super()._analysis_as_dictionary()

        payload["archive"] = {
            "scan_id": self.current_scan_id,
            "custom_message": (
                self._get_custom_message()
                if hasattr(
                    self,
                    "custom_message_textbox",
                )
                else self.current_custom_message
            ),
            "database_path": str(
                APPLICATION_DATABASE_PATH
            ),
        }

        return payload

    def _build_markdown_report(
        self,
    ) -> str:
        report = super()._build_markdown_report()

        custom_message = (
            self._get_custom_message()
            if hasattr(
                self,
                "custom_message_textbox",
            )
            else self.current_custom_message
        )

        return (
            f"{report}\n\n"
            f"## {self.tr('custom_message')}\n\n"
            f"{custom_message or '—'}\n\n"
            f"**{self.tr('scan_id')}:** "
            f"{self.current_scan_id or '—'}\n"
        )

    def _show_about_dialog(self) -> None:
        super()._show_about_dialog()

        self._set_status(
            (
                f"{self.tr('database_path')}: "
                f"{APPLICATION_DATABASE_PATH} · "
                f"{self.tr('database_encryption')}"
            )
        )

def main() -> None:
    application = (
        CompleteCodebaseCartographerApplication()
    )

    application.mainloop()


if __name__ == "__main__":
    main()
