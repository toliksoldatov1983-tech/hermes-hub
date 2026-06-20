# Cleanup Rules

## Purpose

Prevent Hermes Hub from becoming messy like the old workspace.

## Folder Meaning

```text
_scratch     temporary experiments
_quarantine  suspicious or unsafe material
_archive     historical material, not active
_reports     generated reviews and audits
```

## Clean Project Zone

Future clean application code should live in:

```text
E:\Hermes-Hub\projects\malyarka-clean
```

## What Counts As Trash

- temporary extraction files;
- duplicate chat exports;
- generated caches;
- unfinished experiments outside `_scratch`;
- copied files from old Malyarka that were not reviewed;
- any file containing tokens or keys.

## Cleanup Procedure

1. List candidates.
2. Explain why each is trash or archive.
3. Move to `_quarantine` first, not delete.
4. Delete only after user confirms.

## Never Delete Without Permission

```text
state files
worklog
task files
project source
tests
orders data
memory
```

