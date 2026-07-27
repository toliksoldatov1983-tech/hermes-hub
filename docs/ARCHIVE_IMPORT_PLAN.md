# Archive Import Plan

## Purpose

This plan describes how old Hermes archive sources can be reviewed later without making them the current project truth.

Current source of truth:

```text
C:\Users\user\Desktop\Hermes-Clean
```

Archive sources:

```text
[удалён] C:\Users\user\Desktop\«Гермес Клин».zip [архив]
C:\Users\user\Desktop\[архив] архивный zip-файл
```

## Current Rule

The archives are not a working project.

They must not be:

- deleted;
- moved;
- unpacked;
- used as direct source of truth;
- copied into Hermes-Clean automatically;
- scanned deeply without a separate approved block.

## Required Approval Gates

Archive unpack requires:

```text
APPROVE_ARCHIVE_UNPACK
```

Malyarka archive import requires:

```text
APPROVE_MALYARKA_ARCHIVE_IMPORT
```

Real order access requires:

```text
APPROVE_REAL_ORDER_ACCESS
```

Secret handling requires:

```text
APPROVE_SECRET_SETUP
```

## Future Safe Sequence

1. User chooses which archive can be inspected.
2. Codex creates a temporary inspection plan.
3. User explicitly approves archive unpack for that archive.
4. Archive is unpacked only into a dedicated quarantine/inspection folder, not into Hermes-Clean source folders.
5. Codex creates a shallow inventory only.
6. Files that may contain `.env`, tokens, keys, real orders or client data are marked blocked.
7. Nothing is copied into Hermes-Clean automatically.
8. User approves exact candidates for manual import.
9. Imported knowledge is rewritten as clean Hermes-Clean docs or contracts.
10. Old files remain archival evidence, not current truth.

## Blocked By Default

- automatic archive import;
- deep recursive scan;
- running old scripts;
- reading `.env`;
- reading databases;
- reading real orders;
- reading client documents;
- importing old memory automatically;
- sending archive content to external AI providers.

## Malyarka-Specific Rule

Old Malyarka files can inform future parser rules only after:

1. `APPROVE_MALYARKA_ARCHIVE_IMPORT`;
2. explicit user confirmation that the file is not a real customer order;
3. manual rewrite into a clean Hermes-Clean contract or synthetic fixture.

No old Malyarka spreadsheet or order file becomes current truth automatically.

## Output Of Future Archive Review

Future review should produce:

- archive inventory report;
- blocked files list;
- candidate import list;
- user approval checklist;
- clean rewritten Hermes-Clean docs/contracts;
- no direct dependency on old archive paths.
