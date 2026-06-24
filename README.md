# Codebase Cartographer

> A local-first desktop application for exploring, analyzing, documenting, editing, and archiving Python codebases.

| ![Version](https://img.shields.io/badge/version-1.0.0-blue) | ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) | ![License](https://img.shields.io/badge/license-MIT-green) | ![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey) | ![UI](https://img.shields.io/badge/UI-CustomTkinter-1F6AA5)
|---|---|---|---|---|

**Author:** BylickiLabs / Thorsten Bylicki  
**Version:** 1.0.0  
**Release:** June 2026  
**License:** MIT  

<br>

---

<br>

## Table of Contents

### English

1. [Overview](#overview)
2. [Core Features](#core-features)
3. [Analysis Scope](#analysis-scope)
4. [Findings and Thresholds](#findings-and-thresholds)
5. [Quality Index](#quality-index)
6. [Integrated Source-Code Editor](#integrated-source-code-editor)
7. [SQLite Scan Archive](#sqlite-scan-archive)
8. [Encrypted Database Packages](#encrypted-database-packages)
9. [Privacy and Security](#privacy-and-security)
10. [System Requirements](#system-requirements)
11. [Installation](#installation)
12. [Running the Application](#running-the-application)
13. [Usage](#usage)
14. [User Interface](#user-interface)
15. [Export Formats](#export-formats)
16. [Excluded Directories and File Limits](#excluded-directories-and-file-limits)
17. [Project Architecture](#project-architecture)
18. [Data Model](#data-model)
19. [Limitations](#limitations)
20. [Troubleshooting](#troubleshooting)
21. [Development](#development)
22. [Contributing](#contributing)
23. [License](#license)
24. [Author and Copyright](#author-and-copyright)

### German

1. [Überblick](#überblick)
2. [Hauptfunktionen](#hauptfunktionen)
3. [Analyseumfang](#analyseumfang)
4. [Befunde und Grenzwerte](#befunde-und-grenzwerte)
5. [Qualitätsindex](#qualitätsindex)
6. [Integrierter Quelltexteditor](#integrierter-quelltexteditor)
7. [SQLite-Analysearchiv](#sqlite-analysearchiv)
8. [Verschlüsselte Datenbankpakete](#verschlüsselte-datenbankpakete)
9. [Datenschutz und Sicherheit](#datenschutz-und-sicherheit)
10. [Systemanforderungen](#systemanforderungen)
11. [Installation auf Deutsch](#installation-auf-deutsch)
12. [Anwendung starten](#anwendung-starten)
13. [Bedienung](#bedienung)
14. [Benutzeroberfläche](#benutzeroberfläche)
15. [Exportformate auf Deutsch](#exportformate-auf-deutsch)
16. [Ausgeschlossene Verzeichnisse und Dateigrenzen](#ausgeschlossene-verzeichnisse-und-dateigrenzen)
17. [Projektarchitektur](#projektarchitektur)
18. [Datenmodell](#datenmodell)
19. [Einschränkungen](#einschränkungen)
20. [Fehlerbehebung](#fehlerbehebung)
21. [Entwicklung](#entwicklung)
22. [Mitwirken](#mitwirken)
23. [Lizenz auf Deutsch](#lizenz-auf-deutsch)
24. [Autor und Urheberrecht](#autor-und-urheberrecht)

<br>

---

<br>

## Overview

Codebase Cartographer is a bilingual desktop analysis tool designed for Python projects. It performs static analysis through Python's Abstract Syntax Tree (`ast`) and therefore does not need to execute the analyzed project.

The application is intended for developers, maintainers, reviewers, educators, and teams that need a fast local overview of an unfamiliar or growing Python codebase. It combines codebase exploration, quality indicators, issue-oriented findings, source editing, reporting, and historical scan storage in one desktop interface.

### Primary objectives

- Provide an immediate structural overview of a Python project.
- Identify potential maintainability and documentation risks.
- Display dependencies and classify imports.
- Detect syntax errors before deeper metrics are trusted.
- Keep source code and scan results under local control.
- Preserve completed scans in a searchable local archive.
- Allow selected project files to be edited directly from the application.
- Export analysis results for documentation, review, or further processing.

> [!IMPORTANT]
> Codebase Cartographer provides heuristic indicators and static-analysis findings. It is not a replacement for tests, security audits, type checking, linting, runtime profiling, or professional code review.

<br>

---

<br>

## Core Features

### Local static analysis

- Recursively discovers Python files.
- Parses source code with Python's `ast` module.
- Does not import or execute analyzed project modules.
- Counts total, code, comment, and blank lines.
- Detects syntax errors with line and column details.
- Extracts modules, classes, functions, asynchronous functions, and methods.
- Records symbol location, parent context, documentation state, complexity, and nesting.
- Extracts imports and imported names.
- Classifies imports as standard-library, external, local/project, relative, or unknown.
- Detects wildcard imports.
- Detects `TODO`, `FIXME`, `HACK`, and `XXX` markers.

### Maintainability indicators

- File-level complexity.
- Symbol-level complexity.
- Maximum nesting depth.
- Large-file detection.
- Missing module docstrings.
- Missing public-symbol docstrings.
- Repeated public symbol names across multiple files.
- Prioritized findings from informational to critical.
- Calculated documentation coverage and quality index.

### Desktop interface

- Modern CustomTkinter interface.
- Dark, light, and system appearance modes.
- German and English language switching at runtime.
- Dashboard with project metrics.
- Filterable file, symbol, and finding views.
- Dependency overview.
- Detailed report view.
- Cross-platform project-folder opening.
- Background analysis thread to keep the interface responsive.

### Editing, reports, and persistence

- Integrated UTF-8 source-code editor.
- Open files by double-clicking or pressing `Enter` in the file list.
- Save, Save As, reload, search, replace, go to line, undo, and redo.
- Detection of externally modified files before overwriting.
- JSON and Markdown report export.
- Automatic SQLite storage after each completed scan.
- Custom project or scan message with a maximum of 1,000 characters.
- Load, delete, refresh, and export archived scans.
- Password-protected full database export and import.

<br>

---

<br>

## Analysis Scope

Codebase Cartographer currently analyzes files with the following extension:

```text
.py
```

For each eligible Python file, the analyzer can collect:

| Area | Collected information |
|---|---|
| File | Absolute path, relative path, module name, size, line counts, status |
| Structure | Classes, functions, async functions, and methods |
| Symbols | Name, type, start line, end line, parent, docstring, complexity, nesting |
| Imports | Module, imported names, line, category, wildcard state |
| Documentation | Module docstring and public-symbol docstrings |
| Maintenance | TODO, FIXME, HACK, and XXX markers |
| Complexity | File complexity, symbol complexity, maximum nesting |
| Errors | Python syntax errors and skipped-file reasons |

### Import categories

| Category | Meaning |
|---|---|
| `standard_library` | The root module is part of Python's standard library. |
| `external` | The module is not recognized as standard-library or local. |
| `local` | The root module matches a discovered project module. |
| `relative` | The import uses one or more leading dots. |
| `unknown` | The module cannot be classified reliably. |

> [!NOTE]
> Import classification is intentionally lightweight. It does not resolve virtual environments, installed distributions, namespace packages, dynamic imports, or every possible package layout.

<br>

---

<br>

## Findings and Thresholds

The default limits are defined directly in the application and can be adjusted by developers.

| Setting | Default | Effect |
|---|---:|---|
| Maximum file size | 3,000,000 bytes | Larger Python files are skipped. |
| Large-file threshold | 500 lines | Generates a maintainability finding. |
| High file complexity | 25 | Generates a file-complexity finding. |
| High symbol complexity | 10 | Generates a symbol-complexity finding. |
| Deep nesting | 5 levels | Generates a nesting finding. |
| Custom message length | 1,000 characters | Longer messages cannot be saved. |

### Finding severities

| Severity | Typical meaning |
|---|---|
| `critical` | A fundamental problem, such as a syntax error. |
| `high` | A strong maintainability concern requiring attention. |
| `medium` | A relevant issue that should be reviewed. |
| `low` | A minor quality, documentation, or maintenance issue. |
| `info` | An architectural observation without a direct penalty. |

### Detected finding types

- File skipped because it exceeds the configured size limit.
- Python syntax error.
- Very large source file.
- High file complexity.
- Complex class, function, async function, or method.
- Deep nesting.
- Missing module docstring.
- Public symbols without docstrings.
- Open TODO or FIXME-style markers.
- Wildcard import.
- Public symbol name appearing in at least three different files.

### Complexity calculation

The built-in visitor starts with a base complexity of `1` and increases the value for control-flow constructs such as:

- `if`
- `for` and `async for`
- `while`
- `try`
- `with` and `async with`
- conditional expressions
- assertions
- comprehensions
- `match`
- exception handlers
- additional Boolean operands

This is a practical heuristic inspired by cyclomatic complexity, but it is not guaranteed to produce the same values as tools such as Radon, Ruff, or SonarQube.

<br>

---

<br>

## Quality Index

The dashboard calculates a quality index between `0` and `100`.

### Severity penalties

| Severity | Penalty per finding |
|---|---:|
| Critical | 18 |
| High | 9 |
| Medium | 4 |
| Low | 1 |
| Info | 0 |

### Documentation component

Documentation coverage combines:

- **70%** public-symbol documentation coverage.
- **30%** module documentation coverage.

The resulting documentation percentage contributes a bonus of up to 15 points before the final result is restricted to the range from 0 to 100.

Conceptually:

```text
quality score = clamp(100 - finding penalties + documentation bonus, 0, 100)
```

> [!CAUTION]
> The quality index is a project-orientation metric, not an objective certification of source-code quality or security.

<br>

---

<br>

## Integrated Source-Code Editor

The integrated editor allows files from the current analysis to be opened directly from the **Files** page.

### Opening a file

- Double-click a file row.
- Select a row and press `Enter`.

### Editor functions

- Save the current file.
- Save the content under a different path.
- Reload the file from disk.
- Find text.
- Replace text.
- Jump to a specific line.
- Select all content.
- Undo and redo changes.
- Display line, column, encoding, and character count.
- Warn about unsaved changes before closing.
- Detect whether the source file changed outside the editor.
- Ask for confirmation before overwriting the original project file.

The editor reads and writes text as UTF-8. After saving a source file, run the project analysis again to update metrics and findings.

> [!WARNING]
> The editor can overwrite project files. Use version control and commit or back up important work before editing.

<br>

---

<br>

## SQLite Scan Archive

Every successfully completed analysis is stored automatically in a local SQLite database.

### Default database path

```text
~/.codebase_cartographer/codebase_cartographer.sqlite3
```

On Windows, `~` normally resolves to the current user's profile directory.

### Stored scan information

- Scan ID.
- Project path.
- Analysis timestamp.
- Custom message.
- File count.
- Finding count.
- Quality score.
- Complete serialized analysis payload.
- Application version.
- Database creation timestamp.

### Archive functions

- List saved scans.
- Refresh the archive view.
- Load a selected scan into the interface.
- Open a scan by double-clicking it.
- Delete a selected scan permanently.
- Export one scan as JSON.
- Export one scan as Markdown.
- Export the complete database as a password-protected `.ccdb` package.
- Import a password-protected `.ccdb` package.

SQLite is configured with foreign-key enforcement, Write-Ahead Logging, and normal synchronous mode.

<br>

---

<br>

## Encrypted Database Packages

Full database exports use the custom `.ccdb` package format.

### Cryptographic design

- Encryption: **AES-256-GCM**.
- Key derivation: **PBKDF2-HMAC-SHA-256**.
- Derived key length: 32 bytes.
- PBKDF2 iterations: 390,000.
- Random salt: 16 bytes.
- Random nonce: 12 bytes.
- Authentication: built into AES-GCM.
- Package header is authenticated as additional data.

### Import behavior

Before an imported database replaces the current local database:

1. The current SQLite WAL is checkpointed.
2. A temporary backup of the existing database is created.
3. The `.ccdb` package header is validated.
4. The package is decrypted with the entered password.
5. SQLite performs an integrity check on the decrypted temporary database.
6. The validated database replaces the active database.
7. The backup is restored if an error occurs during the process.

> [!IMPORTANT]
> Passwords are not recoverable. A lost password means the encrypted `.ccdb` package cannot be decrypted by the application.

<br>

---

<br>

## Privacy and Security

### Local-first processing

The analyzer works on local files. The application does not contain a feature that uploads source code, project files, reports, or database records to a remote analysis service.

### What remains local

- Selected project path.
- Source-code analysis.
- Generated findings.
- Reports until the user exports or moves them.
- SQLite archive.
- Custom messages.

### Important security distinction

- The regular SQLite database at `~/.codebase_cartographer/codebase_cartographer.sqlite3` is stored as a normal local SQLite file.
- Password-based AES-256-GCM protection applies to exported `.ccdb` packages.
- The source-code editor can modify original files.
- The GitHub button opens the configured BylickiLabs profile in the system browser.

Users are responsible for operating-system permissions, disk encryption, backups, password management, and access control to the local user account.

<br>

---

<br>

## System Requirements

### Required

- Python **3.10 or newer**.
- Tk support for the installed Python version.
- A graphical desktop environment.
- Read access to the project being analyzed.
- Write access for editor saves, exports, and the local database directory.

### Python packages

```text
customtkinter
cryptography
```

The remaining imported modules are part of the Python standard library.

### Platform notes

| Platform | Notes |
|---|---|
| Windows | Python from python.org normally includes Tk. Project folders are opened through the Windows shell. |
| Linux | Tk may require a separate distribution package. Folders are opened with `xdg-open`. |
| macOS | Tk must be available to Python. Folders are opened with the `open` command. |

<br>

---

<br>

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/bylickilabs/codebase_cartographer.git
cd codebase_cartographer
```

Replace `codebase_cartographer` with the actual repository name.

### 2. Create a virtual environment

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4. Install dependencies

```bash
pip install customtkinter cryptography
```

Recommended `requirements.txt`:

```text
customtkinter
cryptography
```

Install from the file with:

```bash
pip install -r requirements.txt
```

### Linux: install Tk when required

Debian or Ubuntu example:

```bash
sudo apt update
sudo apt install python3-tk
```

The exact package name depends on the Linux distribution.

---

## Running the Application

Assuming the application file is named `codebase_cartographer.py`:

```bash
python codebase_cartographer.py
```

On Windows, this may also be used:

```powershell
py codebase_cartographer.py
```

The program starts the `CompleteCodebaseCartographerApplication` and opens the graphical interface.

<br>

---

<br>

## Usage

### Analyze a project

1. Start Codebase Cartographer.
2. Select **Select project**.
3. Choose an existing Python project directory.
4. Select **Start analysis**.
5. Review the dashboard, files, symbols, dependencies, findings, and report pages.
6. Add an optional custom message of up to 1,000 characters.
7. Save the message after a scan has been created.

### Edit a project file

1. Open the **Files** page.
2. Select a file.
3. Double-click the file or press `Enter`.
4. Make the required changes.
5. Save or use **Save As**.
6. Run the analysis again to refresh all metrics.

### Load an archived scan

1. Open the **Database** page.
2. Select a scan.
3. Choose **Load scan** or double-click the archive row.
4. Review the restored analysis and custom message.

### Export an encrypted database package

1. Open the **Database** page.
2. Choose **Export database**.
3. Select a destination ending in `.ccdb`.
4. Enter and confirm a strong password.
5. Store the password separately and securely.

### Import an encrypted database package

1. Open the **Database** page.
2. Choose **Import database**.
3. Confirm that the current local database may be replaced.
4. Select a `.ccdb` package.
5. Enter its password.
6. Wait for decryption and the SQLite integrity check to complete.

<br>

---

<br>

## User Interface

| Page | Purpose |
|---|---|
| Dashboard | Shows core metrics, project information, top dependencies, complex files, and the custom message. |
| Files | Lists analyzed files with size, lines, symbols, imports, complexity, and status. |
| Structure | Lists classes, functions, async functions, and methods with location and documentation state. |
| Dependencies | Aggregates imported modules, categories, usage counts, and referencing files. |
| Findings | Displays prioritized findings, descriptions, file locations, and recommendations. |
| Report | Shows the generated report and provides JSON and Markdown export actions. |
| Database | Lists archived scans and provides archive, scan-export, database-export, and database-import actions. |

### Global controls

- Project selection.
- Start analysis.
- Open selected project folder.
- Switch between German and English.
- Switch appearance mode.
- Open the BylickiLabs GitHub page.
- Open application information.

<br>

---

<br>

## Export Formats

### JSON report

The JSON representation includes application metadata, project information, totals, files, symbols, imports, findings, archive information, and the custom message where applicable.

JSON is suitable for:

- Automated processing.
- Additional reporting.
- Data migration.
- Integration with internal tooling.
- Long-term structured storage.

### Markdown report

The Markdown report provides a human-readable project summary that can be used in:

- GitHub issues.
- Pull requests.
- Project documentation.
- Review notes.
- Internal technical reports.

The extended report also contains the custom message and scan ID.

### `.ccdb` database package

A `.ccdb` file contains an encrypted copy of the complete local SQLite database. It is intended for backup or transfer between installations of Codebase Cartographer.

<br>

---

<br>

## Excluded Directories and File Limits

The recursive scanner excludes hidden directories and the following directory names by default:

```text
.git
.github
.hg
.svn
.idea
.vscode
.venv
venv
env
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
.tox
.nox
node_modules
site-packages
dist
build
```

Other non-Python files are counted as ignored files but are not analyzed.

Python files larger than `3,000,000` bytes are recorded as skipped and produce a low-severity finding.

<br>

---

<br>

## Project Architecture

The current implementation is designed as a single-file desktop application. Its internal responsibilities are separated through data classes, visitors, utility functions, UI components, persistence services, and specialized windows.

### Major components

| Component | Responsibility |
|---|---|
| `SymbolInformation` | Stores details about a discovered code symbol. |
| `ImportInformation` | Stores details about an import statement. |
| `Finding` | Represents a prioritized analysis finding. |
| `FileAnalysis` | Stores all collected metrics for one file. |
| `ProjectAnalysis` | Aggregates project results and calculates totals. |
| `ComplexityVisitor` | Calculates heuristic complexity and nesting values. |
| `PythonStructureVisitor` | Extracts classes, functions, methods, and imports from the AST. |
| Analysis functions | Discover files, parse source, count lines, detect markers, and create findings. |
| `ModernTreeview` | Provides reusable tabular views with scrollbars. |
| `MetricCard` | Displays dashboard metrics. |
| `CodebaseCartographerApplication` | Implements the base analyzer interface and report workflow. |
| Serialization functions | Convert project analyses to and from JSON-compatible dictionaries. |
| `CodebaseDatabaseManager` | Creates and manages the SQLite archive. |
| Cryptographic functions | Derive keys and import or export protected database packages. |
| `DatabasePasswordDialog` | Collects database package passwords. |
| `SourceCodeEditorWindow` | Implements integrated file editing. |
| `CompleteCodebaseCartographerApplication` | Combines analysis, editor, custom messages, and database archive. |

### Analysis workflow

```text
Select project
    ↓
Discover eligible Python files
    ↓
Collect project module names
    ↓
Read and parse each file
    ↓
Extract symbols and imports
    ↓
Calculate lines, complexity, nesting, and documentation
    ↓
Create prioritized findings
    ↓
Calculate project totals and quality index
    ↓
Render views and reports
    ↓
Automatically archive the completed scan in SQLite
```

<br>

---

<br>

## Data Model

### `ProjectAnalysis`

A project analysis contains:

- Project path.
- Generation timestamp.
- List of file analyses.
- List of findings.
- Ignored-file count.
- Excluded-directory configuration.

### `FileAnalysis`

A file analysis contains:

- Absolute and relative paths.
- Module name.
- File size.
- Total, code, comment, and blank lines.
- Module-docstring state.
- Symbols.
- Imports.
- TODO-style markers.
- Complexity.
- Maximum nesting.
- Syntax error or skipped reason.

### SQLite schema

The `project_scans` table stores:

```sql
id
project_path
generated_at
custom_message
file_count
finding_count
quality_score
payload_json
application_version
created_at
```

Indexes are created for project path and generation time.

<br>

---

<br>

## Limitations

- Only `.py` files are analyzed.
- Analysis is static and does not inspect runtime behavior.
- Dynamic imports may not be detected.
- Import classification is heuristic.
- The line counter does not fully replicate Python tokenization semantics.
- Multiline strings are counted as code, including docstrings.
- Complexity values are application-specific heuristics.
- Duplicate-symbol detection is based on matching public names across at least three files.
- The tool does not create a complete call graph or dependency graph.
- It does not resolve inheritance, decorators, type aliases, generated code, or monkey patching in depth.
- It does not replace Ruff, Flake8, Pylint, MyPy, Pyright, Bandit, pytest, coverage tools, or dedicated security scanners.
- The editor is a practical text editor, not a full IDE or Language Server Protocol client.
- Archived scan paths may point to files that were moved, renamed, or deleted after the scan.
- The local SQLite database is not encrypted at rest by the application.

<br>

---

<br>

## Troubleshooting

### `CustomTkinter was not found`

Install the dependency in the same Python environment used to start the application:

```bash
python -m pip install customtkinter
```

### `The 'cryptography' extension was not found`

```bash
python -m pip install cryptography
```

### `No module named tkinter`

Install the Tk package for the operating system. Debian or Ubuntu example:

```bash
sudo apt install python3-tk
```

### The application starts with the wrong Python environment

Check the executable and package installation:

```bash
python --version
python -m pip show customtkinter cryptography
```

### A file is missing from the analysis

Verify that:

- The file ends in `.py`.
- The file is not located in an excluded or hidden directory.
- The file does not exceed the configured maximum size.
- The selected project directory is correct.

### A file reports a syntax error

Open the file in the integrated editor or an IDE and correct the reported line and column. Other structural metrics for that file should not be treated as complete until the syntax error is fixed.

### The editor warns that a file changed externally

Another process modified the file after it was opened. Compare the versions before choosing whether to overwrite it.

### A `.ccdb` package cannot be imported

Possible causes:

- Incorrect password.
- Damaged or incomplete package.
- The selected file is not a valid Codebase Cartographer database package.
- Insufficient write permissions for the application data directory.

### Metrics did not change after editing

Saving a file does not automatically rerun the complete project analysis. Start the analysis again.

<br>

---

<br>

## Development

### Recommended development setup

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
python -m pip install --upgrade pip
pip install customtkinter cryptography
```

Run a syntax compilation check:

```bash
python -m py_compile codebase_cartographer.py
```

Run the application:

```bash
python codebase_cartographer.py
```

### Suggested repository files

```text
codebase-cartographer/
├── codebase_cartographer.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── screenshots/
```

Suggested `.gitignore` entries:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/
build/
dist/
*.sqlite3
*.sqlite3-wal
*.sqlite3-shm
*.ccdb
```


### Recommended future improvements

- Move the single-file implementation into focused modules.
- Add automated unit and integration tests.
- Add configurable thresholds through the UI.
- Add CSV and HTML report exports.
- Add syntax highlighting to the editor.
- Add a project dependency graph.
- Add change comparison between archived scans.
- Add ignore-pattern configuration.
- Add packaging for Windows, Linux, and macOS.
- Add CI workflows for linting, tests, and releases.

<br>

---

<br>

## Contributing

Contributions should be focused, traceable, and tested.

1. Fork the repository.
2. Create a feature branch.
3. Implement the change with clear naming and documentation.
4. Verify that the application starts and the affected workflows operate correctly.
5. Add or update tests where available.
6. Update this README when behavior, dependencies, security properties, or user workflows change.
7. Submit a pull request with a precise description of the change.

Example branch name:

```text
feature/configurable-analysis-thresholds
```

Example commit message:

```text
feat: add configurable complexity thresholds
```

For security-sensitive issues, avoid publishing exploit details in a public issue before the maintainer has had an opportunity to review them.

<br>

---

<br>

## License

The application declares the **MIT License**.

A repository should include a complete [LICENSE](LICENSE) file containing the official MIT License text and the applicable copyright notice.

<br>

---

<br>

## Author and Copyright

**Codebase Cartographer**  
Copyright © 2026 Thorsten Bylicki / BylickiLabs

[Github](https://github.com/bylickilabs)


<br>

---
---

<br>

# German

## Überblick

Codebase Cartographer ist eine zweisprachige Desktop-Anwendung zur statischen Analyse von Python-Projekten. Die Anwendung verwendet den abstrakten Syntaxbaum von Python (`ast`) und muss den analysierten Projektcode daher weder importieren noch ausführen.

Die Software richtet sich an Entwickler, Maintainer, Reviewer, Lehrende und Teams, die sich schnell einen strukturierten Überblick über eine unbekannte oder wachsende Python-Codebasis verschaffen möchten. Analyse, Qualitätsindikatoren, Befunde, Quelltextbearbeitung, Berichtserstellung und historische Archivierung werden in einer lokalen Benutzeroberfläche zusammengeführt.

### Zentrale Zielsetzungen

- Schneller struktureller Überblick über Python-Projekte.
- Erkennung möglicher Wartungs- und Dokumentationsrisiken.
- Darstellung und Klassifizierung von Abhängigkeiten.
- Frühe Erkennung von Syntaxfehlern.
- Lokale Kontrolle über Quellcode und Analyseergebnisse.
- Dauerhafte Speicherung abgeschlossener Analysen.
- Direkte Bearbeitung ausgewählter Projektdateien.
- Exportierbare Berichte für Dokumentation und Reviews.

> [!IMPORTANT]
> Codebase Cartographer liefert heuristische Kennzahlen und statische Befunde. Die Anwendung ersetzt keine Tests, Sicherheitsaudits, Typprüfung, Laufzeitanalyse, professionellen Code-Review oder spezialisierte Qualitätssicherungswerkzeuge.

<br>

---

<br>

## Hauptfunktionen

### Lokale statische Analyse

- Rekursive Erkennung von Python-Dateien.
- Analyse des Quellcodes mit dem Python-Modul `ast`.
- Kein Import und keine Ausführung analysierter Projektmodule.
- Ermittlung von Gesamt-, Code-, Kommentar- und Leerzeilen.
- Erkennung von Syntaxfehlern einschließlich Zeile und Spalte.
- Extraktion von Modulen, Klassen, Funktionen, asynchronen Funktionen und Methoden.
- Erfassung von Position, übergeordnetem Symbol, Docstring, Komplexität und Verschachtelung.
- Extraktion von Importen und importierten Namen.
- Klassifizierung von Importen als Standardbibliothek, extern, lokal, relativ oder unbekannt.
- Erkennung von Wildcard-Importen.
- Erkennung von `TODO`, `FIXME`, `HACK` und `XXX`.

### Wartbarkeitsindikatoren

- Komplexität auf Dateiebene.
- Komplexität einzelner Symbole.
- Maximale Verschachtelungstiefe.
- Erkennung sehr großer Dateien.
- Fehlende Modul-Docstrings.
- Fehlende Docstrings öffentlicher Symbole.
- Wiederholte öffentliche Symbolnamen in mehreren Dateien.
- Priorisierte Befunde von informativ bis kritisch.
- Berechnete Dokumentationsquote und Qualitätsindex.

### Desktop-Oberfläche

- Moderne Benutzeroberfläche mit CustomTkinter.
- Dunkle, helle und systemabhängige Darstellung.
- Umschaltung zwischen Deutsch und Englisch während der Laufzeit.
- Dashboard mit Projektkennzahlen.
- Filterbare Datei-, Struktur- und Befundansichten.
- Übersicht der Abhängigkeiten.
- Ausführliche Berichtsdarstellung.
- Plattformübergreifendes Öffnen des Projektordners.
- Analyse in einem Hintergrund-Thread für eine reaktionsfähige Oberfläche.

### Editor, Berichte und Archivierung

- Integrierter UTF-8-Quelltexteditor.
- Öffnen von Dateien per Doppelklick oder `Enter`.
- Speichern, Speichern unter, Neuladen, Suchen, Ersetzen, Zeilensprung, Rückgängig und Wiederholen.
- Erkennung extern veränderter Dateien vor dem Überschreiben.
- Export von JSON- und Markdown-Berichten.
- Automatische Speicherung jeder abgeschlossenen Analyse in SQLite.
- Benutzerdefinierte Projekt- oder Analysemitteilung mit maximal 1.000 Zeichen.
- Laden, Löschen, Aktualisieren und Exportieren archivierter Scans.
- Passwortgeschützter Export und Import der vollständigen Datenbank.

<br>

---

<br>

## Analyseumfang

Codebase Cartographer analysiert derzeit Dateien mit folgender Erweiterung:

```text
.py
```

Für jede geeignete Python-Datei können folgende Informationen ermittelt werden:

| Bereich | Erfasste Informationen |
|---|---|
| Datei | Absoluter Pfad, relativer Pfad, Modulname, Größe, Zeilenzahlen, Status |
| Struktur | Klassen, Funktionen, Async-Funktionen und Methoden |
| Symbole | Name, Typ, Startzeile, Endzeile, übergeordnetes Symbol, Docstring, Komplexität, Verschachtelung |
| Importe | Modul, importierte Namen, Zeile, Kategorie, Wildcard-Status |
| Dokumentation | Modul-Docstring und Docstrings öffentlicher Symbole |
| Wartung | TODO-, FIXME-, HACK- und XXX-Markierungen |
| Komplexität | Dateikomplexität, Symbolkomplexität, maximale Verschachtelung |
| Fehler | Python-Syntaxfehler und Gründe für übersprungene Dateien |

### Importkategorien

| Kategorie | Bedeutung |
|---|---|
| `standard_library` | Das Stammmodul gehört zur Python-Standardbibliothek. |
| `external` | Das Modul wurde weder als Standardbibliothek noch als lokales Modul erkannt. |
| `local` | Das Stammmodul entspricht einem erkannten Projektmodul. |
| `relative` | Der Import verwendet mindestens einen führenden Punkt. |
| `unknown` | Das Modul kann nicht zuverlässig klassifiziert werden. |

> [!NOTE]
> Die Importklassifizierung ist bewusst leichtgewichtig. Virtuelle Umgebungen, installierte Distributionen, Namespace-Packages, dynamische Importe und sämtliche denkbaren Paketstrukturen werden nicht vollständig aufgelöst.

<br>

---

<br>

## Befunde und Grenzwerte

Die Standardgrenzwerte sind direkt in der Anwendung definiert und können durch Entwickler angepasst werden.

| Einstellung | Standardwert | Auswirkung |
|---|---:|---|
| Maximale Dateigröße | 3.000.000 Byte | Größere Python-Dateien werden übersprungen. |
| Grenzwert für große Dateien | 500 Zeilen | Erzeugt einen Wartbarkeitsbefund. |
| Hohe Dateikomplexität | 25 | Erzeugt einen Dateikomplexitätsbefund. |
| Hohe Symbolkomplexität | 10 | Erzeugt einen Symbolkomplexitätsbefund. |
| Tiefe Verschachtelung | 5 Ebenen | Erzeugt einen Verschachtelungsbefund. |
| Benutzerdefinierte Meldung | 1.000 Zeichen | Längere Meldungen können nicht gespeichert werden. |

### Prioritäten der Befunde

| Priorität | Typische Bedeutung |
|---|---|
| `critical` | Grundlegendes Problem, beispielsweise ein Syntaxfehler. |
| `high` | Deutliches Wartbarkeitsrisiko mit Handlungsbedarf. |
| `medium` | Relevanter Sachverhalt, der geprüft werden sollte. |
| `low` | Kleineres Qualitäts-, Dokumentations- oder Wartungsthema. |
| `info` | Architektonischer Hinweis ohne direkten Punktabzug. |

### Erkannte Befundarten

- Datei aufgrund des Größenlimits übersprungen.
- Python-Syntaxfehler.
- Sehr große Quelldatei.
- Hohe Dateikomplexität.
- Komplexe Klasse, Funktion, Async-Funktion oder Methode.
- Tiefe Verschachtelung.
- Fehlender Modul-Docstring.
- Öffentliche Symbole ohne Docstring.
- Offene TODO-, FIXME-, HACK- oder XXX-Markierungen.
- Wildcard-Import.
- Öffentlicher Symbolname in mindestens drei verschiedenen Dateien.

### Komplexitätsberechnung

Der integrierte Visitor beginnt mit einer Basiskomplexität von `1` und erhöht den Wert unter anderem für:

- `if`
- `for` und `async for`
- `while`
- `try`
- `with` und `async with`
- bedingte Ausdrücke
- Assertions
- Comprehensions
- `match`
- Exception-Handler
- zusätzliche boolesche Operanden

Die Berechnung ist eine praxisorientierte Heuristik in Anlehnung an zyklomatische Komplexität. Die Ergebnisse müssen nicht mit Radon, Ruff, SonarQube oder anderen Analysewerkzeugen übereinstimmen.

<br>

---

<br>

## Qualitätsindex

Das Dashboard berechnet einen Qualitätsindex zwischen `0` und `100`.

### Abzüge nach Priorität

| Priorität | Abzug pro Befund |
|---|---:|
| Kritisch | 18 |
| Hoch | 9 |
| Mittel | 4 |
| Niedrig | 1 |
| Info | 0 |

### Dokumentationskomponente

Die Dokumentationsquote setzt sich zusammen aus:

- **70 %** Dokumentationsquote öffentlicher Symbole.
- **30 %** Dokumentationsquote der Module.

Die resultierende Dokumentationsquote kann einen Bonus von maximal 15 Punkten beitragen. Das Endergebnis wird anschließend auf den Wertebereich von 0 bis 100 begrenzt.

Vereinfacht:

```text
Qualitätsindex = Begrenzung(100 - Befundabzüge + Dokumentationsbonus, 0, 100)
```

> [!CAUTION]
> Der Qualitätsindex dient der Projektorientierung. Er ist keine objektive Zertifizierung von Quellcodequalität oder Sicherheit.

<br>

---

<br>

## Integrierter Quelltexteditor

Der integrierte Editor öffnet Dateien der aktuellen Analyse direkt aus der Seite **Dateien**.

### Datei öffnen

- Dateizeile doppelt anklicken.
- Dateizeile auswählen und `Enter` drücken.

### Editorfunktionen

- Aktuelle Datei speichern.
- Inhalt unter einem anderen Pfad speichern.
- Datei vom Datenträger neu laden.
- Text suchen.
- Text ersetzen.
- Zu einer bestimmten Zeile springen.
- Gesamten Inhalt auswählen.
- Änderungen rückgängig machen und wiederholen.
- Anzeige von Zeile, Spalte, Kodierung und Zeichenzahl.
- Warnung vor ungespeicherten Änderungen beim Schließen.
- Erkennung externer Dateiänderungen.
- Bestätigung vor dem Überschreiben der Originaldatei im Projektverzeichnis.

Der Editor liest und schreibt UTF-8-Text. Nach dem Speichern muss die Projektanalyse erneut gestartet werden, damit Kennzahlen und Befunde aktualisiert werden.

> [!WARNING]
> Der Editor kann Originaldateien des Projekts überschreiben. Wichtige Änderungen sollten zuvor versioniert oder gesichert werden.

<br>

---

<br>

## SQLite-Analysearchiv

Jede erfolgreich abgeschlossene Analyse wird automatisch in einer lokalen SQLite-Datenbank gespeichert.

### Standardpfad der Datenbank

```text
~/.codebase_cartographer/codebase_cartographer.sqlite3
```

Unter Windows verweist `~` normalerweise auf das Profilverzeichnis des aktuellen Benutzers.

### Gespeicherte Analysedaten

- Scan-ID.
- Projektpfad.
- Analysezeitpunkt.
- Benutzerdefinierte Meldung.
- Anzahl der Dateien.
- Anzahl der Befunde.
- Qualitätsindex.
- Vollständige serialisierte Analyse.
- Anwendungsversion.
- Erstellungszeitpunkt des Datenbankeintrags.

### Archivfunktionen

- Gespeicherte Scans anzeigen.
- Archivansicht aktualisieren.
- Ausgewählten Scan in die Oberfläche laden.
- Scan per Doppelklick öffnen.
- Ausgewählten Scan dauerhaft löschen.
- Einzelnen Scan als JSON exportieren.
- Einzelnen Scan als Markdown exportieren.
- Gesamte Datenbank als passwortgeschütztes `.ccdb`-Paket exportieren.
- Passwortgeschütztes `.ccdb`-Paket importieren.

SQLite wird mit Fremdschlüsselprüfung, Write-Ahead Logging und normalem Synchronisationsmodus betrieben.

<br>

---

<br>

## Verschlüsselte Datenbankpakete

Vollständige Datenbankexporte verwenden das anwendungsspezifische `.ccdb`-Format.

### Kryptografisches Verfahren

- Verschlüsselung: **AES-256-GCM**.
- Schlüsselableitung: **PBKDF2-HMAC-SHA-256**.
- Abgeleitete Schlüssellänge: 32 Byte.
- PBKDF2-Iterationen: 390.000.
- Zufälliger Salt: 16 Byte.
- Zufällige Nonce: 12 Byte.
- Authentifizierung: Bestandteil von AES-GCM.
- Der Paketkopf wird als zusätzliche authentifizierte Information einbezogen.

### Verhalten beim Import

Bevor eine importierte Datenbank die lokale Datenbank ersetzt:

1. Das aktuelle SQLite-WAL wird in die Datenbank übertragen.
2. Eine temporäre Sicherung der bestehenden Datenbank wird erstellt.
3. Der Paketkopf der `.ccdb`-Datei wird geprüft.
4. Das Paket wird mit dem eingegebenen Passwort entschlüsselt.
5. SQLite führt eine Integritätsprüfung der temporären Datenbank durch.
6. Die geprüfte Datenbank ersetzt die aktive Datenbank.
7. Bei einem Fehler wird die Sicherung wiederhergestellt.

> [!IMPORTANT]
> Passwörter können nicht wiederhergestellt werden. Ohne das korrekte Passwort kann ein verschlüsseltes `.ccdb`-Paket nicht durch die Anwendung entschlüsselt werden.

<br>

---

<br>

## Datenschutz und Sicherheit

### Lokale Verarbeitung

Die Analyse erfolgt auf lokalen Dateien. Die Anwendung enthält keine Funktion, die Quellcode, Projektdateien, Berichte oder Datenbankeinträge an einen externen Analysedienst überträgt.

### Lokal verbleibende Daten

- Ausgewählter Projektpfad.
- Quellcodeanalyse.
- Erzeugte Befunde.
- Berichte, solange der Benutzer sie nicht exportiert oder verschiebt.
- SQLite-Archiv.
- Benutzerdefinierte Meldungen.

### Wichtige Sicherheitsabgrenzung

- Die reguläre SQLite-Datenbank unter `~/.codebase_cartographer/codebase_cartographer.sqlite3` wird als normale lokale SQLite-Datei gespeichert.
- Die passwortbasierte AES-256-GCM-Verschlüsselung gilt für exportierte `.ccdb`-Pakete.
- Der Quelltexteditor kann Originaldateien verändern.
- Die GitHub-Schaltfläche öffnet das konfigurierte BylickiLabs-Profil im Standardbrowser.

Der Benutzer ist für Betriebssystemberechtigungen, Datenträgerverschlüsselung, Sicherungen, Passwortverwaltung und den Schutz des lokalen Benutzerkontos verantwortlich.

<br>

---

<br>

## Systemanforderungen

### Erforderlich

- Python **3.10 oder neuer**.
- Tk-Unterstützung für die verwendete Python-Installation.
- Grafische Desktop-Umgebung.
- Leserechte für das zu analysierende Projekt.
- Schreibrechte für Editor-Speicherungen, Exporte und das lokale Datenbankverzeichnis.

### Python-Pakete

```text
customtkinter
cryptography
```

Alle weiteren importierten Module gehören zur Python-Standardbibliothek.

### Plattformhinweise

| Plattform | Hinweise |
|---|---|
| Windows | Python von python.org enthält Tk normalerweise bereits. Projektordner werden über die Windows-Shell geöffnet. |
| Linux | Tk muss gegebenenfalls als separates Distributionspaket installiert werden. Ordner werden mit `xdg-open` geöffnet. |
| macOS | Tk muss für Python verfügbar sein. Ordner werden mit dem Befehl `open` geöffnet. |

<br>

---

<br>

## Installation auf Deutsch

### 1. Repository klonen

```bash
git clone https://github.com/bylickilabs/codebase_cartographer.git
cd codebase_cartographer
```

`codebase_cartographer` muss durch den tatsächlichen Repository-Namen ersetzt werden.

### 2. Virtuelle Umgebung erstellen

#### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows-Eingabeaufforderung

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux oder macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. pip aktualisieren

```bash
python -m pip install --upgrade pip
```

### 4. Abhängigkeiten installieren

```bash
pip install customtkinter cryptography
```

Empfohlene `requirements.txt`:

```text
customtkinter
cryptography
```

Installation über die Datei:

```bash
pip install -r requirements.txt
```

### Linux: Tk bei Bedarf installieren

Beispiel für Debian oder Ubuntu:

```bash
sudo apt update
sudo apt install python3-tk
```

Der genaue Paketname ist von der jeweiligen Linux-Distribution abhängig.

<br>

---

<br>

## Anwendung starten

Sofern die Anwendungsdatei `codebase_cartographer.py` heißt:

```bash
python codebase_cartographer.py
```

Unter Windows kann alternativ verwendet werden:

```powershell
py codebase_cartographer.py
```

Das Programm startet die Klasse `CompleteCodebaseCartographerApplication` und öffnet die grafische Oberfläche.

<br>

---

<br>

## Bedienung

### Projekt analysieren

1. Codebase Cartographer starten.
2. **Projekt auswählen** anklicken.
3. Einen vorhandenen Python-Projektordner auswählen.
4. **Analyse starten** anklicken.
5. Übersicht, Dateien, Struktur, Abhängigkeiten, Befunde und Bericht prüfen.
6. Optional eine benutzerdefinierte Meldung mit maximal 1.000 Zeichen erfassen.
7. Die Meldung speichern, nachdem ein Scan erstellt wurde.

### Projektdatei bearbeiten

1. Seite **Dateien** öffnen.
2. Datei auswählen.
3. Datei doppelt anklicken oder `Enter` drücken.
4. Änderungen vornehmen.
5. Speichern oder **Speichern unter** verwenden.
6. Analyse erneut starten, um sämtliche Kennzahlen zu aktualisieren.

### Archivierten Scan laden

1. Seite **Datenbank** öffnen.
2. Scan auswählen.
3. **Scan laden** anklicken oder den Archiveintrag doppelt anklicken.
4. Wiederhergestellte Analyse und Meldung prüfen.

### Verschlüsseltes Datenbankpaket exportieren

1. Seite **Datenbank** öffnen.
2. **Datenbank exportieren** auswählen.
3. Zielpfad mit der Endung `.ccdb` festlegen.
4. Ein starkes Passwort eingeben und bestätigen.
5. Passwort getrennt und sicher aufbewahren.

### Verschlüsseltes Datenbankpaket importieren

1. Seite **Datenbank** öffnen.
2. **Datenbank importieren** auswählen.
3. Bestätigen, dass die lokale Datenbank ersetzt werden darf.
4. `.ccdb`-Paket auswählen.
5. Zugehöriges Passwort eingeben.
6. Entschlüsselung und SQLite-Integritätsprüfung abschließen lassen.

<br>

---

<br>

## Benutzeroberfläche

| Seite | Zweck |
|---|---|
| Übersicht | Zeigt Kennzahlen, Projektinformationen, häufige Abhängigkeiten, komplexe Dateien und die benutzerdefinierte Meldung. |
| Dateien | Listet Dateien mit Größe, Zeilen, Symbolen, Importen, Komplexität und Status auf. |
| Struktur | Zeigt Klassen, Funktionen, Async-Funktionen und Methoden mit Position und Dokumentationsstatus. |
| Abhängigkeiten | Aggregiert importierte Module, Kategorien, Häufigkeiten und verwendende Dateien. |
| Befunde | Zeigt priorisierte Befunde, Beschreibungen, Dateipositionen und Empfehlungen. |
| Bericht | Zeigt den erzeugten Bericht und ermöglicht JSON- und Markdown-Exporte. |
| Datenbank | Zeigt archivierte Scans und stellt Archiv-, Scan-Export-, Datenbankexport- und Datenbankimportfunktionen bereit. |

### Globale Bedienelemente

- Projekt auswählen.
- Analyse starten.
- Projektordner öffnen.
- Zwischen Deutsch und Englisch wechseln.
- Darstellungsmodus wechseln.
- BylickiLabs-GitHub-Seite öffnen.
- Anwendungsinformationen anzeigen.

<br>

---

<br>

## Exportformate auf Deutsch

### JSON-Bericht

Die JSON-Darstellung enthält je nach Export Anwendungsmetadaten, Projektinformationen, Summen, Dateien, Symbole, Importe, Befunde, Archivinformationen und die benutzerdefinierte Meldung.

JSON eignet sich für:

- Automatisierte Weiterverarbeitung.
- Zusätzliche Berichte.
- Datenmigration.
- Integration in interne Werkzeuge.
- Strukturierte Langzeitablage.

### Markdown-Bericht

Der Markdown-Bericht bietet eine lesbare Projektzusammenfassung für:

- GitHub-Issues.
- Pull Requests.
- Projektdokumentation.
- Review-Notizen.
- Interne technische Berichte.

Der erweiterte Bericht enthält zusätzlich die benutzerdefinierte Meldung und die Scan-ID.

### `.ccdb`-Datenbankpaket

Eine `.ccdb`-Datei enthält eine verschlüsselte Kopie der vollständigen lokalen SQLite-Datenbank. Das Format dient der Sicherung oder Übertragung zwischen Installationen von Codebase Cartographer.

<br>

---

<br>

## Ausgeschlossene Verzeichnisse und Dateigrenzen

Der rekursive Scanner schließt versteckte Verzeichnisse sowie standardmäßig folgende Verzeichnisnamen aus:

```text
.git
.github
.hg
.svn
.idea
.vscode
.venv
venv
env
__pycache__
.pytest_cache
.mypy_cache
.ruff_cache
.tox
.nox
node_modules
site-packages
dist
build
```

Andere Nicht-Python-Dateien werden als ignorierte Dateien gezählt, jedoch nicht analysiert.

Python-Dateien mit mehr als `3.000.000` Byte werden als übersprungen erfasst und erzeugen einen Befund mit niedriger Priorität.

<br>

---

<br>

## Projektarchitektur

Die aktuelle Implementierung ist als Single-File-Desktop-Anwendung aufgebaut. Die Verantwortlichkeiten sind intern durch Datenklassen, AST-Visitor, Hilfsfunktionen, UI-Komponenten, Persistenzdienste und spezialisierte Fenster getrennt.

### Zentrale Komponenten

| Komponente | Verantwortung |
|---|---|
| `SymbolInformation` | Speichert Informationen zu einem erkannten Codesymbol. |
| `ImportInformation` | Speichert Informationen zu einem Import. |
| `Finding` | Repräsentiert einen priorisierten Analysebefund. |
| `FileAnalysis` | Enthält sämtliche Kennzahlen einer Datei. |
| `ProjectAnalysis` | Bündelt Projektergebnisse und berechnet Gesamtsummen. |
| `ComplexityVisitor` | Berechnet heuristische Komplexitäts- und Verschachtelungswerte. |
| `PythonStructureVisitor` | Extrahiert Klassen, Funktionen, Methoden und Importe aus dem AST. |
| Analysefunktionen | Erkennen Dateien, parsen Quellcode, zählen Zeilen, finden Markierungen und erzeugen Befunde. |
| `ModernTreeview` | Stellt wiederverwendbare Tabellenansichten mit Scrollbars bereit. |
| `MetricCard` | Zeigt Kennzahlen im Dashboard. |
| `CodebaseCartographerApplication` | Implementiert die grundlegende Analyseoberfläche und Berichtsfunktionen. |
| Serialisierungsfunktionen | Wandeln Analysen in JSON-kompatible Daten um und wieder zurück. |
| `CodebaseDatabaseManager` | Erstellt und verwaltet das SQLite-Archiv. |
| Kryptografiefunktionen | Leiten Schlüssel ab und importieren oder exportieren geschützte Datenbankpakete. |
| `DatabasePasswordDialog` | Erfasst Passwörter für Datenbankpakete. |
| `SourceCodeEditorWindow` | Implementiert die integrierte Dateibearbeitung. |
| `CompleteCodebaseCartographerApplication` | Verbindet Analyse, Editor, Meldungen und Datenbankarchiv. |

### Analyseablauf

```text
Projekt auswählen
    ↓
Geeignete Python-Dateien erkennen
    ↓
Projektmodule erfassen
    ↓
Dateien lesen und parsen
    ↓
Symbole und Importe extrahieren
    ↓
Zeilen, Komplexität, Verschachtelung und Dokumentation ermitteln
    ↓
Priorisierte Befunde erzeugen
    ↓
Gesamtsummen und Qualitätsindex berechnen
    ↓
Ansichten und Berichte darstellen
    ↓
Abgeschlossene Analyse automatisch in SQLite archivieren
```

<br>

---

<br>

## Datenmodell

### `ProjectAnalysis`

Eine Projektanalyse enthält:

- Projektpfad.
- Erstellungszeitpunkt.
- Liste der Dateianalysen.
- Liste der Befunde.
- Anzahl ignorierter Dateien.
- Konfiguration ausgeschlossener Verzeichnisse.

### `FileAnalysis`

Eine Dateianalyse enthält:

- Absoluten und relativen Pfad.
- Modulnamen.
- Dateigröße.
- Gesamt-, Code-, Kommentar- und Leerzeilen.
- Status des Modul-Docstrings.
- Symbole.
- Importe.
- TODO-ähnliche Markierungen.
- Komplexität.
- Maximale Verschachtelung.
- Syntaxfehler oder Grund für das Überspringen.

### SQLite-Schema

Die Tabelle `project_scans` speichert:

```sql
id
project_path
generated_at
custom_message
file_count
finding_count
quality_score
payload_json
application_version
created_at
```

Für Projektpfad und Analysezeitpunkt werden Indizes angelegt.

<br>

---

<br>

## Einschränkungen

- Es werden ausschließlich `.py`-Dateien analysiert.
- Die Analyse ist statisch und untersucht kein Laufzeitverhalten.
- Dynamische Importe können unentdeckt bleiben.
- Die Importklassifizierung ist heuristisch.
- Die Zeilenzählung bildet die vollständige Python-Tokenisierung nicht exakt ab.
- Mehrzeilige Zeichenketten einschließlich Docstrings werden als Code gezählt.
- Komplexitätswerte sind anwendungsspezifische Heuristiken.
- Doppelte Symbolnamen werden anhand öffentlicher Namen in mindestens drei Dateien erkannt.
- Die Anwendung erstellt keinen vollständigen Aufruf- oder Abhängigkeitsgraphen.
- Vererbung, Decorators, Typaliasse, generierter Code und Monkey Patching werden nicht tiefgreifend aufgelöst.
- Ruff, Flake8, Pylint, MyPy, Pyright, Bandit, pytest, Coverage-Werkzeuge und spezialisierte Sicherheitsscanner werden nicht ersetzt.
- Der Editor ist ein funktionaler Texteditor, jedoch keine vollständige IDE und kein Language-Server-Client.
- Pfade archivierter Scans können auf Dateien verweisen, die später verschoben, umbenannt oder gelöscht wurden.
- Die lokale SQLite-Datenbank wird durch die Anwendung nicht im Ruhezustand verschlüsselt.

<br>

---

<br>

## Fehlerbehebung

### `CustomTkinter wurde nicht gefunden`

Die Abhängigkeit muss in derselben Python-Umgebung installiert werden, mit der die Anwendung gestartet wird:

```bash
python -m pip install customtkinter
```

### `Die Erweiterung 'cryptography' wurde nicht gefunden`

```bash
python -m pip install cryptography
```

### `No module named tkinter`

Das Tk-Paket des Betriebssystems installieren. Beispiel für Debian oder Ubuntu:

```bash
sudo apt install python3-tk
```

### Anwendung verwendet die falsche Python-Umgebung

Python-Version und installierte Pakete prüfen:

```bash
python --version
python -m pip show customtkinter cryptography
```

### Eine Datei fehlt in der Analyse

Folgende Punkte prüfen:

- Die Datei endet auf `.py`.
- Die Datei liegt nicht in einem ausgeschlossenen oder versteckten Verzeichnis.
- Die Datei überschreitet nicht die maximale Dateigröße.
- Der richtige Projektordner wurde ausgewählt.

### Eine Datei enthält einen Syntaxfehler

Die gemeldete Zeile und Spalte im integrierten Editor oder in einer IDE korrigieren. Weitere Strukturkennzahlen dieser Datei gelten erst nach der Korrektur als vollständig belastbar.

### Der Editor meldet eine externe Dateiänderung

Ein anderer Prozess hat die Datei nach dem Öffnen verändert. Vor dem Überschreiben sollten beide Versionen verglichen werden.

### Ein `.ccdb`-Paket kann nicht importiert werden

Mögliche Ursachen:

- Falsches Passwort.
- Beschädigtes oder unvollständiges Paket.
- Die ausgewählte Datei ist kein gültiges Codebase-Cartographer-Datenbankpaket.
- Fehlende Schreibrechte für das Anwendungsdatenverzeichnis.

### Kennzahlen ändern sich nach dem Speichern nicht

Das Speichern einer Datei startet nicht automatisch eine vollständige Projektanalyse. Die Analyse muss erneut ausgeführt werden.

<br>

---

<br>

## Entwicklung

### Empfohlene Entwicklungsumgebung

```bash
python -m venv .venv
```

Umgebung aktivieren und Abhängigkeiten installieren:

```bash
python -m pip install --upgrade pip
pip install customtkinter cryptography
```

Syntaxprüfung durchführen:

```bash
python -m py_compile codebase_cartographer.py
```

Anwendung starten:

```bash
python codebase_cartographer.py
```

### Empfohlene Repository-Dateien

```text
codebase-cartographer/
├── codebase_cartographer.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── screenshots/
```

Empfohlene `.gitignore`-Einträge:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
env/
.pytest_cache/
.mypy_cache/
.ruff_cache/
build/
dist/
*.sqlite3
*.sqlite3-wal
*.sqlite3-shm
*.ccdb
```

### Empfohlene Weiterentwicklungen

- Single-File-Implementierung in fachlich getrennte Module aufteilen.
- Automatisierte Unit- und Integrationstests ergänzen.
- Grenzwerte über die Benutzeroberfläche konfigurierbar machen.
- CSV- und HTML-Berichte ergänzen.
- Syntaxhervorhebung in den Editor integrieren.
- Abhängigkeitsgraphen ergänzen.
- Unterschiede zwischen archivierten Scans darstellen.
- Konfigurierbare Ignore-Muster bereitstellen.
- Installationspakete für Windows, Linux und macOS erstellen.
- CI-Workflows für Linting, Tests und Releases ergänzen.

<br>

---

<br>

## Mitwirken

Beiträge sollten klar abgegrenzt, nachvollziehbar und geprüft sein.

1. Repository forken.
2. Feature-Branch erstellen.
3. Änderung mit klaren Bezeichnungen und Dokumentation umsetzen.
4. Startfähigkeit und betroffene Abläufe prüfen.
5. Vorhandene Tests erweitern oder neue Tests ergänzen.
6. README aktualisieren, wenn sich Verhalten, Abhängigkeiten, Sicherheitsmerkmale oder Bedienabläufe ändern.
7. Pull Request mit präziser Beschreibung erstellen.

Beispiel für einen Branch-Namen:

```text
feature/configurable-analysis-thresholds
```

Beispiel für eine Commit-Nachricht:

```text
feat: add configurable complexity thresholds
```

Sicherheitsrelevante Schwachstellen sollten nicht sofort mit vollständigen Exploitdetails in einem öffentlichen Issue veröffentlicht werden.

<br>

---

<br>

## Lizenz auf Deutsch

Die Anwendung weist die **MIT-Lizenz** aus.

Das Repository sollte eine vollständige Datei [LICENSE](LICENSE) mit dem offiziellen Text der MIT-Lizenz und dem zutreffenden Urheberrechtshinweis enthalten.

<br>

---

<br>

## Autor und Urheberrecht

**Codebase Cartographer**  
Copyright © 2026 Thorsten Bylicki / BylickiLabs

[Github](https://github.com/bylickilabs)
