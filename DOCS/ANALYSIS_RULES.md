# Analysis Rules

## English

### Scope

Codebase Cartographer performs deterministic static checks on Python `.py` files. Findings support code review and maintenance planning but do not replace tests, runtime profiling, type checking, security audits, or domain review.



<br>

---

<br>

### Excluded directories

The recursive scan excludes common metadata, virtual-environment, dependency, cache, IDE, and build directories:

```text
.git, .github, .hg, .svn, .idea, .vscode, .venv, venv, env,
__pycache__, .pytest_cache, .mypy_cache, .ruff_cache, .tox,
.nox, node_modules, site-packages, dist, build
```

Hidden directories beginning with a dot are excluded as well.



<br>

---

<br>

### File-size limit

```text
MAX_FILE_SIZE_BYTES = 3,000,000
```

Larger files are skipped and generate a low-priority scan finding.



<br>

---

<br>

### Line metrics

The scanner records total, code, comment, and blank lines. Triple-quoted blocks count as code because they may represent docstrings or string literals.



<br>

---

<br>

### Syntax errors

`ast.parse()` is used for parsing. A syntax error generates a **critical** finding with message, line, and column. The remaining project continues to be analyzed.



<br>

---

<br>

### Large files

```text
LARGE_FILE_LINE_LIMIT = 500
```

Files with at least 500 total lines generate a **medium** maintainability finding.



<br>

---

<br>

### File complexity

```text
HIGH_FILE_COMPLEXITY_LIMIT = 25
```

- 25–44: **medium**
- 45 or higher: **high**

The score starts at 1 and increases for selected branches, loops, exception handling, context managers, comprehensions, pattern matching, boolean operations, and other control-flow structures.



<br>

---

<br>

### Symbol complexity

```text
HIGH_SYMBOL_COMPLEXITY_LIMIT = 10
```

- 10–19: **medium**
- 20 or higher: **high**

Classes, functions, asynchronous functions, and methods are evaluated individually.



<br>

---

<br>

### Nesting

```text
DEEP_NESTING_LIMIT = 5
```

A maximum nesting depth of at least 5 generates a **medium** finding. Guard clauses, helper functions, early returns, and simpler control flow are recommended.



<br>

---

<br>

### Documentation rules

A missing module docstring generates a **low** finding.

Public symbols are names that do not begin with `_`.

- fewer than 5 undocumented public symbols in a file: **low**
- 5 or more: **medium**

Documentation coverage combines 70% public-symbol coverage and 30% module coverage.



<br>

---

<br>

### TODO markers

The scanner detects:

```text
TODO
FIXME
HACK
XXX
```

Detection is case-insensitive. A file with markers generates a **low** finding containing the first line and total count.



<br>

---

<br>

### Wildcard imports

`from module import *` generates a **medium** import finding because it reduces traceability and can create name collisions.



<br>

---

<br>

### Duplicate symbol names

If the same public symbol name appears in at least three different files, an **informational** architecture finding is created. This is a review signal, not automatic proof of a defect.



<br>

---

<br>

### Import categories

Imports are classified as standard library, local/project, relative, external, or unknown. Classification is heuristic and can be affected by namespace packages, multiple source roots, runtime path changes, and editable installations.



<br>

---

<br>

### Quality index

Penalty values:

| Severity | Penalty |
|---|---:|
| Critical | 18 |
| High | 9 |
| Medium | 4 |
| Low | 1 |
| Info | 0 |

A documentation bonus equal to 15% of documentation coverage is added.

```text
score = clamp(100 - penalties + documentation bonus, 0, 100)
```

The result is rounded.



<br>

---

<br>

### Finding order

Findings are sorted by critical, high, medium, low, and info, followed by file and line.



<br>

---

<br>

### Limitations

The scanner does not fully determine runtime behavior, test success, type correctness, dependency vulnerabilities, data flow, performance bottlenecks, code coverage, dead code, dynamic imports, reflection, plugin behavior, generated code, or business correctness.



<br>

---
---

<br>

## German

### Umfang

Codebase Cartographer führt deterministische statische Prüfungen für Python-`.py`-Dateien aus. Die Befunde unterstützen Code-Review und Wartungsplanung, ersetzen aber keine Tests, Laufzeitprofile, Typprüfung, Sicherheitsanalyse oder fachliche Prüfung.



<br>

---

<br>

### Ausgeschlossene Verzeichnisse

Ausgeschlossen werden typische Metadaten-, Virtual-Environment-, Abhängigkeits-, Cache-, IDE- und Buildverzeichnisse:

```text
.git, .github, .hg, .svn, .idea, .vscode, .venv, venv, env,
__pycache__, .pytest_cache, .mypy_cache, .ruff_cache, .tox,
.nox, node_modules, site-packages, dist, build
```

