# Security Policy

The security of **Codebase Cartographer** is important because the application analyzes local source code, writes scan results to SQLite, edits files, and imports or exports database archives.

Please report vulnerabilities responsibly and privately.

---

## Table of Contents

- [English](#english)
  - [Supported Versions](#supported-versions)
  - [Reporting a Vulnerability](#reporting-a-vulnerability)
  - [Do Not Report Publicly](#do-not-report-publicly)
  - [What to Include](#what-to-include)
  - [Response Process](#response-process)
  - [Security Scope](#security-scope)
  - [Out of Scope](#out-of-scope)
  - [Sensitive Areas](#sensitive-areas)
  - [Local Data and Privacy](#local-data-and-privacy)
  - [SQLite Database](#sqlite-database)
  - [Protected CCDB Exports](#protected-ccdb-exports)
  - [Source-Code Editor](#source-code-editor)
  - [Dependency Security](#dependency-security)
  - [Disclosure Policy](#disclosure-policy)
  - [Safe Harbor](#safe-harbor)
  
---

# English

## Supported Versions

Security fixes are generally provided for the latest maintained release.

| Version | Supported |
|---|---|
| Latest stable release | Yes |
| Previous releases | Best effort |
| Development branches | No guarantee |
| Unofficial forks | No |

Users should update to the latest stable release before reporting an issue already fixed upstream.

## Reporting a Vulnerability

Preferred reporting method:

1. Open the repository on GitHub.
2. Navigate to **Security**.
3. Select **Advisories**.
4. Choose **Report a vulnerability**.

If private vulnerability reporting is unavailable, contact the repository owner privately through an official channel listed in the GitHub profile or repository.

Do not include exploit details in public issues, discussions, pull requests, or social media posts.

## Do Not Report Publicly

Do not publicly disclose vulnerabilities involving:

- Source-code exposure
- Arbitrary file read or write
- Path traversal
- Symlink attacks
- Database corruption
- Archive tampering
- Password handling
- Key derivation
- Authentication bypass
- AES-GCM misuse
- Malicious `.ccdb` files
- Command execution
- URL or process launching
- Data exfiltration
- Dependency compromise
- Denial of service through crafted projects
- Editor overwrite behavior

Public reports may place users and their source code at risk.

## What to Include

A useful report includes:

- Vulnerability title
- Affected version or commit
- Operating system
- Python version
- Installation method
- Affected component
- Technical description
- Reproduction steps
- Proof of concept
- Expected behavior
- Actual behavior
- Security impact
- Suggested mitigation
- Relevant logs with secrets removed
- Whether public disclosure has already occurred

Use minimal synthetic test data.

Do not send real private projects, credentials, passwords, or production databases unless explicitly requested through a secure channel.

## Response Process

The maintainers aim to:

1. Acknowledge the report.
2. Validate and reproduce the issue.
3. Assess severity and affected versions.
4. Develop a fix or mitigation.
5. Test the fix.
6. Prepare a release.
7. Coordinate disclosure.
8. Credit the reporter when requested and appropriate.

No specific response or release deadline is guaranteed.

Complex issues may require additional investigation.

## Security Scope

In scope:

- Codebase Cartographer application code
- Official release packages
- Project analysis logic
- File discovery and reading
- AST parsing
- Source-code editor operations
- SQLite persistence
- Scan archive loading
- `.ccdb` import and export
- Password and key handling
- Archive integrity validation
- Backup and rollback behavior
- Path handling
- External process and URL opening
- Official dependency configuration

## Out of Scope

Generally out of scope:

- Vulnerabilities in unsupported versions
- Issues caused only by modified forks
- Social engineering
- Physical access to an unlocked machine
- Operating-system vulnerabilities
- Python runtime vulnerabilities
- Third-party package vulnerabilities with no project-specific impact
- Denial of service requiring unreasonable local resources
- Reports without a realistic security impact
- Self-XSS or equivalent local-only behavior without privilege impact
- Missing security headers for a non-web desktop application

Third-party dependency issues may still be relevant when Codebase Cartographer exposes or amplifies the vulnerability.

## Sensitive Areas

Particular attention should be given to:

- Untrusted project paths
- Symbolic links
- Very large files
- Crafted Python syntax
- Deep AST structures
- Malformed text encodings
- Corrupted SQLite files
- Malicious archive headers
- Modified ciphertext
- Weak password processing
- Reused salts or nonces
- Temporary file permissions
- Insecure backup replacement
- Race conditions during import
- Overwrite confirmation
- External commands
- Browser opening
- Error messages containing private paths

## Local Data and Privacy

Codebase Cartographer is designed to analyze projects locally.

Security reports should distinguish between:

- Intended local file access selected by the user
- Unexpected access outside the selected project
- Unexpected network communication
- Logging or persistence of source content
- Exposure through reports or archives

Any unexpected transmission of source code, scan data, file paths, passwords, or database content is considered security-relevant.

## SQLite Database

The live application database may contain:

- Scan metadata
- Project paths
- File analysis results
- Findings
- Custom messages
- Archive history

Unless the application explicitly implements database encryption, the local SQLite database must be treated as plaintext storage protected by operating-system access controls.

Users should:

- Protect their operating-system account
- Restrict access to the application data directory
- Avoid sharing the live database
- Remove sensitive project data before sharing diagnostics
- Use encrypted storage where appropriate

## Protected CCDB Exports

Password-protected `.ccdb` exports are distinct from the live SQLite database.

Security expectations include:

- Authenticated encryption
- Unique random salt
- Unique nonce
- Strong key derivation
- Correct archive-header validation
- Rejection of modified ciphertext
- Rejection of wrong passwords
- Safe temporary-file handling
- Verified rollback after failed import

A protected export is only as strong as its password.

Do not claim that password recovery is possible unless such a feature explicitly exists.

## Source-Code Editor

The integrated editor can modify user files.

Security-sensitive behavior includes:

- Correct file selection
- Overwrite confirmation
- Encoding preservation
- Handling of read-only files
- Symlink behavior
- Save failures
- Partial writes
- Backup behavior
- Protection against writing outside intended paths

Atomic writes are preferred where practical.

## Dependency Security

Contributors should:

- Pin or constrain dependencies where appropriate
- Avoid abandoned packages
- Review dependency licenses
- Avoid unnecessary dependencies
- Monitor security advisories
- Update vulnerable dependencies
- Verify package names to reduce dependency-confusion risk
- Avoid installing packages from untrusted indexes

Do not commit dependency credentials or private index tokens.

## Disclosure Policy

Please allow maintainers reasonable time to investigate and release a fix before public disclosure.

Coordinated disclosure may include:

- A private advisory
- A patched release
- Release notes
- CVE coordination where appropriate
- Reporter credit
- Mitigation guidance

The project may publish details after a fix is available or when continued secrecy no longer protects users.

## Safe Harbor

Good-faith security research is welcome when it:

- Avoids privacy violations
- Avoids data destruction
- Uses test data
- Does not access systems without authorization
- Does not disrupt other users
- Reports findings privately
- Allows reasonable remediation time
- Complies with applicable law

This policy does not authorize testing against systems, repositories, accounts, or data you do not own or have permission to test.

---
