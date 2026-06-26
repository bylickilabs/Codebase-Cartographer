# Integrated Editor

## English

### Purpose

The integrated source-code editor was developed specifically for Codebase Cartographer. It allows analyzed Python files to be opened, reviewed, changed, and saved directly inside the application.

For basic review and targeted corrections, an additional external editor becomes unnecessary.



<br>

---

<br>

### Opening files

Files can be opened from the file view, including by double-clicking a table entry. The editor validates that the file exists and reports read errors.

Archived scans remain viewable even if the original project path no longer exists, but unavailable source files cannot be edited.



<br>

---

<br>

### Functions

- UTF-8 source display and editing
- Save
- Save As
- Reload
- Find
- Replace
- Go to line
- Select all
- Undo
- Redo
- Line, column, encoding, and character-count status
- Unsaved-change protection
- External-modification warnings



<br>

---

<br>

### Save

Normal Save writes to the currently opened file. Before overwriting a project file, the application requests confirmation.

After saving, the project must be scanned again. Metrics and findings are based on the last completed analysis, not directly on the unsaved editor buffer.



<br>

---

<br>

### Save As

Save As writes the current content to another path. It is suitable for copies, experimental versions, corrected exports, or preserving the original file.



<br>

---

<br>

### Unsaved changes

Closing the editor with unsaved changes triggers a prompt to save first. Reloading also asks for confirmation before discarding local changes.



<br>

---

<br>

### External modifications

The editor can detect that the source file changed outside the application. Before overwriting it, the user is warned and must confirm.

This reduces conflicts with IDEs, formatters, Git operations, build tools, and other processes, but cannot eliminate every race condition.



<br>

---

<br>

### Find and replace

Search reports matches or indicates that no match exists. Replace applies user-supplied replacement text. Replacements should be reviewed carefully because the editor does not perform semantic refactoring.



<br>

---

<br>

### Navigation

Go to line helps users open the source location referenced by a finding. The status line displays current line, column, UTF-8 reference, and character count.



<br>

---

<br>

### Recommended workflow

1. Open the affected file.
2. Review the finding and surrounding code.
3. Make a targeted correction.
4. Save the file.
5. Run the analysis again.
6. Check updated findings and metrics.
7. Run the project's tests separately.



<br>

---

<br>

### Limitations

The editor is not a complete IDE. It does not necessarily provide language-server integration, autocomplete, semantic refactoring, debugging, breakpoints, terminal integration, Git conflict resolution, test execution, or package management.



<br>

---
---

<br>

## German

### Zweck

Der integrierte Quellcode-Editor wurde speziell für Codebase Cartographer entwickelt. Analysierte Python-Dateien können direkt in der Anwendung geöffnet, geprüft, geändert und gespeichert werden.

Für grundlegende Prüfungen und gezielte Korrekturen wird ein zusätzlicher externer Editor entbehrlich.



<br>

---

<br>

### Dateien öffnen

Dateien können aus der Dateiansicht geöffnet werden, auch per Doppelklick. Der Editor prüft die Verfügbarkeit und meldet Lesefehler.

Archivierte Scans bleiben sichtbar, auch wenn das Originalprojekt nicht mehr existiert. Fehlende Quelldateien können jedoch nicht bearbeitet werden.



<br>

---

<br>

### Funktionen

- UTF-8-Anzeige und Bearbeitung
- Speichern
- Speichern unter
- Neuladen
- Suchen
- Ersetzen
- Gehe zu Zeile
- Alles auswählen
- Rückgängig
- Wiederholen
- Status für Zeile, Spalte, Kodierung und Zeichenzahl
- Schutz ungespeicherter Änderungen
- Warnung vor externen Änderungen



<br>

---

<br>

### Speichern

Speichern schreibt in die aktuell geöffnete Datei. Vor dem Überschreiben einer Projektdatei verlangt die Anwendung eine Bestätigung.

Nach dem Speichern muss erneut analysiert werden. Kennzahlen und Befunde basieren auf dem letzten vollständigen Scan.



<br>

---

<br>

### Speichern unter

Speichern unter schreibt den Inhalt an einen anderen Pfad. Das eignet sich für Kopien, Versuche, korrigierte Exporte oder zur Erhaltung der Originaldatei.



<br>

---

<br>

### Ungespeicherte Änderungen

Beim Schließen mit Änderungen fragt der Editor nach dem Speichern. Auch Neuladen erfordert eine Bestätigung, bevor Änderungen verworfen werden.



<br>

---

<br>

### Externe Änderungen

Der Editor kann erkennen, wenn eine Datei außerhalb der Anwendung geändert wurde. Vor dem Überschreiben erscheint eine Warnung.

Dies reduziert Konflikte mit IDEs, Formattern, Git, Buildtools und anderen Prozessen, verhindert aber nicht jede Race Condition.



<br>

---

<br>

### Suchen und Ersetzen

Die Suche meldet Treffer oder fehlende Ergebnisse. Ersetzen verwendet den angegebenen Ersatztext. Da keine semantische Refactoring-Engine vorhanden ist, müssen Ersetzungen sorgfältig geprüft werden.



<br>

---

<br>

### Navigation

„Gehe zu Zeile“ führt zu der in einem Befund genannten Quellposition. Die Statuszeile zeigt Zeile, Spalte, UTF-8 und Zeichenzahl.



<br>

---

<br>

### Empfohlener Ablauf

1. Betroffene Datei öffnen.
2. Befund und Kontext prüfen.
3. Gezielte Korrektur durchführen.
4. Datei speichern.
5. Analyse erneut starten.
6. Befunde und Kennzahlen prüfen.
7. Projekttests separat ausführen.



<br>

---

<br>

### Grenzen

Der Editor ist keine vollständige IDE. Nicht zwingend enthalten sind Language Server, Autovervollständigung, semantisches Refactoring, Debugging, Breakpoints, Terminal, Git-Konfliktlösung, Testausführung und Paketverwaltung.
