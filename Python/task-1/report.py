import csv
import sqlite3
import os
from datetime import date


def generate_report():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT today.asin, today.product_name, today.price, yesterday.price
        FROM products today
        JOIN products yesterday ON today.asin = yesterday.asin
        WHERE DATE(today.scraped_at) = DATE('now')
        AND DATE(yesterday.scraped_at) = DATE('now', '-1 day')
        AND today.price != yesterday.price           
    """
    )

    rows = cursor.fetchall()
    conn.close()

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{date.today()}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Old Price", "New Price", "Change"])
        for asin, name, new_price, old_price in rows:
            change = ((new_price - old_price) / old_price) * 100
            change_str = f"{change:+.1f}%"  # +31.3% or -22.2%
            writer.writerow([name, old_price, new_price, change_str])

    print(f"{len(rows)} price changes detected. Report saved to {filename}")

    print(f"\n=== Price Change Report ===")
    print(f"{'Product':<50} {'Old Price':>10} {'New Price':>10} {'Change':>8}")
    print("-" * 80)
    for asin, name, new_price, old_price in rows:
        change = ((new_price - old_price) / old_price) * 100
        change_str = f"{change:+.1f}%"
        print(f"{name[:50]:<50} {old_price:>10.2f} {new_price:>10.2f} {change_str:>8}")
    print("-" * 80)
    print(f"{len(rows)} price changes detected. Report saved to {filename}")
