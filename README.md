# AutoAsset

**Autonomous Asset Management for Developers**

AutoAsset is a lightweight, modular CLI tool for tracking hardware, software, licenses, and consumables. Designed for developers and small teams, it supports autonomous updates via cron jobs and integrates with version control for license tracking.

## Features
- Add/remove assets via CLI.
- Search and filter assets.
- Export inventory to CSV/JSON.
- Autonomous updates via cron.
- SQLite backend (no setup required).

## Installation
```bash
pip install autoasset
```

## Usage
```bash
# Add an asset
autoasset add --name "MacBook Pro" --type "Hardware" --serial "ABC123" --owner "team"

# List all assets
autoasset list

# Export to CSV
autoasset export --format csv --output inventory.csv
```

## Roadmap
- Web interface (Flask + SQLite).
- GitHub/GitLab integration for license tracking.
- Barcode/QR code scanning for physical assets.

## License
MIT