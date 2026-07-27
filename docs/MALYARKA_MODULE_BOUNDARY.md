# MALYARKA_MODULE_BOUNDARY

Malyarka is a module inside Hermes-Clean.

It starts with contracts only:

- order contract;
- parser contract;
- preview contract;
- dispute contract;
- export contract.

No old code is imported automatically. Real orders are not touched.

## Current local contracts

- `MalyarkaOrderRow` with `CONFIRMED` / `DISPUTED` status.
- `ParserContract` for manual dry-run text only.
- `build_preview` with confirmed/disputed counts.
- `has_blocking_disputes`.
- `export_blocked_until_confirmed`.

This is not a production parser yet.