Versteckte Verzeichnisse mit führendem Punkt werden ebenfalls ausgeschlossen.



<br>

---

<br>

### Dateigrößenlimit

```text
MAX_FILE_SIZE_BYTES = 3.000.000
```

Größere Dateien werden übersprungen und erzeugen einen Befund mit niedriger Priorität.



<br>

---

<br>

### Zeilenkennzahlen

Erfasst werden Gesamt-, Code-, Kommentar- und Leerzeilen. Dreifach zitierte Blöcke gelten als Code, da sie Docstrings oder Stringliterale sein können.



<br>

---

<br>

### Syntaxfehler

Geparst wird mit `ast.parse()`. Ein Syntaxfehler erzeugt einen **kritischen** Befund mit Meldung, Zeile und Spalte. Die übrigen Dateien werden weiter analysiert.



<br>

---

<br>

### Große Dateien

```text
LARGE_FILE_LINE_LIMIT = 500
```

Dateien ab 500 Gesamtzeilen erzeugen einen **mittleren** Wartbarkeitsbefund.



<br>

---

<br>

### Dateikomplexität

```text
HIGH_FILE_COMPLEXITY_LIMIT = 25
```

- 25–44: **mittel**
- ab 45: **hoch**

Der Wert beginnt bei 1 und steigt durch Verzweigungen, Schleifen, Ausnahmebehandlung, Kontextmanager, Comprehensions, Pattern Matching, boolesche Operationen und weitere Kontrollflussstrukturen.



<br>

---

<br>

### Symbolkomplexität

```text
HIGH_SYMBOL_COMPLEXITY_LIMIT = 10
```

- 10–19: **mittel**
- ab 20: **hoch**

Klassen, Funktionen, asynchrone Funktionen und Methoden werden einzeln bewertet.



<br>

---

<br>

### Verschachtelung

```text
DEEP_NESTING_LIMIT = 5
```

Eine maximale Tiefe ab 5 erzeugt einen **mittleren** Befund. Empfohlen werden Guard Clauses, Hilfsfunktionen, frühe Rückgaben und einfachere Kontrollflüsse.



<br>

---

<br>

### Dokumentationsregeln

Ein fehlender Modul-Docstring erzeugt einen **niedrigen** Befund.

Öffentliche Symbole beginnen nicht mit `_`.

- weniger als 5 undokumentierte öffentliche Symbole: **niedrig**
- mindestens 5: **mittel**

Die Dokumentationsabdeckung besteht zu 70 % aus Symbol- und zu 30 % aus Moduldokumentation.



<br>

---

<br>

### TODO-Markierungen

Erkannt werden:

```text
TODO
FIXME
HACK
XXX
```

Die Suche ignoriert Groß- und Kleinschreibung. Marker erzeugen einen **niedrigen** Befund mit erster Fundzeile und Gesamtanzahl.



<br>

---

<br>

### Wildcard-Importe

`from module import *` erzeugt einen **mittleren** Importbefund, weil Nachvollziehbarkeit sinkt und Namenskollisionen entstehen können.



<br>

---

<br>

### Doppelte Symbolnamen

Kommt derselbe öffentliche Symbolname in mindestens drei Dateien vor, entsteht ein **informativer** Architekturbefund. Dies ist ein Prüfsignal und kein automatischer Fehlernachweis.



<br>

---

<br>

### Importkategorien

Importe werden als Standardbibliothek, lokal/Projekt, relativ, extern oder unbekannt eingestuft. Namespace Packages, mehrere Source Roots, Laufzeitpfade und Editable Installs können die Einordnung beeinflussen.



<br>

---

<br>

### Qualitätsindex

Abzüge:

| Priorität | Abzug |
|---|---:|
| Kritisch | 18 |
| Hoch | 9 |
| Mittel | 4 |
| Niedrig | 1 |
| Info | 0 |

Hinzu kommt ein Dokumentationsbonus von 15 % der Abdeckung.

```text
Wert = Begrenzung(100 - Abzüge + Dokumentationsbonus, 0, 100)
```

Das Ergebnis wird gerundet.



<br>

---

<br>

### Sortierung

Befunde werden nach kritisch, hoch, mittel, niedrig und informativ sowie anschließend nach Datei und Zeile sortiert.



<br>

---

<br>

### Grenzen

Nicht vollständig bestimmt werden Laufzeitverhalten, Testerfolg, Typkorrektheit, Paketlücken, Datenfluss, Performance, Code Coverage, toter Code, dynamische Importe, Reflection, Plugins, generierter Code und fachliche Korrektheit.
