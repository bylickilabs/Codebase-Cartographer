# Architecture

## English

### Overview

Codebase Cartographer is a local-first Python desktop application for static source-code analysis. It combines project discovery, AST parsing, software metrics, findings, report generation, a dedicated source-code editor, and a persistent SQLite scan archive in one graphical workflow.

No analyzed source code must be uploaded to an external analysis service. Project files are read, parsed, evaluated, displayed, edited, and archived on the local system.



<br>

---

<br>

### Architectural layers

1. **Presentation layer** — CustomTkinter, Tkinter, and ttk provide navigation, dashboards, tables, filters, dialogs, status information, archive management, and editor windows.
2. **Application layer** — The main application coordinates project selection, background scans, localization, rendering, editor actions, exports, and database operations.
3. **Analysis layer** — Python files are discovered, read, parsed with `ast`, and transformed into structured file, symbol, import, and finding records.
4. **Persistence layer** — Completed analyses are serialized and stored in SQLite.
5. **Security and export layer** — Reports and password-protected database packages are created and imported.



<br>

---

<br>

### Core data model

The analysis model uses dataclasses:

- `SymbolInformation` stores name, symbol type, line range, parent, docstring state, complexity, and maximum nesting.
- `ImportInformation` stores module, imported names, source line, category, and wildcard status.
- `Finding` stores severity, category, translation keys, file, line, and details.
- `FileAnalysis` stores file metadata, line metrics, module information, symbols, imports, TODO markers, complexity, syntax errors, and skip reasons.
- `ProjectAnalysis` combines project metadata, all analyzed files, findings, ignored-file count, and excluded directories.

`ProjectAnalysis.totals()` calculates project-wide metrics such as files, code lines, classes, functions, imports, findings, documentation coverage, quality score, syntax errors, TODO markers, and ignored files.



<br>

---

<br>

### Main classes

#### `ComplexityVisitor`

Traverses AST nodes, counts selected branch and control-flow structures, and tracks maximum nesting depth.

#### `PythonStructureVisitor`

Extracts classes, functions, asynchronous functions, methods, imports, parent relationships, docstrings, complexity, and nesting.

#### `ModernTreeview`

Wraps `ttk.Treeview` inside a CustomTkinter frame and adds headings, scrollbars, insertion, clearing, and tag formatting.

#### `MetricCard`

Displays one dashboard value with a translated title.

#### `CodebaseDatabaseManager`

Initializes and manages the SQLite archive, stores scans, updates messages, lists and loads scans, deletes records, performs WAL checkpoints, and checks integrity.

#### Main application

Coordinates the user interface, selected project, current analysis, archive record, language, worker thread, rendering, editor, and exports.



<br>

---

<br>

### Data flow

1. The user selects a project directory.
2. The scanner recursively discovers `.py` files.
3. Excluded directories and unsupported files are ignored.
4. Project module names are collected.
5. Files are checked against the size limit and read locally.
6. Line metrics and TODO markers are collected.
7. `ast.parse()` creates an abstract syntax tree.
8. Visitors extract structure, imports, complexity, and nesting.
9. Findings are generated and sorted by severity.
10. A `ProjectAnalysis` object is created.
11. The GUI renders metrics, tables, dependencies, findings, and reports.
12. The completed scan is stored in SQLite.
13. The user can edit files, export reports, or load previous scans.



<br>

---

<br>

### AST analysis

The application uses Python's built-in `ast` module and does not execute analyzed source code.

The analysis detects:

- modules, classes, functions, asynchronous functions, and methods;
- source line positions and parent relationships;
- module and symbol docstrings;
- `import` and `from ... import ...` statements;
- standard-library, external, local, relative, and unknown imports;
- wildcard imports;
- complexity and nesting;
- syntax errors.

Static analysis cannot always resolve runtime-generated imports, reflection, monkey patching, plugin loading, `eval()`, `exec()`, or dynamically generated code.



<br>

---

<br>

### Threading

Project analysis runs in a daemon worker thread so the graphical interface remains responsive. Results are returned to the Tkinter event loop with `after()`, ensuring that widget updates occur on the main GUI thread.



<br>

---

<br>

### Integrated editor

