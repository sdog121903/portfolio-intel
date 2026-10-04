"""Shared helpers for the portfolio-intel toolbox. Standard library only (Python 3.9+).

Every tool script imports this module, so paths, config loading, HTTP and file I/O
behave the same way everywhere.
"""
from __future__ import annotations

import csv
import datetime as dt
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CONFIG = ROOT / "config"
LEARNING = ROOT / "learning"

# An honest, identifying User-Agent. Yahoo answers 429 to spoofed browser strings but serves this.
DEFAULT_UA = "portfolio-intel/1.0 (personal research)"
SECRET_PARAM = re.compile(r"((?:api_?key|token)=)[^&\s]+", re.I)


def redact(text: str) -> str:
    """Hide API keys and tokens in URLs; error messages end up in committed status files."""
    return SECRET_PARAM.sub(r"\1REDACTED", text)


# ---------------------------------------------------------------- config
def load_toml(path: Path) -> dict:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:  # pragma: no cover
        import tomli as tomllib  # pip install tomli
    with open(path, "rb") as f:
        return tomllib.load(f)


def portfolio_config() -> dict:
    return load_toml(CONFIG / "portfolio.toml")


def rules_config() -> dict:
    return load_toml(CONFIG / "rules.toml")


# ---------------------------------------------------------------- dates
def run_date() -> str:
    """Report date (ISO). RUN_DATE env var overrides, which keeps tests reproducible."""
    if os.environ.get("RUN_DATE"):
        return os.environ["RUN_DATE"]
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(portfolio_config().get("owner", {}).get("timezone", "UTC"))
        return dt.datetime.now(tz).date().isoformat()
    except Exception:
        return dt.date.today().isoformat()


def parse_date(s: str) -> dt.date:
    return dt.date.fromisoformat(str(s)[:10])


def days_between(a: str, b: str) -> int:
    return (parse_date(b) - parse_date(a)).days


# ---------------------------------------------------------------- HTTP
def http_get(url: str, headers: Optional[dict] = None, timeout: int = 30, retries: int = 3,
             backoff: float = 2.0) -> bytes:
    """GET with retries and gzip handling. Raises the last error if every attempt fails."""
    hdrs = {"User-Agent": DEFAULT_UA, "Accept-Encoding": "gzip"}
    hdrs.update(headers or {})
    last: Optional[Exception] = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
                return body
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (400, 401, 403, 404):  # retrying will not help
                break
        except Exception as e:  # network errors, timeouts
            last = e
        time.sleep(backoff * (attempt + 1))
    raise RuntimeError(redact(f"GET failed for {url}: {last}"))


# ---------------------------------------------------------------- files
def read_json(path: Path) -> Any:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=str)
        f.write("\n")
    return path


PRICE_FIELDS = ["date", "open", "high", "low", "close", "adj_close", "volume"]


def write_prices_csv(path: Path, rows: Iterable[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PRICE_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in PRICE_FIELDS})
    return path


def read_prices_csv(path: Path) -> list:
    """Rows sorted by date; numeric fields as float (None when blank)."""
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            row = {"date": r["date"]}
            for k in PRICE_FIELDS[1:]:
                v = r.get(k, "")
                row[k] = float(v) if v not in ("", None) else None
            if row["adj_close"] is None:
                row["adj_close"] = row["close"]
            if row["close"] is not None:
                out.append(row)
    out.sort(key=lambda x: x["date"])
    return out


def latest_file(folder: Path, pattern: str) -> Optional[Path]:
    files = sorted(folder.glob(pattern))
    return files[-1] if files else None


def load_holdings(date: Optional[str] = None) -> dict:
    folder = DATA / "holdings"
    path = folder / f"{date}.json" if date else latest_file(folder, "20*.json")
    if not path or not path.exists():
        raise FileNotFoundError("No normalised holdings file. Run load_holdings.py first.")
    return read_json(path)


# ---------------------------------------------------------------- math
def pct_change(new: Optional[float], old: Optional[float]) -> Optional[float]:
    if new is None or old in (None, 0):
        return None
    return (new / old - 1.0) * 100.0


def mean(xs: list) -> Optional[float]:
    return sum(xs) / len(xs) if xs else None


def stdev(xs: list) -> Optional[float]:
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def r(x: Optional[float], nd: int = 2) -> Optional[float]:
    return None if x is None else round(x, nd)


def log(msg: str) -> None:
    print(msg, file=sys.stderr)
