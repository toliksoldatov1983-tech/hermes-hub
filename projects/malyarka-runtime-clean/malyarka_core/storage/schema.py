"""SQLite schema for the new Malyarka core.

The schema is created on a caller-provided ``sqlite3.Connection`` so this
module never opens or references the production database path.
"""

from __future__ import annotations

import sqlite3


def create_schema(connection: sqlite3.Connection) -> None:
    """Create all SQLite tables required by the new core.

    The caller owns the database connection. This function only applies the
    schema to that connection and does not open any database files itself.
    """

    connection.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            order_number TEXT,
            order_date TEXT,
            order_type TEXT,
            status TEXT NOT NULL DEFAULT 'draft',
            order_version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_type TEXT,
            height INTEGER NOT NULL,
            width INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            material TEXT,
            thickness TEXT,
            color TEXT,
            coating TEXT,
            milling_type TEXT,
            milling_side TEXT,
            painting_side TEXT,
            edge_processing TEXT,
            group_name TEXT,
            subgroup TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            note TEXT,
            source TEXT,
            confidence REAL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS disputed_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            raw TEXT NOT NULL,
            reason TEXT NOT NULL,
            source TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            thickness TEXT,
            unit TEXT,
            status TEXT NOT NULL DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT,
            status TEXT NOT NULL DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS coatings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS milling_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price_type TEXT NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            unit TEXT NOT NULL,
            valid_from TEXT,
            valid_to TEXT,
            status TEXT NOT NULL DEFAULT 'active'
        );

        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            file_type TEXT NOT NULL,
            path TEXT NOT NULL,
            file_version INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'actual',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            action TEXT NOT NULL,
            entity_type TEXT,
            entity_id INTEGER,
            old_value TEXT,
            new_value TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );

        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS command_aliases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            alias TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        );
        """
    )
    connection.commit()