The dedicated editor opens analyzed files directly from the file view, including by double-click. It supports UTF-8 editing, save, save as, reload, find, replace, go to line, undo, redo, select all, unsaved-change checks, external-modification warnings, and status information.

After saving a file, the project must be analyzed again to refresh metrics and findings.



<br>

---

<br>

### SQLite archive

Every completed scan is serialized and stored locally. The archive preserves project path, scan time, file and finding counts, quality score, application version, custom message, and the complete analysis payload.

Scans can be listed, loaded, updated, exported, and deleted.



<br>

---

<br>

### Localization

German and English translation dictionaries cover navigation, labels, dialogs, findings, recommendations, editor functions, reports, and database controls. The language can be changed at runtime.



<br>

---

<br>

### Architectural boundaries

Codebase Cartographer is a desktop application, not a web service. It does not require a browser runtime, application server, cloud database, REST API, or remote analysis backend.

The current parser is designed for Python `.py` files. Additional languages require dedicated parsers and language-specific rules.



<br>

---
---

<br>

## German

### Überblick

Codebase Cartographer ist eine lokal arbeitende Python-Desktopanwendung zur statischen Quellcodeanalyse. Sie verbindet Projekterkennung, AST-Parsing, Softwarekennzahlen, Befunde, Berichtserstellung, einen speziell entwickelten Quellcode-Editor und ein dauerhaftes SQLite-Scanarchiv in einem grafischen Arbeitsablauf.

Analysierter Quellcode muss nicht an einen externen Dienst übertragen werden. Projektdateien werden auf dem lokalen System gelesen, geparst, bewertet, dargestellt, bearbeitet und archiviert.



<br>

---

<br>

### Architekturschichten

1. **Darstellungsschicht** — CustomTkinter, Tkinter und ttk stellen Navigation, Dashboard, Tabellen, Filter, Dialoge, Statusinformationen, Archivverwaltung und Editorfenster bereit.
2. **Anwendungsschicht** — Die Hauptanwendung koordiniert Projektauswahl, Hintergrundscans, Lokalisierung, Darstellung, Editoraktionen, Exporte und Datenbankoperationen.
3. **Analyseschicht** — Python-Dateien werden erkannt, gelesen, mit `ast` geparst und in strukturierte Datei-, Symbol-, Import- und Befundobjekte überführt.
4. **Persistenzschicht** — Abgeschlossene Analysen werden serialisiert und in SQLite gespeichert.
5. **Sicherheits- und Exportschicht** — Berichte und passwortgeschützte Datenbankpakete werden erstellt und importiert.



<br>

---

<br>

### Zentrales Datenmodell

Das Analysemodell verwendet Dataclasses:

- `SymbolInformation` speichert Name, Typ, Zeilenbereich, übergeordnetes Element, Docstring-Status, Komplexität und maximale Verschachtelung.
- `ImportInformation` speichert Modul, importierte Namen, Quellzeile, Kategorie und Wildcard-Status.
- `Finding` speichert Priorität, Kategorie, Übersetzungsschlüssel, Datei, Zeile und Details.
- `FileAnalysis` speichert Dateimetadaten, Zeilenkennzahlen, Modulstatus, Symbole, Importe, TODO-Markierungen, Komplexität, Syntaxfehler und Überspringgründe.
- `ProjectAnalysis` verbindet Projektmetadaten, Dateien, Befunde, ignorierte Dateien und ausgeschlossene Verzeichnisse.

`ProjectAnalysis.totals()` berechnet projektweite Kennzahlen wie Dateien, Codezeilen, Klassen, Funktionen, Importe, Befunde, Dokumentationsabdeckung, Qualitätsindex, Syntaxfehler und TODO-Markierungen.



<br>

---

<br>

### Hauptklassen

#### `ComplexityVisitor`

Durchläuft AST-Knoten, zählt ausgewählte Verzweigungen und Kontrollflussstrukturen und ermittelt die maximale Verschachtelung.

#### `PythonStructureVisitor`

Extrahiert Klassen, Funktionen, asynchrone Funktionen, Methoden, Importe, Elternbeziehungen, Docstrings, Komplexität und Verschachtelung.

#### `ModernTreeview`

Kapselt `ttk.Treeview` in einem CustomTkinter-Frame und ergänzt Überschriften, Scrollbars, Einfügen, Leeren und Tag-Formatierung.

