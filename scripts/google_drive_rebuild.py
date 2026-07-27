from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\прайсы\Hermes-Clean")
TOKEN_PATH = Path(r"C:\Users\user\AppData\Local\hermes\google_token.json")
RESULT_PATH = PROJECT_ROOT / "05_REPORTS" / "GOOGLE_DRIVE_REBUILD_RESULT_2026-07-24.json"
ROOT_NAME = "МАЛЯРКА — УПРАВЛЕНИЕ"
FOLDER_MIME = "application/vnd.google-apps.folder"
DOC_MIME = "application/vnd.google-apps.document"

CATEGORIES = {
    "00": "00 НАЧАТЬ ЗДЕСЬ",
    "01": "01 ПРАВИЛА",
    "02": "02 ЦЕНЫ И НОРМЫ",
    "03": "03 ШАБЛОНЫ",
    "04": "04 ИНСТРУКЦИИ",
    "05": "05 ЭТАЛОНЫ",
}

DOCUMENTS = [
    ("00", "Главный индекс Малярки", "00_START/MALYARKA_DOCUMENT_INDEX.md", True),
    ("01", "Правила проекта", "00_START/PROJECT_RULES.md", False),
    ("01", "Приём заказа и спорные строки", "00_START/ORDER_INTAKE_RULES.md", False),
    ("01", "Красные линии и запреты", "00_START/GLOBAL_RED_LINES.md", False),
    ("02", "Реестр цен на услуги и нормы расхода", "00_START/PRICE_AND_LKM_FROM_GOOGLE_DRIVE.md", False),
    ("02", "Реестр цен материалов, состава ЛКМ и неизвестных значений", "00_START/HERMES_PRICE_STOCK_DRAFT.md", False),
    ("03", "Шаблон приёма заказа", "docs/malyarka_templates/ORDER_INTAKE_TEMPLATE.md", False),
    ("03", "Шаблон файла Corel", "docs/malyarka_templates/COREL_EXPORT_TEMPLATE.md", False),
    ("03", "Шаблон файла Малярки и материалов", "docs/malyarka_templates/MALYARKA_MATERIAL_TEMPLATE.md", False),
    ("03", "Шаблон финансов и себестоимости", "docs/malyarka_templates/FINANCE_AND_COST_TEMPLATE.md", False),
    ("03", "Шаблон архивной карточки заказа", "docs/malyarka_templates/ARCHIVE_ORDER_CARD_TEMPLATE.md", False),
    ("04", "Безопасное чтение CorelDRAW CDR", "00_MEMORY/CORELDRAW_CDR_READONLY_PROCESS.md", False),
    ("05", "Описание эталонов", "docs/malyarka_reference_orders/README.md", False),
    ("05", "Эталон Юля 001", "docs/malyarka_reference_orders/YULYA_001.md", False),
    ("05", "Эталон УЧ-002", "docs/malyarka_reference_orders/UCH_002.md", False),
    ("05", "Эталон УЧ-003", "docs/malyarka_reference_orders/UCH_003.md", False),
]


def execute_with_retry(request, attempts: int = 5):
    for attempt in range(attempts):
        try:
            return request.execute()
        except HttpError as error:
            status = getattr(error.resp, "status", None)
            if status not in {429, 500, 502, 503, 504} or attempt == attempts - 1:
                raise
            time.sleep(attempt + 1)


