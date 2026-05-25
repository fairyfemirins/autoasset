#!/usr/bin/env python3

import click
import sqlite3
import pandas as pd
from datetime import datetime
import os

# Database setup
DB_PATH = os.path.expanduser("~/.autoasset.db")


def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            serial TEXT,
            owner TEXT,
            location TEXT,
            purchase_date TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@click.group()
def cli():
    """AutoAsset: Autonomous Asset Management for Developers."""
    init_db()


@cli.command()
@click.option("--name", required=True, help="Name of the asset (e.g., 'MacBook Pro').")
@click.option("--type", required=True, help="Type of asset (e.g., 'Hardware', 'Software').")
@click.option("--serial", help="Serial number or unique identifier.")
@click.option("--owner", help="Owner or team responsible for the asset.")
@click.option("--location", help="Physical or virtual location of the asset.")
@click.option("--purchase-date", help="Purchase date (YYYY-MM-DD).")
def add(name, type, serial, owner, location, purchase_date):
    """Add a new asset to the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO assets (name, type, serial, owner, location, purchase_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, type, serial, owner, location, purchase_date))
    conn.commit()
    conn.close()
    click.echo(f"Added asset: {name}")


@cli.command()
@click.option("--id", type=int, help="ID of the asset to remove.")
@click.option("--name", help="Name of the asset to remove.")
def remove(id, name):
    """Remove an asset from the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if id:
        cursor.execute("DELETE FROM assets WHERE id = ?", (id,))
    elif name:
        cursor.execute("DELETE FROM assets WHERE name = ?", (name,))
    else:
        click.echo("Error: Either --id or --name is required.")
        return
    conn.commit()
    conn.close()
    click.echo(f"Removed asset: {name or id}")


@cli.command()
@click.option("--type", help="Filter by asset type (e.g., 'Hardware').")
@click.option("--owner", help="Filter by owner.")
@click.option("--status", default="active", help="Filter by status (active/inactive).")
def list(type, owner, status):
    """List all assets in the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT * FROM assets WHERE status = ?"
    params = [status]
    if type:
        query += " AND type = ?"
        params.append(type)
    if owner:
        query += " AND owner = ?"
        params.append(owner)
    cursor.execute(query, params)
    assets = cursor.fetchall()
    conn.close()
    
    if not assets:
        click.echo("No assets found.")
        return
    
    for asset in assets:
        click.echo(f"ID: {asset[0]}, Name: {asset[1]}, Type: {asset[2]}, Serial: {asset[3]}, Owner: {asset[4]}, Location: {asset[5]}, Status: {asset[7]}")


@cli.command()
@click.option("--format", type=click.Choice(["csv", "json"]), required=True, help="Export format (csv or json).")
@click.option("--output", required=True, help="Output file path.")
def export(format, output):
    """Export the inventory to CSV or JSON."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM assets", conn)
    conn.close()
    
    if format == "csv":
        df.to_csv(output, index=False)
    elif format == "json":
        df.to_json(output, orient="records")
    
    click.echo(f"Exported inventory to {output}")


if __name__ == "__main__":
    cli()