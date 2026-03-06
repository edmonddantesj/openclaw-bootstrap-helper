# Packs

This folder defines **install packs** for OpenClaw Bootstrap Helper.

Design goals:
- **Safe-mode by default**: scripts only *print* copy/paste commands.
- Split packs by **risk level**:
  - `*-lite` packs: public-safe utilities (no wallet/payment/autopost).
  - `*-restricted` packs: wallet/payment/autopost/credential-handling skills (opt-in only).

## Files
- `catalog.json` — pinned catalog of skills (slug → url, tags, short description).
- `pack_minimal.txt` — smallest recommended baseline.
- `pack_recommended.txt` — typical users.
- `pack_full_lite.txt` — everything **except** restricted.
- `pack_full_restricted.txt` — restricted skills (must be explicitly included).

Each `pack_*.txt` file is a newline-separated list of **skill slugs** that must exist in `catalog.json`.
