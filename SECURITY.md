# Security

## Reporting a vulnerability

If you find a security issue in OSCP Notes, please email **th3cyb3rc0p** (search the [LinkedIn profile](https://www.linkedin.com/in/th3cyb3rc0p/) for the current address) rather than opening a public GitHub issue. Give me a reasonable window to respond before disclosure.

## Threat model

OSCP Notes is a **local-first** app. It does not phone home, does not update itself, and does not expose any network port. The SQLite database (`~/OSCP-Notes/data/notes.db` on macOS, etc.) is stored on your local disk and is **never transmitted** anywhere.

Your threat model is whatever your local disk's threat model is: full-disk encryption (FileVault / BitLocker / LUKS) protects the database at rest; without it, anyone with the file can read it. The Notes / Tracker / Payloads tabs are **not encrypted at rest** — only the Vault tab is.

## Vault encryption

The **Vault tab** uses:

- **Cipher:** Fernet (AES-128-CBC + HMAC-SHA256, authenticated encryption)
- **Key derivation:** scrypt with a per-install random salt, stored in the same SQLite DB

The **master password is never stored**. The salt is stored, but it does not weaken the key on its own — deriving the key from the salt + your password is what scrypt is for. If you lose your master password, your vault entries are **unrecoverable by design**. There is no backdoor.

## What this app does not do

- No telemetry, analytics, or crash reporting
- No auto-update channel — you download and update manually
- No network calls in the running app (the only network use is `webbrowser.open(...)` when you click "Reveal Data Folder" / "Reveal Exported File", which is your default browser, not the app)
- No third-party tracking SDKs

## Dependency vulnerabilities

The runtime deps are pinned to current major versions:

- `markdown>=3.5`
- `Pygments>=2.17`
- `reportlab>=4.0`
- `openpyxl>=3.1`
- `cryptography>=42.0`

To check for known issues: `pip install pip-audit && pip-audit -r requirements.txt`.