def escape_query(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def find_child(drive, name: str, parent_id: str | None, mime_type: str):
    clauses = [f"name = '{escape_query(name)}'", f"mimeType = '{mime_type}'", "trashed = false"]
    if parent_id:
        clauses.append(f"'{parent_id}' in parents")
    response = execute_with_retry(drive.files().list(
        q=" and ".join(clauses),
        spaces="drive",
        fields="files(id,name,mimeType,webViewLink,parents)",
        pageSize=10,
    ))
    files = response.get("files", [])
    if len(files) > 1:
        raise RuntimeError(f"Найдено несколько объектов с именем {name!r} в одном разделе")
    return files[0] if files else None


def ensure_folder(drive, name: str, parent_id: str | None):
    existing = find_child(drive, name, parent_id, FOLDER_MIME)
    if existing:
        return existing, False
    body = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        body["parents"] = [parent_id]
    created = execute_with_retry(drive.files().create(
        body=body,
        fields="id,name,mimeType,webViewLink,parents",
    ))
    return created, True


def document_text(docs, document_id: str) -> str:
    data = execute_with_retry(docs.documents().get(documentId=document_id))
    chunks: list[str] = []
    for block in data.get("body", {}).get("content", []):
        for element in block.get("paragraph", {}).get("elements", []):
            chunks.append(element.get("textRun", {}).get("content", ""))
    return "".join(chunks)


def populate_document(docs, document_id: str, body_text: str):
    for attempt in range(5):
        try:
            docs.documents().batchUpdate(
                documentId=document_id,
                body={"requests": [{"insertText": {"location": {"index": 1}, "text": body_text}}]},
            ).execute()
            return
        except HttpError as error:
            status = getattr(error.resp, "status", None)
            if status not in {429, 500, 502, 503, 504} or attempt == 4:
                raise
            time.sleep(attempt + 1)
            if len(document_text(docs, document_id).strip()) > 1:
                return


def create_document(drive, docs, title: str, parent_id: str, body_text: str):
    existing = find_child(drive, title, parent_id, DOC_MIME)
    if existing:
        if len(document_text(docs, existing["id"]).strip()) <= 1:
            populate_document(docs, existing["id"], body_text)
        return existing, False

    created = None
    for attempt in range(5):
        try:
            created = drive.files().create(
                body={"name": title, "mimeType": DOC_MIME, "parents": [parent_id]},
                fields="id,name,mimeType,webViewLink,parents",
            ).execute()
            break
        except HttpError as error:
            status = getattr(error.resp, "status", None)
            if status not in {429, 500, 502, 503, 504} or attempt == 4:
                raise
            time.sleep(attempt + 1)
            created = find_child(drive, title, parent_id, DOC_MIME)
            if created:
                break
    if created is None:
        raise RuntimeError(f"Не удалось создать документ {title!r}")
    populate_document(docs, created["id"], body_text)
    return created, True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Создать структуру на Google Drive")
    args = parser.parse_args()

    missing = [rel for _, _, rel, _ in DOCUMENTS if not (PROJECT_ROOT / rel).exists()]
    if missing:
        raise RuntimeError(f"Отсутствуют исходные файлы: {missing}")
    if not TOKEN_PATH.exists():
        raise RuntimeError("OAuth token не найден")

    if not args.apply:
        print(json.dumps({"status": "dry-run", "folders": 7, "documents": len(DOCUMENTS)}, ensure_ascii=False))
        return 0

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    docs = build("docs", "v1", credentials=creds, cache_discovery=False)

    root, root_created = ensure_folder(drive, ROOT_NAME, None)
    folders = {}
    created_folders = int(root_created)
    for key, name in CATEGORIES.items():
        folder, was_created = ensure_folder(drive, name, root["id"])
        folders[key] = folder
        created_folders += int(was_created)
        time.sleep(0.05)

    created_docs = 0
    records = []
    index_entry = None
    for category, title, rel, is_index in DOCUMENTS:
        if is_index:
            index_entry = (category, title, rel)
            continue
        source = PROJECT_ROOT / rel
        body = f"Канонический источник Hermes-Clean: {rel}\n\n{source.read_text(encoding='utf-8-sig')}"
        doc, was_created = create_document(drive, docs, title, folders[category]["id"], body)
        created_docs += int(was_created)
        records.append({"category": category, "title": title, "source": rel, **doc})
        time.sleep(0.05)

    if index_entry is None:
        raise RuntimeError("Главный индекс не определён")
    category, title, rel = index_entry
    source_text = (PROJECT_ROOT / rel).read_text(encoding="utf-8-sig")
    links = ["", "ССЫЛКИ НА ДОКУМЕНТЫ GOOGLE DRIVE", ""]
    for key in sorted(CATEGORIES):
        links.append(CATEGORIES[key])
        for record in [r for r in records if r["category"] == key]:
            links.append(f"- {record['title']}: {record['webViewLink']}")
        links.append("")
    index_body = f"Канонический источник Hermes-Clean: {rel}\n\n{source_text}\n" + "\n".join(links)
    index_doc, index_created = create_document(drive, docs, title, folders[category]["id"], index_body)
    created_docs += int(index_created)
    records.insert(0, {"category": category, "title": title, "source": rel, **index_doc})

    children = execute_with_retry(drive.files().list(
        q=f"'{root['id']}' in parents and trashed = false",
        spaces="drive",
        fields="files(id,name,mimeType)",
        pageSize=100,
    )).get("files", [])
    child_folders = [x for x in children if x.get("mimeType") == FOLDER_MIME]

    verification = []
    unsafe_permissions = []
    for record in records:
        text = document_text(docs, record["id"])
        verification.append({"title": record["title"], "characters": len(text), "nonempty": len(text.strip()) > 100})
        permissions = execute_with_retry(drive.permissions().list(
            fileId=record["id"],
            fields="permissions(id,type,role,emailAddress,domain)",
        )).get("permissions", [])
        bad = [p for p in permissions if p.get("type") in {"anyone", "domain"}]
        if bad:
            unsafe_permissions.append({"title": record["title"], "permissions": bad})

    result = {
        "status": "created-and-verified",
        "root": root,
        "folders_expected": 7,
        "folders_created_now": created_folders,
        "root_child_folders": len(child_folders),
        "documents_expected": len(DOCUMENTS),
        "documents_created_now": created_docs,
        "documents_verified": len(verification),
        "empty_documents": [x["title"] for x in verification if not x["nonempty"]],
        "unsafe_permissions": unsafe_permissions,
        "folders": folders,
        "documents": records,
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "root_id": root["id"],
        "root_link": root.get("webViewLink"),
        "root_child_folders": result["root_child_folders"],
        "documents_verified": result["documents_verified"],
        "empty_documents": result["empty_documents"],
        "unsafe_permissions_count": len(unsafe_permissions),
        "result_path": str(RESULT_PATH),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
