# Privacy

## English

### Local processing

Codebase Cartographer is designed to process Python projects locally. File discovery, source reading, AST parsing, metrics, findings, reports, editing, and SQLite archiving run on the user's own system.

The core application does not require source-code upload to an external analysis service.



<br>

---

<br>

### Processed information

The application may process project paths, file paths, Python source text, module and symbol names, imports, line metrics, docstring states, complexity, nesting, TODO markers, syntax errors, findings, recommendations, and custom messages.



<br>

---

<br>

### Local database

Completed scans are stored in:

```text
~/.codebase_cartographer/codebase_cartographer.sqlite3
```

The live SQLite database can contain sensitive project metadata and is not automatically encrypted by the application.

Operating-system access controls, account security, disk encryption, backups, and device protection remain the user's responsibility.



<br>

---

<br>

### Protected exports

Password-protected database exports use AES-256-GCM and PBKDF2-HMAC-SHA-256 with 390,000 iterations.

This protects the exported package. It does not encrypt the live local database or ordinary JSON and Markdown reports.



<br>

---

<br>

### Plain exports

JSON and Markdown are plain files unless the user applies additional protection. They can expose local paths, project names, file names, symbols, dependencies, findings, and custom messages.

Review them before publishing or sharing.



<br>

---

<br>

### Editor access

The integrated editor reads and writes local files selected by the user. Saving can modify the original project. Version control and backups are strongly recommended.



<br>

---

<br>

### External links and packages

Opening GitHub or another explicit link transfers control to the browser and destination website. Installing Python packages through `pip` also involves external package infrastructure.

These processes are outside the core local analysis workflow.



<br>

---

<br>

### Telemetry

The provided core application does not require analytics telemetry, advertising tracking, user profiling, or remote project upload.

Future telemetry, update checks, crash reporting, cloud APIs, or plugins must be documented separately.



<br>

---

<br>

### User responsibilities

Users should protect accounts and devices, analyze only authorized projects, use strong export passwords, keep passwords separate from packages, review reports before sharing, understand cloud synchronization, and comply with confidentiality obligations.



<br>

---

<br>

### Deletion

Deleting a scan removes its archive record but does not remove original source files, previous exports, backups, cloud copies, or operating-system snapshots.

Complete deletion requires removing all copies from the relevant storage systems.



<br>

---

<br>

### Limitations

Local processing reduces unnecessary data transfer but cannot protect against malware, compromised accounts, insecure backups, weak passwords, unencrypted disks, accidental publication, or modified distributions.



<br>

---
---

<br>

## German

### Lokale Verarbeitung

Codebase Cartographer verarbeitet Python-Projekte lokal. Dateisuche, Quelltextzugriff, AST-Parsing, Kennzahlen, Befunde, Berichte, Bearbeitung und SQLite-Archivierung laufen auf dem eigenen System.

Der Kernablauf benötigt keinen Upload an einen externen Analysedienst.



<br>

---

<br>

### Verarbeitete Informationen

Verarbeitet werden können Projekt- und Dateipfade, Python-Quelltext, Modul- und Symbolnamen, Importe, Zeilenkennzahlen, Docstrings, Komplexität, Verschachtelung, TODO-Markierungen, Syntaxfehler, Befunde, Empfehlungen und Meldungen.



<br>

---

<br>

### Lokale Datenbank

Abgeschlossene Scans werden gespeichert in:

```text
~/.codebase_cartographer/codebase_cartographer.sqlite3
```

Die aktive SQLite-Datenbank kann vertrauliche Projektmetadaten enthalten und wird nicht automatisch verschlüsselt.

Betriebssystemrechte, Kontosicherheit, Datenträgerverschlüsselung, Backups und Geräteschutz liegen in der Verantwortung des Benutzers.



<br>

---

<br>

### Geschützte Exporte

Passwortgeschützte Datenbankexporte verwenden AES-256-GCM und PBKDF2-HMAC-SHA-256 mit 390.000 Iterationen.

Dies schützt das Exportpaket, nicht die aktive Datenbank oder normale JSON- und Markdown-Dateien.



<br>

---

<br>

### Unverschlüsselte Exporte

JSON und Markdown sind Klartextdateien, sofern der Benutzer sie nicht zusätzlich schützt. Sie können Pfade, Projektnamen, Dateien, Symbole, Abhängigkeiten, Befunde und Meldungen offenlegen.

Vor Veröffentlichung oder Weitergabe müssen sie geprüft werden.



<br>

---

<br>

### Editorzugriff

Der Editor liest und schreibt ausgewählte lokale Dateien. Speichern kann das Originalprojekt verändern. Versionsverwaltung und Backups werden dringend empfohlen.



<br>

---

<br>

### Externe Links und Pakete

Beim Öffnen von GitHub oder anderen Links übernimmt der Browser. Auch `pip`-Installationen nutzen externe Infrastruktur.

Diese Vorgänge liegen außerhalb der lokalen Kernanalyse.



<br>

---

<br>

### Telemetrie

Die vorliegende Kernanwendung benötigt keine Analytiktelemetrie, Werbetracking, Benutzerprofile oder Remote-Projektuploads.

Zukünftige Telemetrie, Updateprüfungen, Crashberichte, Cloud-APIs oder Plugins müssen separat dokumentiert werden.



<br>

---

<br>

### Verantwortung

Benutzer sollten Konten und Geräte schützen, nur berechtigte Projekte analysieren, starke Exportpasswörter verwenden, Passwörter getrennt speichern, Berichte vor dem Teilen prüfen, Cloud-Synchronisierung verstehen und Vertraulichkeitspflichten einhalten.



<br>

---

<br>

### Löschung

Das Löschen eines Scans entfernt den Archiveintrag, nicht aber Originaldateien, Exporte, Backups, Cloudkopien oder Snapshots.

Für vollständige Löschung müssen alle Kopien entfernt werden.



<br>

---

<br>

### Grenzen

Lokale Verarbeitung reduziert Datenübertragung, schützt aber nicht vor Malware, kompromittierten Konten, unsicheren Backups, schwachen Passwörtern, unverschlüsselten Datenträgern, versehentlicher Veröffentlichung oder manipulierten Distributionen.
