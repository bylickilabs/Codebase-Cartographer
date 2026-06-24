# Contributing to Codebase Cartographer

Thank you for your interest in contributing to **Codebase Cartographer**.

Codebase Cartographer is a local-first Python desktop application for analyzing Python projects. Contributions are welcome when they improve reliability, maintainability, usability, security, performance, documentation, accessibility, testing, or platform compatibility.

---

## Table of Contents

- [English](#english)
  - [Project Principles](#project-principles)
  - [Ways to Contribute](#ways-to-contribute)
  - [Before You Start](#before-you-start)
  - [Development Setup](#development-setup)
  - [Repository Workflow](#repository-workflow)
  - [Branch Naming](#branch-naming)
  - [Commit Messages](#commit-messages)
  - [Coding Standards](#coding-standards)
  - [Architecture Guidelines](#architecture-guidelines)
  - [User Interface Contributions](#user-interface-contributions)
  - [Database Contributions](#database-contributions)
  - [Security-Sensitive Contributions](#security-sensitive-contributions)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Pull Requests](#pull-requests)
  - [Bug Reports](#bug-reports)
  - [Feature Requests](#feature-requests)
  - [Translations](#translations)
  - [Review Process](#review-process)
  - [Licensing](#licensing)

---

# English

## Project Principles

Contributions must support these principles:

1. Local-first processing
2. No unnecessary data transmission
3. Transparent and reproducible analysis
4. Readable and maintainable Python code
5. Cross-platform desktop compatibility
6. Safe handling of source files and database archives
7. Consistent German and English user experience
8. Minimal and justified dependencies
9. Deterministic analysis where possible
10. Clear error handling and recovery behavior

## Ways to Contribute

You can contribute through:

- Bug fixes
- New analysis rules
- Performance improvements
- Refactoring
- Automated tests
- Documentation
- Translation corrections
- Accessibility improvements
- User-interface improvements
- Cross-platform fixes
- SQLite improvements
- Archive import and export improvements
- Packaging and release automation
- Issue triage
- Reproducible test cases

Security vulnerabilities must not be reported through public issues. Follow `SECURITY.md`.

## Before You Start

Before working on a substantial change:

1. Search existing issues and pull requests.
2. Confirm that the change fits the project scope.
3. Open an issue for major features, architecture changes, database schema changes, cryptographic changes, or large UI redesigns.
4. Keep pull requests focused on one logical change.
5. Avoid unrelated formatting or refactoring.
6. Do not include private source code, credentials, local databases, or personal filesystem paths.

Small typo fixes and narrowly scoped documentation improvements may be submitted directly.

## Development Setup

### Recommended Requirements

- Python 3.11 or newer
- Git
- Tk support
- A virtual environment
- A supported desktop operating system

### Clone the Repository

```bash
git clone https://github.com/bylickilabs/Codebase-Cartographer.git
cd Codebase-Cartographer
```

### Create a Virtual Environment

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

Replace `main.py` if the repository uses another entry-point filename.

## Repository Workflow

1. Fork the repository.
2. Clone your fork.
3. Add the upstream repository.
4. Create a dedicated branch.
5. Implement and test the change.
6. Update documentation and translations.
7. Commit the change.
8. Push the branch.
9. Open a pull request.

```bash
git remote add upstream https://github.com/bylickilabs/Codebase-Cartographer.git
git fetch upstream
git checkout -b fix/editor-save-handling upstream/main
```

Before opening a pull request:

```bash
git fetch upstream
git rebase upstream/main
```

Do not force-push shared branches.

## Branch Naming

Use lowercase and descriptive branch names.

Recommended prefixes:

```text
feature/
fix/
docs/
refactor/
test/
security/
performance/
build/
ci/
chore/
translation/
```

Examples:

```text
feature/dependency-filter
fix/sqlite-import-rollback
security/archive-validation
docs/update-installation
translation/german-ui-corrections
```

## Commit Messages

Recommended format:

```text
type(scope): concise summary
```

Examples:

```text
feat(analysis): add async function metrics
fix(editor): preserve encoding when saving
fix(database): restore backup after failed import
docs(readme): clarify local processing
security(archive): reject malformed headers
test(complexity): add nested match cases
```

Each commit should:

- Represent one logical change
- Use clear language
- Avoid unrelated changes
- Avoid generated files unless necessary
- Contain no secrets, private code, or personal data

## Coding Standards

### Python

- Use type annotations for public functions and important interfaces.
- Prefer `pathlib.Path` for filesystem operations.
- Use dataclasses for structured data where appropriate.
- Keep functions focused and readable.
- Avoid hidden global state.
- Handle platform-specific behavior explicitly.
- Catch only exceptions that can be handled meaningfully.
- Use descriptive names.
- Avoid wildcard imports.
- Document public classes, methods, and functions.
- Preserve compatibility with the minimum supported Python version.
- Use UTF-8 for source files and text exports.
- Avoid blocking the GUI thread.

### Formatting and Linting

Use the repository tooling when configured.

```bash
python -m ruff check .
python -m ruff format --check .
python -m black --check .
```

Do not reformat unrelated files.

### Import Order

1. Future imports
2. Standard library
3. Third-party dependencies
4. Local imports

### Error Handling

User-facing errors should:

- Identify the failed action
- Avoid exposing secrets
- Preserve useful diagnostic context
- Be translated where displayed in the UI
- Warn clearly about possible data-loss risks

### Threading

Tkinter and CustomTkinter widgets must be updated from the main GUI thread.

Background operations should:

- Return results through safe callbacks
- Restore controls after success or failure
- Avoid concurrent access to the same database connection
- Avoid accessing destroyed widgets
- Handle shutdown cleanly

## Architecture Guidelines

Keep a clear separation between:

- Project discovery
- File reading
- AST parsing
- Symbol extraction
- Import analysis
- Complexity analysis
- Finding generation
- Report generation
- Database persistence
- Secure archive import and export
- Source-code editing
- User-interface rendering
- Translation resources

New analysis rules should:

1. Produce deterministic results.
2. Define severity.
3. Provide a clear description.
4. Provide a practical recommendation.
5. Include German and English translations.
6. Avoid excessive false positives.
7. Include positive and negative tests.

Do not couple analysis logic directly to GUI widgets.

## User Interface Contributions

The interface uses Tkinter, ttk, and CustomTkinter.

UI changes must:

- Work in dark and light modes
- Remain usable at the minimum window size
- Preserve keyboard accessibility where possible
- Use the translation system for visible text
- Include German and English labels
- Avoid blocking the GUI
- Confirm destructive actions
- Display accurate status and progress information
- Handle long paths and large result text safely

Every new visible string must be added to both language dictionaries.

## Database Contributions

The application uses SQLite for local scan history.

Database changes must:

- Use parameterized SQL
- Preserve transactional integrity
- Define rollback behavior
- Avoid data loss
- Create backups before destructive replacement
- Document schema changes
- Include migrations when required
- Test empty, old, partial, and corrupted databases
- Handle connection closing and checkpoints correctly

The local SQLite database must not be described as encrypted unless the implementation actually encrypts it.

Password-protected `.ccdb` exports must be treated separately from the live SQLite database.

## Security-Sensitive Contributions

Changes involving these areas require additional review:

- Password handling
- Key derivation
- AES-GCM or other cryptography
- Nonce and salt generation
- Archive headers
- Database import and replacement
- Backup and rollback behavior
- Path validation
- Symlink handling
- Temporary files
- File overwrite behavior
- External process execution
- URL opening
- Source-editor saving

Do not implement custom cryptographic primitives.

Never log passwords, derived keys, private source code, plaintext database contents, tokens, or credentials.

## Testing

### Minimum Manual Verification

Verify:

- Application startup
- Project selection
- Valid project analysis
- Syntax-error handling
- Oversized-file handling
- File and symbol filtering
- Dependency categorization
- Finding generation
- German and English switching
- Dark and light modes
- JSON and Markdown exports
- Source-file opening and saving
- SQLite persistence
- Archived scan loading
- Protected database export
- Correct-password import
- Wrong-password rejection
- Failed-import rollback
- Clean shutdown

### Automated Tests

Preferred areas:

- Line counting
- TODO detection
- Module-name conversion
- Import categorization
- AST extraction
- Complexity calculations
- Finding thresholds
- Quality-score calculations
- Serialization
- Database operations
- Database migrations
- Archive authentication
- Corrupted-archive rejection
- Encoding handling
- Cross-platform filesystem operations

```bash
python -m pytest
```

With coverage:

```bash
python -m pytest --cov
```

Tests must not depend on internet access, personal paths, existing databases, real credentials, or private projects.

## Documentation

Update documentation when changes affect installation, dependencies, supported Python versions, workflows, configuration, database behavior, security guarantees, export formats, editor behavior, supported operating systems, or known limitations.

Use fictional data in examples.

## Pull Requests

A pull request should include:

- Clear title
- Problem description
- Implementation summary
- Related issue
- Tests performed
- UI screenshots for visible changes
- Compatibility notes
- Security impact
- Database migration impact
- Documentation changes
- Known limitations

Suggested checklist:

```markdown
## Summary

Describe the change.

## Related Issue

Closes #

## Validation

- [ ] Tests pass
- [ ] Manual application test completed
- [ ] German UI reviewed
- [ ] English UI reviewed
- [ ] Dark mode reviewed
- [ ] Light mode reviewed
- [ ] No secrets or private source code included
- [ ] Documentation updated
- [ ] Database compatibility reviewed
- [ ] Security impact reviewed
```

## Bug Reports

A useful bug report includes:

- Application version
- Python version
- Operating system
- Installation method
- Reproduction steps
- Expected behavior
- Actual behavior
- Error message
- Sanitized logs
- Minimal reproducible example

Do not attach confidential source code, unredacted databases, passwords, credentials, or personal data.

## Feature Requests

Explain:

- The user problem
- The proposed behavior
- Why it belongs in Codebase Cartographer
- Possible alternatives
- UI impact
- Analysis impact
- Performance impact
- Database impact
- Security and privacy impact
- Translation requirements

Discuss large features before implementation.

## Translations

The application supports German and English.

Translation contributions must preserve meaning, use consistent terminology, fit the interface, be manually reviewed, update every corresponding key, and avoid changing logic.

## Review Process

A contribution may be accepted when it:

- Fits project scope
- Is technically correct
- Preserves privacy and security
- Includes appropriate tests
- Preserves compatibility
- Includes translations
- Updates documentation
- Avoids unnecessary dependencies
- Uses compatible licensing
- Meets maintainability expectations

Final decisions remain with the maintainers.

## Licensing

By contributing, you agree that your contribution may be distributed under the repository license.

Only submit work you are legally permitted to contribute.

---
---