#### `MetricCard`

Zeigt einen Dashboardwert mit übersetzter Bezeichnung.

#### `CodebaseDatabaseManager`

Initialisiert und verwaltet das SQLite-Archiv, speichert Scans, aktualisiert Meldungen, listet und lädt Scans, löscht Datensätze, führt WAL-Checkpoints und Integritätsprüfungen aus.

#### Hauptanwendung

Koordiniert Oberfläche, Projekt, Analyse, Archiveintrag, Sprache, Worker-Thread, Darstellung, Editor und Exporte.



<br>

---

<br>

### Datenfluss

1. Der Benutzer wählt ein Projektverzeichnis.
2. Der Scanner sucht rekursiv nach `.py`-Dateien.
3. Ausgeschlossene Verzeichnisse und nicht unterstützte Dateien werden ignoriert.
4. Projektmodule werden gesammelt.
5. Dateien werden gegen das Größenlimit geprüft und lokal gelesen.
6. Zeilenkennzahlen und TODO-Markierungen werden erfasst.
7. `ast.parse()` erstellt einen abstrakten Syntaxbaum.
8. Visitoren extrahieren Struktur, Importe, Komplexität und Verschachtelung.
9. Befunde werden erzeugt und nach Priorität sortiert.
10. Ein `ProjectAnalysis`-Objekt entsteht.
11. Die Oberfläche rendert Kennzahlen, Tabellen, Abhängigkeiten, Befunde und Berichte.
12. Der Scan wird automatisch in SQLite gespeichert.
13. Dateien können bearbeitet, Berichte exportiert und frühere Scans geladen werden.



<br>

---

<br>

### AST-Analyse

Die Anwendung verwendet das integrierte Python-Modul `ast` und führt den analysierten Quellcode nicht aus.

Erkannt werden:

- Module, Klassen, Funktionen, asynchrone Funktionen und Methoden;
- Quellzeilen und übergeordnete Strukturen;
- Modul- und Symbol-Docstrings;
- `import`- und `from ... import ...`-Anweisungen;
- Standardbibliotheks-, externe, lokale, relative und unbekannte Importe;
- Wildcard-Importe;
- Komplexität und Verschachtelung;
- Syntaxfehler.

Statische Analyse kann dynamische Importe, Reflection, Monkey Patching, Plugins, `eval()`, `exec()` oder generierten Code nicht immer vollständig auflösen.



<br>

---

<br>

### Threading

Die Projektanalyse läuft in einem Daemon-Worker-Thread, damit die Oberfläche bedienbar bleibt. Ergebnisse werden mit `after()` in den Tkinter-Ereignisloop zurückgeführt.



<br>

---

<br>

### Integrierter Editor

Der speziell entwickelte Editor öffnet analysierte Dateien direkt aus der Dateiansicht, auch per Doppelklick. Unterstützt werden UTF-8-Bearbeitung, Speichern, Speichern unter, Neuladen, Suchen, Ersetzen, Zeilensprung, Rückgängig, Wiederholen, Alles auswählen, Prüfung ungespeicherter Änderungen, Warnung vor externen Änderungen und Statusinformationen.

Nach dem Speichern muss das Projekt erneut analysiert werden.



<br>

---

<br>

### SQLite-Archiv

Jeder abgeschlossene Scan wird lokal serialisiert gespeichert. Das Archiv enthält Projektpfad, Zeitpunkt, Datei- und Befundanzahl, Qualitätsindex, Anwendungsversion, Meldung und vollständige Analysedaten.

Scans können aufgelistet, geladen, aktualisiert, exportiert und gelöscht werden.



<br>

---

<br>

### Lokalisierung

Deutsche und englische Übersetzungswörterbücher decken Navigation, Bezeichnungen, Dialoge, Befunde, Empfehlungen, Editor, Berichte und Datenbankfunktionen ab.



<br>

---

<br>

### Architekturgrenzen

Codebase Cartographer ist eine Desktopanwendung und kein Webdienst. Browserlaufzeit, Server, Cloud-Datenbank, REST-API und Remote-Backend sind nicht erforderlich.

Der aktuelle Parser ist für Python-`.py`-Dateien ausgelegt. Weitere Sprachen benötigen eigene Parser und Regeln.
