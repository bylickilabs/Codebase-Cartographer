# Compatibility

## English

### Requirements

Codebase Cartographer requires a supported Python 3 interpreter, Tk/Tkinter, a graphical desktop session, read access to project directories, write access to the application data directory, and the packages in `requirements.txt`.



<br>

---

<br>

### Python

Recommended baseline:

```text
Python 3.10 or newer
```

The CI workflow targets Python 3.10 and Python 3.14.

The application uses dataclasses, modern type annotations, built-in generic types, union syntax, and current AST nodes. New Python releases should be tested before being declared fully supported.



<br>

---

<br>

### Operating systems

The desktop application is intended for:

- Windows
- macOS
- desktop Linux

Folder opening uses `os.startfile` on Windows, `open` on macOS, and `xdg-open` on Linux and other Unix-like desktops.



<br>

---

<br>

### Windows

Standard Python installations usually include Tkinter. Antivirus software, enterprise restrictions, controlled-folder access, long paths, and user-profile permissions can affect scanning or saving.



<br>

---

<br>

### macOS

Python must include a working Tk framework. macOS privacy permissions may restrict Desktop, Documents, Downloads, external drives, and network shares. Gatekeeper can affect packaged unsigned builds.



<br>

---

<br>

### Linux

Tkinter may require a package such as `python3-tk`. `xdg-open` should be available. A graphical display is required; headless servers are not the primary supported environment.



<br>

---

<br>

### Dependencies

External runtime packages:

```text
customtkinter
cryptography
```

Modules such as `ast`, `json`, `sqlite3`, `threading`, `pathlib`, `tkinter`, `hashlib`, `tempfile`, and `subprocess` belong to the Python standard library.



<br>

---

<br>

### Tkinter verification

```bash
python -c "import tkinter; print(tkinter.TkVersion)"
```

If this fails, Tk support must be installed or repaired for the selected Python distribution.



<br>

---

<br>

### Source compatibility

The AST parser belongs to the Python version running the application. Source syntax newer than that interpreter may produce syntax errors.

For best results, run Codebase Cartographer with a Python version equal to or newer than the analyzed project's syntax level.



<br>

---

<br>

### Filesystems

The scanner works with local or mounted filesystems accessible through `pathlib` and `os`.

Possible issues include permissions, unavailable network shares, broken links, long paths, files changing during scans, non-UTF-8 files, cloud placeholders, and case-sensitivity differences.



<br>

---

<br>

### Project layouts

Conventional layouts such as `src`, packages, tests, and scripts are supported. Import classification remains heuristic for namespace packages, monorepos, multiple source roots, editable installs, and runtime `sys.path` changes.



<br>

---

<br>

### Database compatibility

The local archive uses SQLite. The protected package format is application-specific and versioned with `CODEBASE_CARTOGRAPHER_DB_V3`.

Future incompatible formats may require migration support.



<br>

---

<br>

### Display

Default window size:

```text
1500 × 900
```

Minimum size:

```text
1180 × 720
```

Small displays, high scaling, remote desktops, and different window managers can affect layout and rendering.



<br>

---

<br>

### Headless environments

The current application expects a graphical interface and is not primarily designed as a CLI or server process. Containers, CI servers, and SSH sessions without a display may fail when Tk starts.



<br>

---

<br>

### Packaging

When using PyInstaller, Nuitka, cx_Freeze, or similar tools, verify CustomTkinter assets, Tcl/Tk files, Cryptography binaries, platform libraries, signing, user-data permissions, and antivirus behavior.



<br>

---

<br>

### Known limitations

- only `.py` files are analyzed;
- files larger than 3,000,000 bytes are skipped;
- dynamic imports may be classified incorrectly;
- generated or runtime-created code is not resolved;
- the editor is not a full IDE;
- the live database is not automatically encrypted;
- JSON and Markdown exports are plain text;
- archived source files need the original path for editing;
- analysis must be rerun after editor changes.



<br>

---
---

<br>

## German

### Anforderungen

Codebase Cartographer benötigt einen unterstützten Python-3-Interpreter, Tk/Tkinter, eine grafische Desktopsitzung, Leserechte für Projekte, Schreibrechte im Anwendungsdatenverzeichnis und die Pakete aus `requirements.txt`.



<br>

---

<br>

### Python

Empfohlene Basis:

```text
Python 3.10 oder neuer
```

Der CI-Workflow testet Python 3.10 und Python 3.14.

