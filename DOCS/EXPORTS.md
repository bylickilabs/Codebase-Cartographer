# Exports

## English

### Available formats

Codebase Cartographer supports:

- current analysis as JSON;
- current analysis as Markdown;
- archived scan as JSON;
- archived scan as Markdown;
- complete SQLite archive as a password-protected package;
- import of a protected database package.



<br>

---

<br>

### JSON

JSON preserves structured data such as application metadata, project path, timestamps, totals, file analyses, symbols, imports, TODO markers, findings, ignored files, and excluded directories.

Archive JSON also includes scan ID and custom message.

JSON is intended for automation, scripts, dashboards, comparisons, and external processing.



<br>

---

<br>

### Markdown

Markdown produces a human-readable report for GitHub, reviews, documentation, and local records. It can include project information, metrics, documentation coverage, quality score, file data, findings, recommendations, and generator information.



<br>

---

<br>

### Archived scan exports

One historical scan can be exported independently of the full database.

The JSON structure includes:

```text
scan_id
custom_message
analysis
application
```

The Markdown form renders the same historical context as a readable report.



<br>

---

<br>

### Protected database package

The full archive export uses:

```text
AES-256-GCM
PBKDF2-HMAC-SHA-256
390,000 iterations
32-byte key
16-byte salt
12-byte nonce
```

The package starts with the versioned magic header:

```text
CODEBASE_CARTOGRAPHER_DB_V3
```

followed by a null byte, salt, nonce, and encrypted SQLite payload.



<br>

---

<br>

### Security behavior

AES-GCM authenticates the encrypted data. A wrong password, damaged package, modified payload, or incorrect header causes decryption or validation to fail.

The password is not stored in the package. Losing it normally means the protected export cannot be recovered.



<br>

---

<br>

### Import workflow

Import requires confirmation, validates the package, decrypts it to a temporary file, runs an SQLite integrity check, backs up the current database, and replaces it only after validation succeeds.



<br>

---

<br>

### Format selection

| Purpose | Format |
|---|---|
| Human-readable report | Markdown |
| Automated processing | JSON |
| One historical scan | Archive JSON |
| Complete history | Database package |
| Protected backup or transfer | Encrypted database package |



<br>

---

<br>

### Sensitive content

Exports can contain local paths, project names, file names, symbols, imports, findings, timestamps, and custom messages. Review plain JSON and Markdown before publishing them.



<br>

---

<br>

### Version compatibility

The database package is versioned through its magic header. JSON and Markdown structures may evolve. External tools should validate required fields and ignore unknown fields when possible.



<br>

---
---

<br>

## German

### Verfügbare Formate

Codebase Cartographer unterstützt:

- aktuelle Analyse als JSON;
- aktuelle Analyse als Markdown;
- archivierten Scan als JSON;
- archivierten Scan als Markdown;
- vollständiges SQLite-Archiv als passwortgeschütztes Paket;
- Import eines geschützten Datenbankpakets.



<br>

---

<br>

### JSON

JSON bewahrt strukturierte Daten wie Anwendungsmetadaten, Projektpfad, Zeitpunkte, Gesamtwerte, Dateianalysen, Symbole, Importe, TODO-Markierungen, Befunde, ignorierte Dateien und Ausschlüsse.

Archiv-JSON enthält zusätzlich Scan-ID und Meldung.

JSON ist für Automatisierung, Skripte, Dashboards, Vergleiche und externe Verarbeitung vorgesehen.



<br>

---

<br>

### Markdown

Markdown erzeugt einen lesbaren Bericht für GitHub, Reviews, Dokumentation und lokale Nachweise. Enthalten sein können Projektinformationen, Kennzahlen, Dokumentationsabdeckung, Qualitätsindex, Dateidaten, Befunde, Empfehlungen und Generatorinformationen.



<br>

---

<br>

### Archivscanexporte

Ein historischer Scan kann unabhängig von der gesamten Datenbank exportiert werden.

Die JSON-Struktur enthält:

```text
scan_id
custom_message
analysis
application
```

Markdown stellt denselben historischen Kontext lesbar dar.



<br>

---

<br>

### Geschütztes Datenbankpaket

Der vollständige Archivexport verwendet:

```text
AES-256-GCM
PBKDF2-HMAC-SHA-256
390.000 Iterationen
32-Byte-Schlüssel
16-Byte-Salt
12-Byte-Nonce
```

Das Paket beginnt mit:

```text
CODEBASE_CARTOGRAPHER_DB_V3
```

gefolgt von Nullbyte, Salt, Nonce und verschlüsseltem SQLite-Payload.



<br>

---

<br>

### Sicherheitsverhalten

AES-GCM authentifiziert die verschlüsselten Daten. Falsches Passwort, beschädigtes Paket, veränderte Nutzdaten oder falscher Header führen zum Abbruch.

Das Passwort wird nicht gespeichert. Bei Verlust ist der Export normalerweise nicht wiederherstellbar.



<br>

---

<br>

### Importablauf

Der Import verlangt eine Bestätigung, validiert das Paket, entschlüsselt in eine temporäre Datei, prüft SQLite, sichert die aktuelle Datenbank und ersetzt sie erst nach erfolgreicher Validierung.



<br>

---

<br>

### Formatwahl

| Zweck | Format |
|---|---|
| Lesbarer Bericht | Markdown |
| Automatisierte Verarbeitung | JSON |
| Einzelner historischer Scan | Archiv-JSON |
| Vollständige Historie | Datenbankpaket |
| Geschütztes Backup oder Übertragung | Verschlüsseltes Datenbankpaket |



<br>

---

<br>

### Sensible Inhalte

Exporte können lokale Pfade, Projekte, Dateien, Symbole, Importe, Befunde, Zeitstempel und Meldungen enthalten. JSON und Markdown müssen vor Veröffentlichung geprüft werden.



<br>

---

<br>

### Versionskompatibilität

Das Datenbankpaket ist über den Magic Header versioniert. JSON- und Markdown-Strukturen können sich weiterentwickeln. Externe Werkzeuge sollten Pflichtfelder prüfen und unbekannte Felder tolerieren.
