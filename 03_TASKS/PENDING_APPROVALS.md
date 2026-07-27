# PENDING_APPROVALS

## Google Drive

- Google Drive LOW move pending.
- Требуется либо ручной перенос, либо переподключение Codex с нужными правами.
- Malyarka-документы не трогать.
- Sheets и Apps Script не трогать.

## Future gates

- `APPROVE_SECRET_SETUP`
- `APPROVE_TELEGRAM_LIVE`
- `APPROVE_REAL_ORDER_ACCESS`
- `APPROVE_MALYARKA_ARCHIVE_IMPORT`
- `APPROVE_ARCHIVE_UNPACK`

## Gemini

- Gemini setup pending.
- Required gate: `APPROVE_SECRET_SETUP`.
- Real `GEMINI_API_KEY` must not be stored in Hermes-Clean.
- Real `.env` must not be created automatically.
- First future Gemini test must use synthetic text only.
- Real orders, client documents, Google Drive files and old archives must not be sent to Gemini without separate approval.

## Archive Import

- Archive import pending.
- Archive unpack requires `APPROVE_ARCHIVE_UNPACK`.
- Malyarka archive import requires `APPROVE_MALYARKA_ARCHIVE_IMPORT`.
- Real order access requires `APPROVE_REAL_ORDER_ACCESS`.
- `«Гермес Клин».zip [архив]` and `[архив] архивный zip-файл` are archival sources only.
- Archives must not be unpacked, scanned deeply or copied into Hermes-Clean automatically.

## DeepSeek / DeepSig Review

- DeepSeek / DeepSig review setup pending.
- Required gate: `APPROVE_SECRET_SETUP`.
- Real review keys must not be stored in Hermes-Clean.
- Real `.env` must not be created or opened automatically.
- Review provider must not edit project files directly.
- Codex writes code and accepts or rejects review comments.
- Maximum review/fix cycles: 2.
- Real orders, client documents, Google Drive files, old archives and `[удалён]` must not be sent to review without separate approval.