Verwendet werden Dataclasses, moderne Typannotationen, eingebaute generische Typen, Union-Syntax und aktuelle AST-Knoten. Neue Python-Versionen müssen vor offizieller Unterstützung geprüft werden.



<br>

---

<br>

### Betriebssysteme

Vorgesehen für:

- Windows
- macOS
- Desktop-Linux

Ordneröffnung erfolgt über `os.startfile`, `open` oder `xdg-open`.



<br>

---

<br>

### Windows

Standardinstallationen enthalten meist Tkinter. Antivirus, Unternehmensrichtlinien, Controlled Folder Access, lange Pfade und Benutzerrechte können Scan- oder Speichervorgänge beeinflussen.



<br>

---

<br>

### macOS

Python benötigt ein funktionierendes Tk-Framework. Datenschutzrechte können Desktop, Dokumente, Downloads, externe Laufwerke und Netzfreigaben einschränken. Gatekeeper kann unsignierte Pakete blockieren.



<br>

---

<br>

### Linux

Tkinter muss möglicherweise als `python3-tk` installiert werden. `xdg-open` sollte verfügbar sein. Eine grafische Anzeige ist erforderlich; Headless-Server sind nicht das primäre Ziel.



<br>

---

<br>

### Abhängigkeiten

Externe Laufzeitpakete:

```text
customtkinter
cryptography
```

`ast`, `json`, `sqlite3`, `threading`, `pathlib`, `tkinter`, `hashlib`, `tempfile` und `subprocess` gehören zur Standardbibliothek.



<br>

---

<br>

### Tkinter-Prüfung

```bash
python -c "import tkinter; print(tkinter.TkVersion)"
```

Schlägt dies fehl, muss die Tk-Unterstützung der Python-Distribution installiert oder repariert werden.



<br>

---

<br>

### Quellcodekompatibilität

Der AST-Parser gehört zur laufenden Python-Version. Neuere Syntax kann als Fehler erscheinen.

Für beste Ergebnisse sollte die Anwendung mindestens mit dem Syntaxniveau des analysierten Projekts laufen.



<br>

---

<br>

### Dateisysteme

Unterstützt werden lokale und eingebundene Dateisysteme, die über `pathlib` und `os` erreichbar sind.

Probleme können durch Rechte, Netzlaufwerke, defekte Links, lange Pfade, gleichzeitige Änderungen, nicht UTF-8-kodierte Dateien, Cloud-Platzhalter und Groß-/Kleinschreibung entstehen.



<br>

---

<br>

### Projektstrukturen

Übliche Strukturen mit `src`, Paketen, Tests und Skripten werden unterstützt. Namespace Packages, Monorepos, mehrere Source Roots, Editable Installs und Laufzeitänderungen an `sys.path` können die Importkategorisierung beeinflussen.



<br>

---

<br>

### Datenbankkompatibilität

Das Archiv nutzt SQLite. Das geschützte Paketformat ist anwendungsspezifisch und mit `CODEBASE_CARTOGRAPHER_DB_V3` versioniert.

Zukünftige inkompatible Formate können Migrationen erfordern.



<br>

---

<br>

### Anzeige

Standardgröße:

```text
1500 × 900
```

Mindestgröße:

```text
1180 × 720
```

Kleine Displays, hohe Skalierung, Remote Desktop und unterschiedliche Fenstermanager können Darstellung und Layout beeinflussen.



<br>

---

<br>

### Headless-Umgebungen

Die Anwendung erwartet eine grafische Oberfläche und ist nicht primär als CLI oder Serverprozess ausgelegt. Container, CI-Server und SSH-Sitzungen ohne Display können beim Tk-Start scheitern.



<br>

---

<br>

### Paketierung

Bei PyInstaller, Nuitka, cx_Freeze oder ähnlichen Werkzeugen müssen CustomTkinter-Ressourcen, Tcl/Tk-Dateien, Cryptography-Binärmodule, Plattformbibliotheken, Signierung, Schreibrechte und Antivirusverhalten geprüft werden.



<br>

---

<br>

### Bekannte Einschränkungen

- nur `.py`-Dateien;
- Dateien über 3.000.000 Byte werden übersprungen;
- dynamische Importe können falsch kategorisiert werden;
- generierter Laufzeitcode wird nicht aufgelöst;
- der Editor ist keine vollständige IDE;
- die aktive Datenbank ist nicht automatisch verschlüsselt;
- JSON und Markdown sind Klartext;
- archivierte Dateien benötigen den Originalpfad zur Bearbeitung;
- nach Editoränderungen muss erneut analysiert werden.
