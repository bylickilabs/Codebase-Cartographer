# Database

## English

### Purpose

Codebase Cartographer uses SQLite as a persistent local archive for completed project analyses. The archive makes previous scans available after the application is closed and supports historical review, report export, and custom project notes.



<br>

---

<br>

### Default location

```text
~/.codebase_cartographer/codebase_cartographer.sqlite3
```

The exact home-directory path depends on the operating system and user account.



<br>

---

<br>

### Connection configuration

The application uses Python's standard-library `sqlite3` module and enables:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

A full WAL checkpoint is performed before exporting the complete database.



<br>

---

<br>

### Schema

```sql
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
```

Indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_project_scans_project_path
ON project_scans(project_path);

CREATE INDEX IF NOT EXISTS idx_project_scans_generated_at
ON project_scans(generated_at);
```



<br>

---

<br>

### Columns

| Column | Purpose |
|---|---|
| `id` | Unique scan identifier |
| `project_path` | Path of the analyzed project |
| `generated_at` | Analysis timestamp |
| `custom_message` | User note, limited to 1000 characters |
| `file_count` | Number of analyzed files |
| `finding_count` | Number of findings |
| `quality_score` | Quality index from 0 to 100 |
| `payload_json` | Complete serialized analysis |
| `application_version` | Version that created the record |
| `created_at` | SQLite insertion timestamp |



<br>

---

<br>

### Serialized payload

`payload_json` contains project metadata, analyzed files, line metrics, modules, symbols, imports, TODO markers, complexity, nesting, syntax errors, skipped-file data, findings, ignored-file counts, and excluded directories.

The separate summary columns make archive lists efficient, while the JSON payload preserves the complete scan.



<br>

---

<br>

### Operations

The database manager supports initialization, scan insertion, custom-message updates, archive listing, scan loading, individual scan export, deletion, WAL checkpointing, and `PRAGMA integrity_check`.

Deleting a scan removes only the archive record, not the original project.



<br>

---

<br>

### Custom messages

Each scan can store a message with up to 1000 characters. It can describe release state, review context, known limitations, or other project-specific information.



<br>

---

<br>

### Individual scan exports

Archived scans can be exported as JSON or Markdown. JSON contains the scan ID, custom message, complete analysis, and application metadata. Markdown produces a readable historical report.



<br>

---

<br>

### Protected full-database export

The complete SQLite database can be exported as a password-protected package.

Parameters:

```text
AES-256-GCM
PBKDF2-HMAC-SHA-256
390,000 iterations
32-byte derived key
16-byte random salt
12-byte random nonce
```

Package structure:

```text
magic header + salt + nonce + encrypted SQLite bytes
```

The live local database is not automatically encrypted. Encryption applies to the protected export package.



<br>

---

<br>

### Import validation

Import validates the package header, derives the key, authenticates and decrypts the content, writes a temporary SQLite file, runs `PRAGMA integrity_check`, creates a backup of the existing database, and replaces it only after successful validation.



<br>

---

<br>

### Maintenance recommendations

- use the integrated protected export for backups;
- store backups outside the application directory;
- keep passwords in a password manager;
- close the application before manually replacing the live database;
- avoid manually editing `payload_json`;
- treat database contents as potentially confidential.



<br>

---
---

<br>

## German

### Zweck

Codebase Cartographer verwendet SQLite als dauerhaftes lokales Archiv für abgeschlossene Projektanalysen. Frühere Scans bleiben nach dem Beenden verfügbar und können geprüft, exportiert und mit Projektnotizen ergänzt werden.



<br>

---

<br>

### Standardspeicherort

```text
~/.codebase_cartographer/codebase_cartographer.sqlite3
```

Der konkrete Benutzerpfad hängt vom Betriebssystem ab.



<br>

---

<br>

### Verbindungskonfiguration

Die Anwendung verwendet das Standardbibliotheksmodul `sqlite3` und aktiviert:

```sql
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

Vor dem vollständigen Datenbankexport wird ein WAL-Checkpoint ausgeführt.



<br>

---

<br>

### Schema

```sql
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
```

Indizes:

```sql
CREATE INDEX IF NOT EXISTS idx_project_scans_project_path
ON project_scans(project_path);

CREATE INDEX IF NOT EXISTS idx_project_scans_generated_at
ON project_scans(generated_at);
```



<br>

---

<br>

### Spalten

| Spalte | Zweck |
|---|---|
| `id` | Eindeutige Scan-ID |
| `project_path` | Pfad des analysierten Projekts |
| `generated_at` | Analysezeitpunkt |
| `custom_message` | Meldung mit maximal 1000 Zeichen |
| `file_count` | Anzahl analysierter Dateien |
| `finding_count` | Anzahl der Befunde |
| `quality_score` | Qualitätsindex von 0 bis 100 |
| `payload_json` | Vollständige serialisierte Analyse |
| `application_version` | Erzeugende Anwendungsversion |
| `created_at` | SQLite-Speicherzeitpunkt |



<br>

---

<br>

### Serialisierte Nutzdaten

`payload_json` enthält Projektmetadaten, Dateien, Zeilenkennzahlen, Module, Symbole, Importe, TODO-Markierungen, Komplexität, Verschachtelung, Syntaxfehler, übersprungene Dateien, Befunde, ignorierte Dateien und ausgeschlossene Verzeichnisse.

Zusammenfassungsspalten ermöglichen eine schnelle Archivliste, während JSON den vollständigen Scan bewahrt.



<br>

---

<br>

### Operationen

Der Datenbankmanager unterstützt Initialisierung, Speicherung, Meldungsaktualisierung, Auflistung, Laden, Einzelexport, Löschen, WAL-Checkpoint und `PRAGMA integrity_check`.

Das Löschen eines Scans entfernt nicht das Originalprojekt.



<br>

---

<br>

### Benutzerdefinierte Meldungen

Jeder Scan kann eine Meldung mit bis zu 1000 Zeichen speichern, etwa für Releasezustand, Prüfkontext oder bekannte Einschränkungen.



<br>

---

<br>

### Einzelne Scanexporte

Archivierte Scans können als JSON oder Markdown exportiert werden. JSON enthält Scan-ID, Meldung, Analyse und Anwendungsmetadaten. Markdown erzeugt einen lesbaren historischen Bericht.



<br>

---

<br>

### Geschützter Gesamtexport

Die vollständige SQLite-Datenbank kann passwortgeschützt exportiert werden.

Parameter:

```text
AES-256-GCM
PBKDF2-HMAC-SHA-256
390.000 Iterationen
32-Byte-Schlüssel
16-Byte-Salt
12-Byte-Nonce
```

Paketstruktur:

```text
Magic Header + Salt + Nonce + verschlüsselte SQLite-Daten
```

Die aktive lokale Datenbank ist nicht automatisch verschlüsselt. Der Schutz gilt für das Exportpaket.



<br>

---

<br>

### Importprüfung

Der Import prüft Header, Schlüssel, Authentifizierung, temporäre SQLite-Datei und Integrität, sichert die bestehende Datenbank und ersetzt sie erst nach erfolgreicher Validierung.



<br>

---

<br>

### Wartungsempfehlungen

- integrierten geschützten Export verwenden;
- Backups außerhalb des Anwendungsverzeichnisses speichern;
- Passwortmanager nutzen;
- Anwendung vor manuellem Austausch schließen;
- `payload_json` nicht unkontrolliert verändern;
- Datenbankinhalte als potenziell vertraulich behandeln.
